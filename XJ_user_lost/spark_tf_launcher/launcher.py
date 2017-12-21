#! /usr/bin/env python

# IBM_PROLOG_BEGIN_TAG
# Copyright 2017 IBM Corp.
#
# All Rights Reserved.
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# IBM_PROLOG_END_TAG

#               ------------------------------------------
#               THIS SCRIPT PROVIDED AS IS WITHOUT SUPPORT
#               ------------------------------------------


from __future__ import print_function

import os, sys, stat, re
import random
import time
import threading
import Queue
import optparse

# use this module to get hostname and reserve tcp port
import socket
# use this module to serialize/de-serialze dict into/from mq
import pickle

# use this module to run task process
import subprocess

# use this module to escape input tf_args when generating commandline
import pipes

from pyspark import SparkConf, SparkContext
from redis import StrictRedis

CMD_REGISTER_CN_TASK = 'register_cn_task'
CMD_RESERVE_TF_PORTS = 'reserve_tf_ports'
CMD_REGISTER_TF_PORTS = 'register_tf_ports'
CMD_RUN_CMD = 'run_cmd'
CMD_FINISH_CMD = 'finish_cmd'
CMD_STOP_CN_TASK = 'stop_cn_task'

CMD_LOG_MSG = 'log_msg'
CMD_ECHO = 'echo'

TARGET_MASTER = 'driver'
TARGET_SLAVE = 'executor'

ERROR = '[E]:'
INFO = '[I]:'
WARN = '[W]:'
DEBUG = '[D]:'

NVIDIA_SMI_L_FAKE_OUTPUT = '/tmp/nvidia-smi-L.gpu_list.txt'

# balance GPU to CUDA_VISIBLE_DEVICES based on workload
# - num_gpus: number of visible GPUs to be exported, 0 means all
# - app_pid: application process id which need to be charged to the specific GPUs
def gpu_balance(num_gpus=0, app_pid=0, logger=print):
    if app_pid == 0:
        app_pid = os.getpid()

    #gpu_lines = subprocess.check_output(['nvidia-smi', '-L'], shell=False)
    lines = ''
    try:
        lines = subprocess.check_output(['nvidia-smi', '-L'], shell=False)
    except OSError as e:
        logger(ERROR, "\"%s\" failed with following error:\n%s" % (
            "nvidia-smi -L", '\n'.join(map(lambda line: ERROR + " >> "+line, str(e).split('\n')))))
        try:
            with open(os.devnull, 'w') as devnull:
                lines = subprocess.check_output(['cat', NVIDIA_SMI_L_FAKE_OUTPUT], shell=False,
                    stderr=devnull)
            logger(WARN, "Load GPU list from %s" % (NVIDIA_SMI_L_FAKE_OUTPUT))
        except:
            pass
    except subprocess.CalledProcessError as e:
        logger(ERROR, "\"%s\" failed with rc equals to %d and following error message:\n%s" % (
            "nvidia-smi -L", e.returncode, map(lambda line: ">> "+line, e.output)))

    gpu_lines = re.sub(r'^GPU\s+([0-9]+):.*UUID:\s+(.*)\)', r'\1,\2', lines, flags=re.MULTILINE).split('\n')

    # get all active processes in the OS to compare with
    # saved proc list for each GPU and drop inactive ones.
    all_pids = set(map(int,
        re.sub(r'^,+', '',
        re.sub(r',+$', '',
        re.sub(r'[\s\n]+', ',',
            subprocess.check_output(['ps', '-A', '-o', 'pid='], shell=False)))).split(',')))

    # loop for each GPUs
    gpus = []
    for line in gpu_lines:
        # make sure it is a valid GPU line
        items = line.split(',')
        if len(items) != 2 or re.match(r'^[0-9]+', items[0]) is None:
            continue

        # validate procs per GPU
        pids = ''
        pidf = "/tmp/gpu_pids.%s" % (items[1])
        try:
            with open(pidf, 'r') as pidf_obj:
                pids = \
                    re.sub(r'^,+', '',
                    re.sub(r',+$', '',
                    re.sub(r'[\s\n]+', ',', pidf_obj.read())))
        except:
            pass
        pids = pids.split(',') if pids != '' else []
        pids = set(map(int, pids))

        # update active GPU procs back
        active_pids = pids & all_pids
        if pids != active_pids:
            with open(pidf, 'w') as pidf_obj:
                for pid in active_pids:
                    pidf_obj.write("%d\n" % (pid))

        # prepare GPU info table to be sorted later
        gpu = {
            'id': int(items[0]),
            'uuid': items[1],
            'pidf': pidf,
            'pids': map(int, active_pids),
            'nproc': len(active_pids)
        }
        gpus.append(gpu)

    # balance GPU list by overhead asc
    gpus = sorted(gpus, key=lambda item: item['nproc'], reverse=False)

    # output for debug
    for gpu in gpus:
        logger(INFO, "%s,%s,%s,%s" % (gpu['id'], gpu['uuid'], gpu['nproc'], gpu['pidf']))

    # refine num_gpus
    if num_gpus == 0:
        num_gpus = len(gpus)

    # attach app pid to the target GPUs
    for gpu in gpus[:num_gpus]:
        pidf = gpu['pidf']
        with open(pidf, 'w+') as pidf_obj:
            pidf_obj.write("%s\n" % app_pid)

        # mark all writable if possible
        try:
            os.chmod(pidf,
                stat.S_IWUSR | stat.S_IRUSR | stat.S_IWGRP | stat.S_IRGRP | stat.S_IWOTH | stat.S_IROTH)
        except:
            pass

    # manipulate CUDA_VISIBLE_DEVICES list
    cmdline = 'export CUDA_VISIBLE_DEVICES="%s"' % (','.join(map(lambda item: item['uuid'], gpus[:num_gpus])))
    return cmdline if num_gpus > 0 else "true"


def get_appTop(app_id):
    return app_id


def get_appChannelCtrl(app_id):
    return "%s/channel_ctrl" % (app_id)


def publish_msg(r, ch, logger=print, **kw):
    logging = False
    if "catetory" in kw:
        if kw['catetory'] == 'log_msg':
            logging = False

    if logging:
        logger(INFO, "publish msg: >>", kw)
    return r.publish(ch, pickle.dumps(kw))


def msg_handler(msg, myfilter, myroutes, logger=print):
    msg_dict = {}

    # de-serialize msg to dict by pickle
    if msg['type'] == 'message':
        try:
            msg_dict = pickle.loads(msg['data'])
        except:
            logger(ERROR, "ignore un-pickleable msg: [%s]" % (msg['data']))
            return False
    else:
        # we only handle "message"
        return True

    # filter msg first
    rc = True
    prefix = ""
    func = None
    level = DEBUG
    if not myfilter(msg_dict):
        category = msg_dict['category']

        # pick up msg handler from routes
        if category in myroutes:
            func = myroutes[category]

            # ignore log_msg
            # if there is already handler in the routes table
            if category != CMD_LOG_MSG or func is None:
                prefix = "handle msg: >>"
        else:
            prefix = "no routes for msg: >>"
            rc = False
            level = ERROR

    # log for debug
    if prefix != "":
        logger(level, "%s %s" % (prefix, str(msg_dict)))

    # call msg handler if exist
    if func != None:
        rc = func(msg_dict)

    return rc


def call_in_background(f, *args):
    result = Queue.Queue(1)
    t = threading.Thread(target=lambda: result.put(f(*args)))
    t.daemon = True
    t.start()

    return result


def stream_reader(stream, fout, fmt, queue):
    for line in iter(stream.readline, b''):
        fout(line)
        queue.put(fmt(line))

def track_subprocess(popenobj, fout, ferr, fall, fterm):
    q = Queue.Queue()

    # thread for stdout
    tout = threading.Thread(target = stream_reader, args = (
        popenobj.stdout,
        fout,
        lambda line: "stdout: >> %s" % (line.rstrip()),
        q
    ))
    tout.daemon = True
    tout.start()

    # thread for stderr
    terr = threading.Thread(target = stream_reader, args = (
        popenobj.stderr,
        ferr,
        lambda line: "stderr: >> %s" % (line.rstrip()),
        q
    ))
    terr.daemon = True
    terr.start()

    # thread for merged output
    def output_queue_reader():
        while tout.isAlive() or terr.isAlive():
            try:
                line = q.get_nowait()
            except Queue.Empty:
                pass
            else:
                fall(line)

    tall = threading.Thread(target = output_queue_reader)
    tall.daemon = True
    tall.start()

    # wait for terminiate
    #while popenobj.poll() is None:
    #    time.sleep(1)
    popenobj.wait()

    # wait for monitor thread
    tall.join()

    # call post process
    if fterm != None:
        fterm(popenobj)

    return True

# sleep_interval: unit seconds of time.sleep(), default 0.01
# timeout: time of sleep before give up, default to 0. -1 means wait forever
def wait_for_condition(fcond, **kw):
    timeout = 0
    sleep_interval = 0.001
    if kw != None:
        if 'timeout' in kw: timeout = kw['timeout']
        if 'sleep_interval' in kw: sleep_interval = kw['sleep_interval']

    try_cnt = int(timeout / sleep_interval)
    cnt = 0
    rc = fcond()
    while not rc and (cnt < try_cnt or try_cnt < 0):
        #print("wait for cnt=%d, interval=%f" % (cnt, sleep_interval))
        time.sleep(sleep_interval)
        rc = fcond()
        cnt += 1

    return rc

class SlaveTask(object):
    # reserve a free tcp port
    __reserved_tcp_ports = []
    def reserve_tcp_port(self, addr='', port=0):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((addr, port))
            self.__reserved_tcp_ports.append(s)

            addr, port = s.getsockname()
            self.log_msg(DEBUG, "Reserve tcp port at %s:%d" % (addr, port))
        except socket.error as msg:
            self.log_msg(ERROR, "Failed to reserve a tcp port with error message: %s" % (msg))

            s.close()
            s = None
        return s

    # free reserved tcp port
    # free all by default,
    def free_reserved_tcp_port(self, addr='', port=0):
        freed_ports = []
        for s in self.__reserved_tcp_ports:
            saddr, sport = s.getsockname()
            if ((addr != '') and (addr != saddr)) or \
               ((port != 0) and (port != sport)):
                continue

            try:
                s.shutdown(socket.SHUT_RDWR)
            except:
                pass
            else:
                self.log_msg(INFO, "Shutdown connections at %s:%d" % (saddr, sport))

            self.log_msg(DEBUG, "Free tcp port %s:%d" % (saddr, sport))
            s.close()
            freed_ports.append(s)

        for s in freed_ports:
            self.__reserved_tcp_ports.remove(s)
            self.log_msg(DEBUG, "cnt = %d" % len(self.__reserved_tcp_ports))

        return len(freed_ports)


    # beacon by redis
    partition_index = 0
    iterator = None

    r = None
    channel_ctrl = ''

    q = None
    hostname = ''

    __msg_routes = {}

    def __init__(self, partition_index, iterator, input_params_V):
        self.channel_ctrl = input_params_V['channel_ctrl']
        redis_serv = input_params_V['redis_serv']
        redis_port = input_params_V['redis_port']

        # save rdd parameter
        self.partition_index = partition_index
        self.iterator = iterator

        # estatlish connection to the beacon
        self.r = StrictRedis(host=redis_serv, port=redis_port)

        # find out hostname of running host
        self.hostname = socket.getfqdn()

        # semaphear to sync between main thread and mq engine
        self.q = Queue.Queue(1)

        # define msg handler routes
        self.__msg_routes[CMD_RESERVE_TF_PORTS] = lambda msg_dict: self.handle_reserve_tf_ports(
            msg_dict['number']
        )
        self.__msg_routes[CMD_RUN_CMD] = lambda msg_dict: self.handle_run_cmd(
            msg_dict['cmd'],
            msg_dict['blocking'],
            msg_dict['ports'],
            msg_dict['gpu_balance']
        )
        self.__msg_routes[CMD_STOP_CN_TASK] = lambda msg_dict: self.handle_stop_cn_task()


    # debug function
    # log msg to local and central beacon
    def log_msg(self, level, msg, publish=True, **kw):
        if level != ERROR: return True

        # to local
        print(level, msg, kw)

        # to remote
        if publish:
            publish_msg(self.r, self.channel_ctrl,
                target = TARGET_MASTER,
                source = TARGET_SLAVE,
                partition_index = self.partition_index,
                host = self.hostname,
                category = CMD_LOG_MSG,
                level = level,
                content = msg,
                **kw
            )

        return True


    # register executor task to the beacon
    def register_cn_task(self):
        self.log_msg(DEBUG, "calling \"register_cn_task\"", hostname = self.hostname)

        return publish_msg(self.r, self.channel_ctrl,
            target = TARGET_MASTER,
            src = TARGET_SLAVE,
            partition_index = self.partition_index,
            category = CMD_REGISTER_CN_TASK,
            hostname = self.hostname)


    # handle reserve_tf_ports command from driver
    def handle_reserve_tf_ports(self, number):
        self.log_msg(DEBUG, "calling \"handle_reserve_tf_ports\"", number = number)

        # reserver TCP ports for PS and/or WORKER services of TensorFlow task, and
        ports = []
        for i in xrange(number):
            s = self.reserve_tcp_port()
            if s is None:
                self.log_msg(ERROR, "fail to reserver the %d'th tcp port." % (i))
                return False

            _, port = s.getsockname()
            #port = random.randint(11100,11190)
            ports.append(port)

        # register reserved ports to the beacon
        publish_msg(self.r, self.channel_ctrl,
            target = TARGET_MASTER,
            src = TARGET_SLAVE,
            partition_index = self.partition_index,
            category = CMD_REGISTER_TF_PORTS,
            ports = ports)

        return True


    __processes = {}
    def handle_run_cmd(self, cmd, blocking, ports, gpu):
        self.log_msg(DEBUG, "calling \"handle_run_cmd\"",
            cmd = cmd, blocking = blocking, ports = ports, gpu_balance = gpu 
        )

        # free reserved ports just before launching the tf command
        for port in ports:
            self.free_reserved_tcp_port('', port)

        # insert gpu balance cmdline when needed
        # NOTE: if not requested, assume run on CPU by exporting empty GPU list
        # to CUDA_VISIBLE_DEVICES env variables.
        env_val = os.getenv('CUDA_VISIBLE_DEVICES')
        if env_val is None or env_val == '':
            if gpu:
                # TODO: num_gpus as argument in future
                gpu_balance_cmdline = gpu_balance(num_gpus=1, app_pid=0, logger=self.log_msg)
                cmd = "set -x; %s; set +x; %s" % (gpu_balance_cmdline, cmd)

                self.log_msg(DEBUG, "mod cmd(wk): %s" % (cmd))

            else:
                cmd = "set -x; %s; set +x; %s" % ("export CUDA_VISIBLE_DEVICES=''", cmd)

                self.log_msg(DEBUG, "mod cmd(ps): %s" % (cmd))


        # execute command
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
        pid = p.pid

        # define function to display merged stdout and stderr
        def fall(line):
            self.log_msg(DEBUG, "[%d] >> %s" % (pid, line.rstrip()))

        # define post process if blocking subprocess had finished
        if blocking:
            fterm = lambda popenobj: publish_msg(self.r, self.channel_ctrl,
                    target = TARGET_MASTER,
                    src = TARGET_SLAVE,
                    partition_index = self.partition_index,
                    category = CMD_FINISH_CMD,
                    output = [],
                    error = [],
                    returncode = popenobj.returncode
            )
        else:
            fterm = None

        # start thraed to tracking process asychronizely
        result = call_in_background(track_subprocess,
            p, sys.stdout.write, sys.stderr.write, fall, fterm)

        # register executing command process
        self.__processes[pid] = dict(
            popenobj = p,
            blocking = blocking,
            tracker = result
        )

        self.log_msg(DEBUG, "ending \"handle_run_cmd\"")
        return True


    def handle_stop_cn_task(self):
        self.log_msg(DEBUG, "calling \"handle_stop_cn_task\"")

        # terminate non-blocking sub process
        for pid in iter(self.__processes):
            d = self.__processes[pid]
            p = d['popenobj']
            blocking = d['blocking']
            tracker = d['tracker']

            if not blocking:
                # xian li
                self.log_msg(DEBUG, "wait[1] for non blocking process %d" % (p.pid))
                if not wait_for_condition(lambda: p.poll() != None, timeout=0):
                    self.log_msg(INFO, "terminate subprocess %d forcely by %s" % (p.pid, 'sig_term'))
                    p.terminate()

                    # hou bing
                    self.log_msg(DEBUG, "wait[2] for non blocking process %d" % (p.pid))
                    if not wait_for_condition(lambda: p.poll() != None, timeout=0.1):
                        self.log_msg(INFO, "terminate subprocess %d forcely by %s" % (p.pid, 'sig_kill'))
                        p.kill()

            self.log_msg(DEBUG, "wait[3] for non blocking process %d" % (p.pid))
            if not wait_for_condition(lambda: p.poll() != None, timeout=1):
                self.log_msg(ERROR, "subprocess %d not termianted!" %(p.pid))

            self.log_msg(DEBUG, "wait[4] for non blocking process %d" % (p.pid))
            if tracker.empty():
                self.log_msg(ERROR, "subprocess %d's tracker does not finished!" %(p.pid))

        self.q.put('xxx', 1)
        return True


    def msg_filter(self, msg_dict):
        try:
            target = msg_dict['target']
            partition_index = msg_dict['partition_index']
        except:
            target = ''
            partition_index = -2

        return (target != TARGET_SLAVE) or ((partition_index != self.partition_index) and (partition_index != -1))


    def msg_handler(self, msg):
        # this msg should NOT be published to remote in order to break the recurisve call to itself
        # because we are sharing the same beacon and can see our own post.
        self.log_msg(DEBUG, "calling \"msg_handler\"", False)

        # DEBUG: echo msg back to master
        msg_dict = pickle.loads(msg['data'])
        if not self.msg_filter(msg_dict): 
            publish_msg(self.r, self.channel_ctrl,
                target = TARGET_MASTER,
                src = TARGET_SLAVE,
                partition_index = self.partition_index,
                category = CMD_ECHO,
                host = self.hostname,
                echo_msg = str(msg_dict))

        return msg_handler(msg, self.msg_filter, self.__msg_routes, self.log_msg)


    # logic in executor node which will
    # cooperate with driver task to parepare resource and launch real TF process
    def main(self):
        # TODO
        # initialize random seed in case there are multiple tasks in same CN host
        # this is mainly used by the faked tf port reserving before the real reserving
        # logic had been implemented.
        random.seed()

        # driver mq start
        ps = self.r.pubsub()
        ps.subscribe(**{self.channel_ctrl: self.msg_handler})
        mq_t = ps.run_in_thread(sleep_time=0.001)

        self.log_msg(INFO, "mq started at slave")
        self.register_cn_task()

        # wait for the "STOP" command from driver
        self.q.get(1)

        # stop mq
        mq_t.stop()

        # clean up resources
        self.free_reserved_tcp_port()

        return (self.partition_index, self.iterator.next()**3)


class MasterTask(object):
    # beacon by redis
    r = None
    channel_ctrl = ''

    # application id which will be used to distinguish logs in the same node
    app_id = ''

    # number of cn tasks / partitions
    partitions = 0
    num_of_ps_hosts = 0
    num_of_worker_hosts = 0
    tf_model = ''
    tf_args = []

    # semaphore to sync between mq and task main thread
    q = None

    # message routes for mq
    __msg_routes = {}

    def __init__(self, input_params_V):
        self.partitions = input_params_V['partitions']
        self.channel_ctrl = input_params_V['channel_ctrl']
        redis_serv = input_params_V['redis_serv']
        redis_port = input_params_V['redis_port']
        self.num_of_worker_hosts = input_params_V['num_of_worker_hosts']
        self.num_of_ps_hosts = input_params_V['num_of_ps_hosts']
        self.tf_model = input_params_V['tf_model']
        self.tf_args = input_params_V['tf_args']

        # app id to distinguish logs
        self.app_id = input_params_V['app_id']

        # estatlish connection to the beacon
        self.r = StrictRedis(host=redis_serv, port=redis_port)

        # semaphear to sync between main thread and mq engine
        self.q = Queue.Queue(1)

        # define msg handler routes
        self.__msg_routes[CMD_REGISTER_CN_TASK] = lambda msg_dict: self.handle_register_cn_task(
                msg_dict['partition_index'],
                msg_dict['hostname']
        )
        self.__msg_routes[CMD_REGISTER_TF_PORTS] = lambda msg_dict: self.handle_register_tf_ports(
                msg_dict['partition_index'],
                msg_dict['ports']
        )
        self.__msg_routes[CMD_FINISH_CMD] = lambda msg_dict: self.handle_finish_cmd(
                msg_dict['partition_index'],
                msg_dict['returncode'],
                msg_dict['output'],
                msg_dict['error'],
        )
        self.__msg_routes[CMD_LOG_MSG] = lambda msg_dict: self.handle_log_msg(
                msg_dict['level'],
                msg_dict['partition_index'],
                msg_dict['host'],
                msg_dict['content']
        )
        self.__msg_routes[CMD_ECHO] = lambda msg_dict: self.handle_log_msg(
                DEBUG,
                msg_dict['partition_index'],
                msg_dict['host'],
                "echo: >> %s" % (msg_dict['echo_msg'])
        )


    # debug function
    # log msg to local and central beacon
    def log_msg(self, level, msg, publish=False, **kw):
        # to local
        print(level, msg, kw)

        # TODO: to remote, not necessary and disabled for now.
        if publish and False:
            publish_msg(self.r, self.channel_ctrl,
                target = TARGET_MASTER,
                source = TARGET_MASTER,
                category = CMD_LOG_MSG,
                level = level,
                content = msg,
                **kw
            )

        return True


    def handle_log_msg(self, level, partition_index, hostname, content):
        return self.log_msg(level, "remote_msg: [%2d][%s]: >> %s" % (partition_index, hostname, content), False)


    def msg_filter(self, msg_dict):
        try:
            target = msg_dict['target']
        except:
            target = ''

        return (target != TARGET_MASTER)


    def msg_handler(self, msg):
        # this msg should NOT be published to remote in order to break the recurisve call to itself
        # because we are sharing the same beacon and can see our own post.
        #self.log_msg(DEBUG, "calling \"msg_handler\"", False)

        # DEBUG: echo msg back to master
        # disable in Master for now
        msg_dict = pickle.loads(msg['data'])
        if not self.msg_filter(msg_dict) and False:
            publish_msg(self.r, self.channel_ctrl,
                target = msg_dict['src'],
                src = msg_dict['target'],
                partition_index = msg_dict['partition_index'],
                category = CMD_ECHO,
                echo_msg = str(msg_dict))

        return msg_handler(msg, self.msg_filter, self.__msg_routes, self.log_msg)


    # response cn task registration
    __registered_cn_tasks = {}
    def handle_register_cn_task(self, partition_index, hostname):
        self.log_msg(DEBUG, "calling \"handle_register_cn_task\"",
            partition_index = partition_index, hostname = hostname,
            cnt = len(self.__registered_cn_tasks))

        self.__registered_cn_tasks[partition_index] = dict(
            hostname = hostname,
            num_of_ps_ports = 0,
            num_of_worker_ports = 0,
        )
        if len(self.__registered_cn_tasks) >= self.partitions:
            self.plan_tf_ports()
            self.reserve_tf_ports()

        return True


    def plan_tf_ports(self):
        self.log_msg(DEBUG, "calling \"plan_tf_ports\"",
            registered_cn_tasks = self.__registered_cn_tasks)

        idxs = range(self.partitions)
        random.shuffle(idxs)

        ps_ports_cnt = 0
        ps_hosts = []
        for i in xrange(self.num_of_worker_hosts):
            partition_index = idxs[i]

            d = self.__registered_cn_tasks[partition_index]
            d['num_of_worker_ports'] += 1

            # skip if ps_hosts are all allocated
            if ps_ports_cnt >= self.num_of_ps_hosts: continue

            # prefer to distribute ps_host
            hostname = d['hostname']
            if hostname in ps_hosts: continue

            # pick up a ps_host and record
            d['num_of_ps_ports'] += 1
            ps_ports_cnt += 1
            ps_hosts.append(hostname)


    def reserve_tf_ports(self):
        self.log_msg(DEBUG, "calling \"reserve_tf_ports\"",
            registered_cn_tasks = self.__registered_cn_tasks)

        for partition_index in xrange(self.partitions):
            d = self.__registered_cn_tasks[partition_index]
            num_of_ports = d['num_of_ps_ports'] + d['num_of_worker_ports']


            # TODO: always reserver two ports per cn task
            publish_msg(self.r, self.channel_ctrl,
                target = TARGET_SLAVE,
                src = TARGET_MASTER,
                partition_index = partition_index,
                category = CMD_RESERVE_TF_PORTS,
                number = num_of_ports)

        return True


    __registered_tf_ports = {}
    def handle_register_tf_ports(self, partition_index, ports):
        self.log_msg(DEBUG, "calling \"handle_register_tf_ports\"",
            partition_index = partition_index, ports = ports,
            cnt = len(self.__registered_tf_ports))

        self.__registered_tf_ports[partition_index] = ports
        if len(self.__registered_tf_ports) >= self.partitions:
            self.generate_tf_cmd()
            self.run_cmd()

        return True


    def generate_tf_cmd(self):
        self.log_msg(DEBUG, "calling \"generate_tf_cmd\"")

        # generate --ps_hosts and --worker_hosts
        ps_hosts_str = ''
        worker_hosts_str = ''
        for partition_index in xrange(self.partitions):
            ports = self.__registered_tf_ports[partition_index]

            d = self.__registered_cn_tasks[partition_index]
            hostname = d['hostname']
            num_of_ps_ports = d['num_of_ps_ports']
            num_of_worker_ports = d['num_of_worker_ports']

            for port in ports[:num_of_ps_ports]:
                if ps_hosts_str != '': ps_hosts_str += ','
                ps_hosts_str += "%s:%d" % (hostname, port)

            for port in ports[num_of_ps_ports:]:
                if worker_hosts_str != '': worker_hosts_str += ','
                worker_hosts_str += "%s:%d" % (hostname, port)

        # consolidate common part of tf command line
        model_dir = os.path.dirname(self.tf_model)
        model_file = os.path.basename(self.tf_model)
        prefix = "python %s --ps_hosts=\"%s\" --worker_hosts=\"%s\"" % (
            model_file,
            ps_hosts_str,
            worker_hosts_str
        )

        # generate task spefic tf cmd line
        ps_task_id = 0
        tf_args_line = reduce(lambda x, y: "%s %s" % (x, pipes.quote(y)), self.tf_args, "")
        for partition_index in xrange(self.partitions):
            d = self.__registered_cn_tasks[partition_index]
            hostname = d['hostname']
            num_of_ps_ports = d['num_of_ps_ports']
            num_of_worker_ports = d['num_of_worker_ports']

            ps_cmdline = ''
            if num_of_ps_ports > 0:
                ps_cmdline = prefix + " --task_id=%d --job_name=ps %s" % (ps_task_id, tf_args_line)
                d['ps_cmdline'] = "set -x; if cd %s; then %s; echo finish; else false; fi 2>&1 | tee /tmp/log.ps.t%d.%s" % (
                    model_dir,
                    ps_cmdline,
                    ps_task_id,
                    self.app_id
                )
                ps_task_id += 1

            worker_cmdline = prefix + " --task_id=%d --job_name=worker %s" % (partition_index, tf_args_line)
            d['worker_cmdline'] = "set -x; if cd %s; then %s; echo finish; else false; fi 2>&1 | tee /tmp/log.wk.t%d.%s" % (
                model_dir,
                worker_cmdline,
                partition_index,
                self.app_id
            )

        self.log_msg(DEBUG, ">> %s" % (self.__registered_cn_tasks))

    def run_cmd(self):
        self.log_msg(DEBUG, "calling \"run_cmd\"",
            registered_cn_tasks = self.__registered_cn_tasks
        )

        # fire ps first
        for partition_index in xrange(self.partitions):
            ports = self.__registered_tf_ports[partition_index]

            d = self.__registered_cn_tasks[partition_index]
            num_of_ps_ports = d['num_of_ps_ports']

            # TODO:
            # to workaround a problem in slave side about releasing and rebinding the worker's port
            # all reserved ports will be freed when launching ps task in the same node.
            # NOTE: This will increase the worker port conflicting between different tf jobs which
            # launched by this installer.
            if 'ps_cmdline' in d:
                cmdline = d['ps_cmdline']
                publish_msg(self.r, self.channel_ctrl,
                    target = TARGET_SLAVE,
                    src = TARGET_MASTER,
                    partition_index = partition_index,
                    category = CMD_RUN_CMD,
                    cmd = cmdline,
                    blocking = False,
                    #ports = ports[:num_of_ps_ports]
                    ports = [0],
                    gpu_balance = False
                )

        time.sleep(2)

        # fire worker
        for partition_index in xrange(self.partitions):
            ports = self.__registered_tf_ports[partition_index]

            d = self.__registered_cn_tasks[partition_index]
            num_of_ps_ports = d['num_of_ps_ports']

            if 'worker_cmdline' in d:
                cmdline = d['worker_cmdline']
                publish_msg(self.r, self.channel_ctrl,
                    target = TARGET_SLAVE,
                    src = TARGET_MASTER,
                    partition_index = partition_index,
                    category = CMD_RUN_CMD,
                    cmd = cmdline,
                    blocking = True,
                    ports = ports[num_of_ps_ports:],
                    gpu_balance = True
                )

        return True


    __finished_cn_tasks = {}
    def handle_finish_cmd(self, partition_index, rc, output, error):
        self.log_msg(DEBUG, "calling \"handle_finish_cmd\"",
            partition_index = partition_index, returncode = rc,
            cnt = len(self.__finished_cn_tasks))

        self.__finished_cn_tasks[partition_index] = dict(rc = rc, output = output, error = error)
        if len(self.__finished_cn_tasks) >= self.partitions:
            self.stop_cn_tasks()

        return True


    def stop_cn_tasks(self):
        self.log_msg(DEBUG, "calling \"stop_cn_tasks\"")

        # Stop all cn tasks
        for partition_index in xrange(self.partitions):
            publish_msg(self.r, self.channel_ctrl,
                target = TARGET_SLAVE,
                src = TARGET_MASTER,
                partition_index = partition_index,
                category = CMD_STOP_CN_TASK
            )

        # all done, mq could be stopped
        self.q.put('xxx', 1)
        return True


    # logic in executor node which will
    # cooperate with driver task to parepare resource and launch real TF process
    def main(self):
        # start mq
        ps = self.r.pubsub()
        ps.subscribe(**{self.channel_ctrl: self.msg_handler})
        mq_t = ps.run_in_thread(sleep_time=0.001)

        self.log_msg(INFO, "mq started at master")
        # TODO: announce master?

        # wait for the mq terminiation semaphore
        self.q.get(1)

        # stop mq
        mq_t.stop()

        return True


def main():
    parser = optparse.OptionParser()
    parser.add_option("--model",
        action="store", dest="model", type="string",
        default="", metavar="<tf_model_path>",
        help="Tensorflow model"
    )
    parser.add_option("--worker",
        action="store", dest="num_of_worker_hosts", type="int",
        default=2, metavar="N",
        help="number of worker tasks for distributed Tensorflow job. Default is %default"
    )
    parser.add_option("--ps",
        action="store", dest="num_of_ps_hosts", type="int",
        default=1, metavar="N",
        help="number of ps tasks for distributed Tensorflow job. Default is %default"
    )
    parser.add_option("--redis_host",
        action="store", dest="redis_host", type="string",
        default="", metavar="host",
        help="redis server address"
    )
    parser.add_option("--redis_port",
        action="store", dest="redis_port", type="int",
        default=6379, metavar="port",
        help="redis server tcp port. Default is %default"
    )

    # parse input parameters
    (options, args) = parser.parse_args()
    print({'options': options, 'args': args})

    # assign the input parameters
    partitions = options.num_of_worker_hosts
    redis_serv = options.redis_host
    redis_port = options.redis_port
    num_of_worker_hosts = options.num_of_worker_hosts
    num_of_ps_hosts = options.num_of_ps_hosts
    tf_model = options.model
    tf_args = args

    if num_of_ps_hosts > num_of_worker_hosts:
        print("Error: The number of ps tasks should NOT great than the number of worker tasks. Abort!", file=sys.stderr)
        return 1

    if tf_model is None or tf_model == "":
        print("Error: The model url should NOT be empty. Abort!", file=sys.stderr)
        return 1

    if redis_serv is None or redis_serv == "":
        print("Error: Redis host should NOT be empty. Abort!", file=sys.stderr)
        return 1

    # initialize Spark context
    conf = SparkConf().set("spark.ui.showConsoleProgress", "false")
    sc = SparkContext(appName="PySparkTensorFlowJobLauncher", conf=conf)

    # pick up the application id and pass to all functions as if it's a global variable.
    # TODO: can executor task pick it from any contact instead of passing in globally?
    app_id = sc.applicationId
    channel_ctrl = get_appChannelCtrl(app_id)

    input_params = sc.broadcast(dict(
        app_id = app_id,
        partitions = partitions,
        channel_ctrl = channel_ctrl,
        redis_serv = redis_serv,
        redis_port = redis_port,
        num_of_worker_hosts = num_of_worker_hosts,
        num_of_ps_hosts = num_of_ps_hosts,
        tf_model = tf_model,
        tf_args = tf_args
    ))

    # a dumy RDD
    def run_rdd():
        rdd = sc.parallelize(range(partitions), partitions).mapPartitionsWithIndex(
            lambda idx, iterator: SlaveTask(idx, iterator, input_params.value).main())
        return rdd.glom().collect()

    # start the job asynchronizly.
    result = call_in_background(run_rdd)

    # launch master
    master = MasterTask(input_params.value)
    q_main = call_in_background(master.main)

    # monitor and control the job flow in driver
    status = sc.statusTracker()
    while result.empty():
        ids = status.getJobIdsForGroup()
        for id in ids:
            job = status.getJobInfo(id)
            print("Job", id, "status: ", job.status)
            for sid in job.stageIds:
                info = status.getStageInfo(sid)
                if info:
                    print("Stage %d: %d tasks total (%d active, %d complete)" %
                          (sid, info.numTasks, info.numActiveTasks, info.numCompletedTasks))
        time.sleep(1)

    print("Job results are:", result.get())
    sc.stop()

    q_main.get(1)
    return True


if __name__ == "__main__":
    main()

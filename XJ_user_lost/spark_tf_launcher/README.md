Tensorflow job launcher for Spark
===================


Usage sample
-------------------
    # Startup a redis server
    $ docker run --name redis-data -v /data -d ppc64le/busybox
    $ docker run --name redis --volumes-from redis-data -p 6379:6379 -d ppc64le/redis
    $ hostname
    x3650m2n5-hs.clusters.com
    
    $ cd ~/workspace/bluemind/tools/spark_tf_launcher
    
    $ spark-submit --master yarn ./launcher.py --help
    Usage: launcher.py [options]
    
    Options:
      -h, --help            show this help message and exit
      --model=<tf_model_path>
                            Tensorflow model
      --worker=N            number of worker tasks for distributed Tensorflow job.
                            Default is 2
      --ps=N                number of ps tasks for distributed Tensorflow job.
                            Default is 1
      --redis_host=host     redis server address
      --redis_port=port     redis server tcp port. Default is 6379
    
    $ spark-submit \
        --master yarn \                                        <== parameter for spark-submit
        ./launcher.py \
            --model=`pwd`/cifar10_async_dist_train.py \        <== parameter for launcher.py
            --redis_host=x3650m2n5-hs.clusters.com \           <== ...
            --worker=2 --ps=1 \
            -- \
              --data_dir=/gpfs/dlfs1/data/cifar10 \            <== parameters for tf model .py
              --train_dir=/tmp/yarn/train \                    <== ...
              --max_steps=500
                
    {'args': ['--train_dir=/tmp/yarn2/train', '--max_steps=500'], 'options': <Values at 0x7f3cffe7afc8: {'redis_host': 'x3650m2n5-hs.clusters.com', 'model': '/u/fuzhiwen/workspace/bluemind/tools/spark_tf_launcher/cifar10_async_dist_train.py', 'redis_port': 6379, 'num_of_worker_hosts': 2, 'num_of_ps_hosts': 1}>}
    17/01/19 08:47:27 INFO SparkContext: Running Spark version 1.6.2
    ...
    Job 0 status:  RUNNING
    Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> Session init done {}
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> Started 2 queues for processing input data. {}
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> INFO:tensorflow:Variable/sec: 0 {}
    Job 0 status:  RUNNING
    Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 1][x3650m2n4-hs.clusters.com]: >> [31335] >> stdout: >> 2017-01-19 08:47:50.576520: step 0 (global_step 0), loss = 4.68 (27.6 examples/sec; 4.638 sec/batch) {}
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> 2017-01-19 08:47:53.502266: step 0 (global_step 0), loss = 4.68 (20.1 examples/sec; 6.372 sec/batch) {}
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 1][x3650m2n4-hs.clusters.com]: >> [31335] >> stdout: >> 2017-01-19 08:47:53.653128: step 10 (global_step 10), loss = 4.63 (413.5 examples/sec; 0.310 sec/batch) {}
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 1][x3650m2n4-hs.clusters.com]: >> [31335] >> stdout: >> 2017-01-19 08:47:56.778850: step 20 (global_step 29), loss = 4.61 (426.0 examples/sec; 0.300 sec/batch) {}
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> 2017-01-19 08:47:56.818441: step 10 (global_step 30), loss = 4.61 (400.7 examples/sec; 0.319 sec/batch) {}
    ...
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> 2017-01-19 08:50:23.963482: step 470 (global_step 966), loss = 3.02 (245.9 examples/sec; 0.520 sec/batch) {}
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 1][x3650m2n4-hs.clusters.com]: >> [31335] >> stdout: >> + echo finish {}
    [D]: handle msg: >> {'category': 'finish_cmd', 'src': 'executor', 'returncode': 0, 'partition_index': 1, 'target': 'driver', 'error': [], 'output': []} {}
    [D]: calling "handle_finish_cmd" {'cnt': 0, 'returncode': 0, 'partition_index': 1}
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> 2017-01-19 08:50:27.282788: step 480 (global_step 980), loss = 2.58 (417.3 examples/sec; 0.307 sec/batch) {}
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> 2017-01-19 08:50:30.347789: step 490 (global_step 990), loss = 2.45 (411.6 examples/sec; 0.311 sec/batch) {}
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (2 active, 0 complete)
    [D]: remote_msg: [ 0][x3650m2n5-hs.clusters.com]: >> [16882] >> stdout: >> + echo finish {}
    [D]: handle msg: >> {'category': 'finish_cmd', 'src': 'executor', 'returncode': 0, 'partition_index': 0, 'target': 'driver', 'error': [], 'output': []} {}
    [D]: calling "handle_finish_cmd" {'cnt': 1, 'returncode': 0, 'partition_index': 0}
    [D]: calling "stop_cn_tasks" {}
    [I]: publish msg: >> {'category': 'stop_cn_task', 'src': 'driver', 'partition_index': 0, 'target': 'executor'}
    [I]: publish msg: >> {'category': 'stop_cn_task', 'src': 'driver', 'partition_index': 1, 'target': 'executor'}
    17/01/19 08:50:34 INFO TaskSetManager: Finished task 0.0 in stage 0.0 (TID 0) in 176569 ms on x3650m2n5-hs.clusters.com (1/2)
    Job 0 status:  RUNNING
        Stage 0: 2 tasks total (1 active, 1 complete)
    17/01/19 08:50:34 INFO TaskSetManager: Finished task 1.0 in stage 0.0 (TID 1) in 176585 ms on x3650m2n4-hs.clusters.com (2/2)
    17/01/19 08:50:34 INFO DAGScheduler: ResultStage 0 (collect at /gpfs/dlfs1/user_home/fuzhiwen/workspace/bluemind/tools/spark_tf_launcher/./launcher.py:928) finished in 176.605 s
    17/01/19 08:50:34 INFO YarnScheduler: Removed TaskSet 0.0, whose tasks have all completed, from pool
    17/01/19 08:50:34 INFO DAGScheduler: Job 0 finished: collect at /gpfs/dlfs1/user_home/fuzhiwen/workspace/bluemind/tools/spark_tf_launcher/./launcher.py:928, took 176.819909 s
    Job results are: [[0, 0], [1, 1]]


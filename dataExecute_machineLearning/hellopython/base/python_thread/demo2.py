from threading import Timer
import threading
import time
import sys

__author__ = 'sss'
class CountdownTask(threading.Thread):
    def __init__(self):
        super(CountdownTask, self).__init__()
        self._running = True

    def terminate(self):
        self._running = False

    def run(self):
        print("begin thread......")
        while self._running:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1)
        print("end threads......")


if __name__ == '__main__':
    ct = CountdownTask()
    ct.start()
    print('start')
    time.sleep(2)
    ct.terminate()
    time.sleep(1)
    print('over')



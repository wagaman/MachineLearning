from threading import Timer
import threading
import time
import sys

__author__ = 'sss'
def worker(arg1, arg2):
    while True:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':
    t = threading._start_new_thread(worker, ("Thread", 1))

    try:
        threading.main_thread()._stop()
    except Exception as e:
        pass

    print('start')
    time.sleep(5)
    print('over')



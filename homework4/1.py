import time
import random
import threading


lock = threading.Lock()


def worker(file: object, *args):
    with lock:
        file.write(threading.currentThread().name + ': ' + 'started.\n')
        time.sleep(random.random() * 5)
        file.write(threading.currentThread().name + ': ' + 'done.\n')


if __name__ == '__main__':
    file = open('test.txt', 'a')
    for _ in range(10):
        my_thread = threading.Thread(target=worker, args=(file,))
        my_thread.start()

import threading
import time
lock =threading.Lock()
def even_odd():
    for num in range(1, 11):
        lock.acquire()
        if threading.current_thread().name == 'even' and num % 2 == 0:
            time.sleep(2)
            # with lock:
            print(threading.current_thread().name, ".....", num)
        elif threading.current_thread().name == 'odd' and num % 2 != 0:
            time.sleep(2)
            # with lock:
            print(threading.current_thread().name, ".....", num)
        lock.release()
thread1 = threading.Thread(target=even_odd, name='even')
thread2 = threading.Thread(target=even_odd, name='odd')
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("executed!")



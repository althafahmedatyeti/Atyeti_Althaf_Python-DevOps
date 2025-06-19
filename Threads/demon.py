import threading
import time
def task():
    while True:
        print("Running...")
        time.sleep(1)
t = threading.Thread(target=task)
t.daemon = True
t.start()
time.sleep(1)
print("Main thread done")
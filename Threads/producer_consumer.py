import threading
import time
buffer = []
condition = threading.Condition()
def producer():
    for i in range(11):
        with condition:
            buffer.append(i)
            print(i, "no of elements")
            condition.notify()
        time.sleep(0.2)
    print("All elements are added")
def consumer():
    while True:
        with condition:
            while not buffer:
                condition.wait()
            item = buffer.pop(0)
            print(f"Item taken {item}")
            condition.notify()
        time.sleep(0.5)
pro = threading.Thread(target=producer)
con = threading.Thread(target=consumer)
pro.start()
con.start()
pro.join()
con.join()



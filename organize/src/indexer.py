from raw_manager import raw_manager
from data_transform import data_transform
import time
import atexit
import threading

data_indexing_status = True
quitting_signal = False

def start_indexing():
    rm = raw_manager("organize\\src\\database\\raw_test.db")
    dt = data_transform("organize\\src\\database\\data_test.db", "organize\\src\\database\\raw_test.db")
    while data_indexing_status:
        fetched_data = rm.fetch_raw()
        if fetched_data is not None:
            print(fetched_data[0])
            dt.update_web(fetched_data[0], fetched_data[1])
        else:
            print("No more data to index")
            time.sleep(5)

    event.set()

    while quitting_signal:
        print("Quitting signal received")
        del rm
        del dt
        return

def my_exit_function():
    global quitting_signal
    quitting_signal = True
    # wait until start_indexing() is finished
    event.wait()

# main function
if __name__ == '__main__':
    event = threading.Event()
    atexit.register(my_exit_function)
    t = threading.Thread(target=start_indexing)
    t.start()

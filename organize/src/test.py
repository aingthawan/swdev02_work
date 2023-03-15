import time
import threading

paused = False

def pingpong():
    while True:
        if not paused:
            print("pingpong")
            time.sleep(1)

def handle_command():
    global paused
    while True:
        command = input("Get command:")
        if command == "p":
            paused = True
            print("pingpong paused")
            time.sleep(5)  # sleep for 5 seconds
        elif command == "c":
            paused = False
            print("pingpong continued")
        else:
            print("invalid command")

if __name__ == "__main__":
    # start pingpong
    threading.Thread(target=pingpong).start()
    
    print("pingpong started")
    
    # start command handler
    threading.Thread(target=handle_command).start()

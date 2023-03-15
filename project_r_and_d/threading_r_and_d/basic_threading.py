#!/usr/bin/env python
# coding: utf-8

import threading
import time


class Job(threading.Thread):

    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait() # return immediately when it is True, block until the internal flag is True when it is False
            print(time.time())
            time.sleep(1)

    def pause(self):
        self.__flag.clear() # Set to False to block the thread

    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking

    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False

# make a main function for receiving user input, p for pause, c for continue, s for stop
if __name__ == "__main__":
    a = Job()
    a.start()
    while True:
        user_input = input("Enter 'p' to pause or 'c' to continue or 's' to stop: ")
        if user_input == 'p':
            # Stop the go_scrape thread
            print("Pausing scraping...")
            a.pause()
        elif user_input == 'c':
            # Resume the go_scrape thread
            print("Resuming scraping...")
            a.resume()
        elif user_input == 's':
            # Stop the go_scrape thread
            print("Stopping scraping...")
            a.stop()
            break
        # other than p, c, s, print invalid input
        else:
            print("Invalid input")
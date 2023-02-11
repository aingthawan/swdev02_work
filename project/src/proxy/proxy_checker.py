# Reference : https://www.youtube.com/watch?v=FbtCl9jJyyc&t=417s
# Proxy List : https://free-proxy-list.net/

import threading
import queue
import requests


q = queue.Queue()
valid_proxies = []

with open('project\src\proxy\proxy_list.txt', 'r') as f:
    proxies = f.read().split("\n")

    for proxy in proxies:
        # print(proxy)
        q.put(proxy)

def check_proxy():
    global q
    while not q.empty():
        proxy = q.get()
        try:
            response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy})
        except:
            continue

        if response.status_code == 200:
            print(proxy)

for _ in range(10):
    threading.Thread(target=check_proxy).start()

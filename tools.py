import random
from datetime import datetime
import requests

def save_html_file(src, name):
    with open(name, "w", encoding="utf-8") as file:
        file.write(src)

def load_html_file(name):
    with open(name, "r", encoding="utf-8") as file:
        return file.read()

def load_proxies(url="https://proxoid.net/api/getProxy?key=176856a0dcf70b3f79eae945fe18b021&countries=all&types=https&level=anonymous&speed=500&count=0", file_name="proxies_list.txt"):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(f"{int(datetime.now().timestamp())}\n")
        file.write(requests.get(url=url).text)

def get_proxy(file_name="proxies_list.txt"):
    with open(file_name, "r", encoding="utf-8") as file:
        proxies = file.readlines()[1:]
        print(random.choice(proxies))

if __name__ == "__main__":
    get_proxy()
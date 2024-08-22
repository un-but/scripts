import random, requests, os
import aiohttp
from fake_useragent import UserAgent

# def get_proxy(url="https://proxoid.net/api/getProxy?key=176856a0dcf70b3f79eae945fe18b021&countries=all&types=https&level=anonymous&speed=500&count=0"):
#     proxies = requests.get(url=url).text.splitlines()
#     return {"https": random.choice(proxies)}

# for i in range(1, 100):
#     url = "https://obsproject.com/ru"
#     headers = {
#         "user-agent": UserAgent().random
#     }
#     if not os.path.exists("proxies.txt"):
#         with open("proxies.txt", "w") as file:
#             req = requests.get(url="https://proxoid.net/api/getProxy?key=176856a0dcf70b3f79eae945fe18b021&countries=all&types=https&level=anonymous&speed=500&count=0").text
#             file.write(req)
#             proxies = req.splitlines()
#     else:
#         with open("proxies.txt", "r") as file:
#             proxies = file.readlines()
#     try:
#         ip = {"https": random.choice(proxies)}
#         src = requests.get(url=url, headers=headers, proxies=ip, verify=False).text
#         print(f"страница успешно получена с ip {ip}")
#     except requests.exceptions.ProxyError:
#         print("прокси не работает")
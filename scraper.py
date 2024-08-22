import requests
import feedparser
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import sqlite3
import json
import os
import time
import tools


def add_order_to_db(url, name, date, description, price, views, responses):
    con = sqlite3.connect("tasks_list.db")
    cur = con.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY,
                url TEXT,
                name TEXT,
                date TEXT,
                description TEXT,
                price TEXT,
                views TEXT,
                responses TEXT
                )
                ''')
    cur.execute("INSERT INTO Tasks (url, name, date, description, price, views, responses) VALUES (?, ?, ?, ?, ?, ?, ?)", (url, name, date, description, price, views, responses))
    con.commit()
    con.close()


def get_data_from_habr():
    p = 1
    while True:
        url = f"https://freelance.habr.com/tasks?categories=development_bots&page={p}"
        headers = {
            "user-agent": UserAgent().random
        }

        src = requests.get(url=url, headers=headers).text
        soup = BeautifulSoup(src, "lxml")
        
        if soup.find(class_="empty-block__title"):
            break

        orders = soup.find_all(class_="task__title")
        for order in orders:
            order_url = "https://freelance.habr.com" + order.find("a")['href']
            order_page = requests.get(url=order_url, headers=headers).text
            order_soup = BeautifulSoup(order_page, "lxml")

            order_name = order_soup.find(class_="task__title").contents[0].text.strip() + " " + order_soup.find(class_="task__title-nowrap").find("span").text.strip()
            order_date = order_soup.find(class_="task__meta").contents[0].text.replace("•", "").strip()
            order_description = order_soup.find(class_="task__description").get_text("\n").strip()
            order_price = order_soup.find(class_="task__finance").find("span").text.strip()
            order_views = order_soup.find(class_="task__meta").contents[1].text + " " + order_soup.find(class_="task__meta").contents[2].text.replace("•", "").strip()
            order_responses = order_soup.find(class_="task__meta").contents[3].text + " " + order_soup.find(class_="task__meta").contents[4].text.replace("•", "").strip()
            print(f"{order_url}\n{order_name}\n{order_price}\t\t{order_date}\t\t{order_views}\t{order_responses}\n{order_description}\n\n\n\n")
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~ лог в консоль ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            # add_task_to_db(task_url, task_name, task_date, task_description, task_price, task_views, task_responses)
        
        p += 1

def get_data_from_kwork():
    session = requests.Session()
    p = 1


    if not os.path.exists("cookies.json"):
        login_url = "https://kwork.ru/api/user/login"
        login_data = {
            "l_username": "unbut",
            "l_password": "uc9-8YG-S3f-eny"
        }
        login_request = session.post(url=login_url, data=login_data, headers={"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36"})
        # print([{"domain": key.domain, "name": key.name, "path": key.path, "value": key.value} for key in session.cookies])
        # return
        with open("cookies.json", "w") as file:
            json.dump(session, file, indent=4)
    else:
        with open("cookies.json", "r") as file:
            cookies_dict = json.load(file)
        for cookies in cookies_dict:
            session.cookies.set(**cookies)

    url = "https://kwork.ru/projects?a=1&fc=41&attr=211&page={p}"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36" #UserAgent().random
    }

    src = session.get(url=url, headers=headers, allow_redirects=False).text
    with open("kwork.html", "w") as file:
        file.write(src)

    # r = requests.get('https://kwork.ru/projects?keyword=парсинг&page=10', allow_redirects=False).text
    # print("Redirecting to <a href=\"/projects?keyword=%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3\">/projects?keyword=%D0%BF%D0%B0%D1%80%D1%81%D0%B8%D0%BD%D0%B3</a>" in r)
    # while True:
    #     url = "https://kwork.ru/projects?keyword=парсинг&page={p}"
    #     headers = {
    #         "user-agent": UserAgent().random
    #     }

    #     src = session.get(url=url, headers=headers, allow_redirects=False).text
    #     soup = BeautifulSoup(src, "lxml")
    
    #     if "Redirecting to" in src:
    #         print("эщкере")
    #         break
        
    #     print(f"парсинг страницы номер {p} завершен")
    #     p += 1
    #     time.sleep(5)
    #     if p > 5:
    #         print("скрипт работает неправильно")
    #         return

def get_data_from_fl():
    p = 1
    src = feedparser.parse("https://www.fl.ru/rss/all.xml?subcategory=172&category=3")
    # tools.save_html_file(str(src), "index.html")
    print(src)


if __name__ == "__main__":
    # get_data_from_habr()
    get_data_from_kwork()
    # get_data_from_fl()

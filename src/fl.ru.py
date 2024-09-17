"""Functions for getting all orders from FL.ru in selected categories from RSS channel."""

import asyncio

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# from database import add_order_to_db


# https://www.fl.ru/rss/all.xml?subcategory=280&category=5 - парсинг данных
# https://www.fl.ru/rss/all.xml?subcategory=279&category=5 - разработка чат-ботов

async def get_data_from_fl() -> None:
    """Main function, adding info from all pages to database.""" # Надо исправить
    async_tasks = []
    async with aiohttp.ClientSession() as session:
        base_url = "https://www.fl.ru/projects/category/programmirovanie/parsing-dannyih"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "user-agent": UserAgent().chrome
        }
        page = 1
        while True:
            page_url = f"{base_url}/page-{page}" if page > 1 else base_url
            async with session.get(url=page_url, headers=headers) as res:
                src = await res.text()
            if page == 3:
                with open("test/test.html", "w", encoding="utf-8") as file:
                    file.write(src)
            soup = BeautifulSoup(src, "lxml")

            orders = soup.find_all("h2", class_="b-post__title")
            for order in orders:
                order_url = f"https://www.fl.ru{order.find("a")["href"]}"
                async_tasks.append(
                    asyncio.create_task(get_data_from_fl_order_page(order_url, session))
                )

            page += 1
            if "b-pager__next" not in src:
                break


        await asyncio.gather(*async_tasks)

async def get_data_from_fl_order_page(order_url: str, session: aiohttp.ClientSession) -> None:
    headers = {"user-agent": UserAgent().random}

    async with session.get(url=order_url, headers=headers, timeout=1000) as res:
        src = await res.text()
    
    order_id = order_url.split("/")[-2]
    print(order_id)
    order_soup = BeautifulSoup(src, "lxml")
    order_name = order_soup.find("h1", id=f"prj_name_{order_id}").get_text(" ", strip=True)
    order_description = order_soup.find("div", id=f"projectp{order_id}").get_text("\n", strip=True)
    order_price = order_soup.find(class_=f"task__finance").get_text(strip=True)

    order_meta = order_soup.find(class_="task__meta").get_text(" ", strip=True).split("\n • ")
    order_date = f"{order_meta[0]}/нет информации"
    order_responses = order_meta[1]


    # add_order_to_db(
    #     order_url,
    #     order_name,
    #     order_date,
    #     order_description,
    #     order_price,
    #     order_responses
    # )
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ лог в консоль ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print(
        f"{order_url}\n{order_name}\n"
        f"{order_price}\t\t{order_date}\t\t{order_responses}\n"
        f"{order_description}\n\n\n\n"
    )

if __name__ == "__main__":
    asyncio.run(get_data_from_fl())

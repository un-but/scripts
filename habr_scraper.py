"""Functions for getting all orders in search request."""

import asyncio

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# from database import add_order_to_db


async def get_data_from_habr() -> None:
    """Main function, adding info from all pages to database."""
    p = 1
    async with aiohttp.ClientSession() as session:
        while True:
            url = f"https://freelance.habr.com/tasks?categories=development_bots&page={p}"
            headers = {"user-agent": UserAgent().random}

            # async with aiohttp.ClientSession() as session:
            async with session.get(url=url, headers=headers) as res:
                src = await res.text()

            soup = BeautifulSoup(src, "lxml")

            if soup.find(class_="empty-block__title"):
                break

            orders = soup.find_all(class_="task__title")
            async_tasks = []
            for order in orders:
                order_url = "https://freelance.habr.com" + order.find("a")["href"]
                async_tasks.append(
                    asyncio.create_task(get_data_from_habr_order_page(order_url, session))
                )

            p += 1

    await asyncio.gather(*async_tasks)


async def get_data_from_habr_order_page(order_url: str, session: aiohttp.ClientSession) -> None:
    """Functions for getting info from one page"""
    headers = {"user-agent": UserAgent().random}

    async with session.get(url=order_url, headers=headers, timeout=1000) as res:
        src = await res.text()

    order_soup = BeautifulSoup(src, "lxml")
    order_name = (
        order_soup.find(class_="task__title").contents[0].text.strip()
        + " "
        + order_soup.find(class_="task__title-nowrap").find("span").text.strip()
    )
    order_date = (
        order_soup.find(class_="task__meta").contents[0].text.replace("•", "").strip()
    )
    order_description = (
        order_soup.find(class_="task__description").get_text("\n").strip()
    )
    order_price = order_soup.find(class_="task__finance").find("span").text.strip()
    order_views = (
        order_soup.find(class_="task__meta").contents[1].text
        + " "
        + order_soup.find(class_="task__meta").contents[2].text.replace("•", "").strip()
    )
    order_responses = (
        order_soup.find(class_="task__meta").contents[3].text
        + " "
        + order_soup.find(class_="task__meta").contents[4].text.replace("•", "").strip()
    )

    # add_order_to_db(
    #     order_url,
    #     order_name,
    #     order_date,
    #     order_description,
    #     order_price,
    #     order_views,
    #     order_responses,
    # )
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~ лог в консоль ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    print(
        f"{order_url}\n{order_name}\n"
        f"{order_price}\t\t{order_date}\t\t{order_views}\t{order_responses}\n"
        f"{order_description}\n\n\n\n"
    )



if __name__ == "__main__":
    asyncio.run(get_data_from_habr())

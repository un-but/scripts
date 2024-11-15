import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from common.tools import create_driver, save_array_to_csv


def get_data_from_kwork(url: str = "https://kwork.ru/projects?c=41&attr=211") -> None:
    result = []
    driver = create_driver(mode="headless")

    current_page = 1
    last_page = 1

    while current_page <= last_page:
        page_url = f"{url}&page={current_page}"
        driver.get(page_url)
        orders = driver.find_elements(By.CLASS_NAME, "want-card")

        for order in orders:
            order_header = order.find_element(By.CLASS_NAME, "wants-card__header-title")
            order_url = order_header.find_element(By.TAG_NAME, "a").get_attribute("href")
            order_name = order_header.text.strip()

            order_price = order.find_element(By.CLASS_NAME, "wants-card__price").find_element(By.CLASS_NAME, "d-inline").text.strip()

            description = order.find_element(By.CLASS_NAME, "wants-card__description-text")
            try:
                description.find_element(By.CLASS_NAME, "kw-link-dashed").click()
                time.sleep(0.5)
                order_description = description.find_elements(By.CLASS_NAME, "d-inline")[1].text
            except NoSuchElementException:
                order_description = description.text

            order_info = order.find_element(By.CLASS_NAME, "want-card__informers-row").find_elements(By.TAG_NAME, "span")
            order_date = order_info[0].text.strip()
            order_responses = f"{order_info[1].text.split(": ")[1]} откликов"

            result.append((
                order_url,
                order_name,
                order_date,
                order_description,
                order_price,
                order_responses,
            ))

        if current_page == 1:
            last_page = int(driver.find_elements(By.CLASS_NAME, "pagination__item")[-2].text)

        current_page += 1
        time.sleep(3)

    save_array_to_csv(result, "kwork.ru-output.csv")



if __name__ == "__main__":
    get_data_from_kwork()

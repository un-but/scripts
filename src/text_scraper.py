from __future__ import annotations

import re
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

from common.tools import create_driver


def collect_text(driver: Chrome, pages: list[str], sleep: int = 0) -> dict:
    result = []

    for page in pages:
        driver.get(page)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        if sleep:
            time.sleep(sleep)

        text = driver.find_element(By.XPATH, "/html/body").text
        words_number = len(re.findall(r"\b\S+\b", text))

        try:
            urls = [el.get_attribute("href") for el in driver.find_elements(By.XPATH, "//a")]
        except NoSuchElementException:
            urls = []

        result.append({
            "page": page,
            "text": text,
            "words_number": words_number,
            "urls": urls,
        })


    return result



# Этот пример использования будет выполнен при запуске этого файла
if __name__ == "__main__":
    print(collect_text(create_driver(mode="headless", stealth_mode=True), ["https://google.com", "https://kwork.ru/user/unbut"], 3))

"""Frequently used functions"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_driver(mode="headless") -> webdriver.Chrome:
    """Create chrome driver object.

    Args:
        mode (str, optional): "headless" for server or "desktop" for debug. Defaults to "headless".

    Returns:
        webdriver.Chrome
    """
    options = Options()

    if mode == "headless":
        options_list = [
            "--no-sandbox", 
            "--disable-gpu", 
            "--disable-dev-shm-usage", 
            "--headless", 
            "--ignore-certificate-errors-spki-list", 
            "--log-level=3",
            "--start-maximized"
        ]
        # options.add_argument('--start-maximized')
    elif mode == "desktop":
        # Добавить функции для отображения браузера
        pass

    for option in options_list:
        options.add_argument(option)

    return webdriver.Chrome(options=options)

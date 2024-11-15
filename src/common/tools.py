"""Frequently used functions."""
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def create_driver(mode: str = "desktop", stealth_mode: bool = False) -> Chrome:
    """Создает объект драйвера Chrome.

    Args:
        mode (str, optional): "headless" для запуска на сервере и "desktop" или без указания для отладки с графическим интерфейсом. По умолчанию desktop.
        stealth (bool, optional): значение указывает на необходимость скрывать, что это программа и вести себя как обычный пользователь.

    Returns:
        Chrome: объект драйвера Chrome

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
            "--disable-blink-features=AutomationControlled",
            "--disable-software-rasterizer",
            "--start-maximized",
        ]
    elif mode == "desktop":
        options_list = [
            "--ignore-certificate-errors-spki-list",
            "--log-level=3",
            "--disable-blink-features=AutomationControlled",
            "--start-maximized",
        ]

    for option in options_list:
        options.add_argument(option)

    driver = Chrome(options=options)

    if stealth_mode:
        from selenium_stealth import stealth

        stealth(driver=driver,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36",
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True,
        )

        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """})

    return driver


def save_array_to_csv(array: list, filename: str) -> None:
    import csv

    with open(f"files/{filename}", mode="w", newline="", encoding="utf-8-sig") as file:
        csv_writer = csv.writer(file, delimiter =";")
        csv_writer.writerows(array)

import csv
import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from common.tools import create_driver

driver = create_driver(mode="desktop")
result = []

with open(file="files/iswork.ru-input.csv", encoding="utf-8") as file:
    inns = [line.replace("\n", "").strip() for line in file]

for inn in inns:
    driver.get("https://iswork.ru/")

    driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul[1]/li/form/div").click()
    driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul[1]/li/form/div/input").send_keys(inn)
    driver.find_element(By.XPATH, "/html/body/nav/div/div[2]/ul[1]/li/form/button").click()

    time.sleep(1)
    try:
        driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[1]/div/div[3]/ul/p/a")
    except NoSuchElementException:
        name = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td/span").text

        try:
            income = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[3]/th[2]").text
            expenditure = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[3]/th[3]").text
            profit = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[2]/div[3]/table/tbody/tr[3]/th[4]").text
        except NoSuchElementException:
            income = "не найдено"
            expenditure = "не найдено"
            profit = "не найдено"
        okved = driver.find_element(By.XPATH, "/html/body/div[4]/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[10]/td[1]").text
        logging.info(inn, name, income, expenditure, profit, okved)
        result.append([inn, name, income, expenditure, profit, okved])
    else:
        result.append([inn, "страница отсутствует"])


with open("files/iswork.ru-output.csv", mode="w", newline="") as file:
    csv_writer = csv.writer(file, delimiter =";")
    csv_writer.writerows(result)

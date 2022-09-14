from time import sleep
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import requests

MAIN_URL = "https://teremok.ru/"
MENU_URL = "https://teremok.ru/menu/category/novinki/"
RESULT = []


def collect_urls_menu() -> List:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(1920, 1080)
    driver.get(MENU_URL)

    sleep(5)

    ul_class = driver.find_elements(By.CSS_SELECTOR, "a.b-catalog__nav-link")
    menu_list = []

    for i in ul_class:
        menu_list.append(f'https://teremok.ru/menu/category/{i.get_attribute("class").split("--")[1].split(" ")[0]}/')

    return menu_list


def collect_urls_positions(menu_list) -> List:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.set_window_size(768, 1024)

    items = []
    for li_menu in menu_list:
        driver.get(li_menu)
        sleep(5)

        items_list = driver.find_elements(By.CSS_SELECTOR, "li.b-catalog__list-item")

        for i in items_list:
            items.append(i.find_element(By.TAG_NAME, 'a').get_attribute('href'))

    return items


def take_data_items(items):
    for item in items:
        response = requests.get(item)

        soup = BeautifulSoup(response.text, "html.parser")
        attributes = {}
        img_url = f'{MAIN_URL}{soup.find_all("picture", class_="b-detail-product__img")[0].contents[5].attrs["src"]}'
        name = soup.find("h1").text
        product_url = item
        attributes.update({'name': name, 'product_url': product_url, 'img_url': img_url})

        rows = soup.find_all("div", class_="b-detail-product__info-row")

        for k in rows[1:]:
            product_property = k.contents[1].text
            product_value = k.contents[5].text
            attributes.update({product_property: product_value})

        RESULT.append(attributes)


def create_excel(RESULT):
    df = pd.DataFrame(RESULT)
    df.to_excel('teremok.xlsx')


if __name__ == '__main__':
    take_data_items(collect_urls_positions(collect_urls_menu()))
    create_excel(RESULT)

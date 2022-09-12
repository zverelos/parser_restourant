import json
import pandas as pd
from bs4 import BeautifulSoup
from typing import List
import requests

MAIN_URL = "http://eastoria.ru"
SITE_MAP_URL = "http://eastoria.ru/sitemap.xml"
RESULT = []


def parse_sitemap() -> List:
    response = requests.get(SITE_MAP_URL)

    soup = BeautifulSoup(response.text, "lxml-xml")

    product_list = []
    for _ in soup.find_all("loc"):
        if 'product' in _.text:
            product_list.append(_.text)

    return product_list


def take_data(url):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find("h1").text
    if soup.find_all("a", class_="highslide"):
        img_url = f'{MAIN_URL}{soup.find_all("a", class_="highslide")[0].attrs["href"]}'
    else:
        img_url = "None"
    product_price = soup.find_all("div", class_="product-price")[0].text.strip()

    if soup.find_all("div", class_="shop-tab"):
        description = soup.find_all("div", class_="shop-tab")[0].text.strip()
    else:
        description = "None"

    category = [_.text for _ in soup.find_all("div", class_="site-path")]

    result = {}
    result.update(name=name, img_url=img_url, product_price=product_price, description=description, category=category)
    RESULT.append(result)


def create_excel(RESULT):
    df = pd.DataFrame(RESULT)
    df.to_excel("output.xlsx")


if __name__ == '__main__':
    for i in parse_sitemap():
        take_data(i)
    with open("to_load1.json", "a", encoding="utf-8") as file:
        json.dump(RESULT, file, indent=2, ensure_ascii=False)
    create_excel(RESULT)
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


MAIN_URL = "https://teremok.ru/"
MENU_URL = "https://teremok.ru/menu/category/novinki/"


def collect_urls():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(MENU_URL)


if __name__ == '__main__':
    collect_urls()
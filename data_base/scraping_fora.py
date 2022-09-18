from data_base import db_sqlite
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import random
import time


def scrap_fora():
    print('Scraping Fora started')
    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
    option.add_argument("--disable-notifications")
    option.add_argument('--disable-blink-features=AutomationControlled')

    url = 'https://fora.ua/promotions'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.maximize_window()  # For maximizing window
    driver.get(url)

    first_button = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/button')
    first_button.click()
    time.sleep(random.triangular(1, 2))

    while True:
        time.sleep(random.triangular(1, 2))
        try:
            download_button = driver.find_element(By.XPATH, '//*[text()="Завантажити ще"]')
            download_button.click()
        except:
            break

    for i in range(1, 5000):
        try:
            core_path = f'//*[@id="__next"]/div/div[2]/div[3]/div[2]/div[2]/div/div/div[{i}]'

            item = driver.find_element(By.XPATH, core_path)
            name = item.find_element(By.XPATH, f'{core_path}/a/div[2]/div[1]/h2').text
            size = item.find_element(By.XPATH, f'{core_path}/a/div[2]/div[1]/div').text
            old_price = item.find_element(By.XPATH, f'{core_path}/a/div[2]/div[2]/div[1]/div[1]').text.replace(',', '.')
            new_price = item.find_element(By.XPATH, f'{core_path}/a/div[2]/div[2]/div[1]/div[2]').text.replace(',', '.')
            url_img = item.find_element(By.XPATH, f'{core_path}/a/div[1]/img').get_property('src')

            db_sqlite.SqlDb().add_product(
                                          'Fora',
                                          f'{name}, {size}',
                                          float(old_price),
                                          float(new_price),
                                          int(100 - ((float(new_price) / float(old_price)) * 100)),
                                          url_img)

        except:
            break

    print('Scraping Fora ended')

from data_base import db_sqlite
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import random
import time


def scrap_silpo():
    print('Scraping Silpo started')
    option = webdriver.ChromeOptions()
    option.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                        '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36')
    option.add_argument("--disable-notifications")
    option.add_argument('--disable-blink-features=AutomationControlled')

    url = 'https://silpo.ua/offers'
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    driver.maximize_window()  # For maximizing window
    driver.get(url)

    time.sleep(5)

    for i in range(0, 5000000, 5000):        # скролю сайт вниз до конца
        time.sleep(random.triangular(0, 1))
        try:
            driver.execute_script(f"window.scrollTo({i}, {i+5000});")
        except:
            break

    for i in range(1, 5000):
        core_path = f'//*[@id="l-body"]/div[1]/div[2]/div/div/ul/li[{i}]'

        try:          # Когда товары заканчиваются, остановить цикл
            item = driver.find_element(By.XPATH, core_path)
            try:      # не все елементы core_path являются товарами, по этому в них нет нужных елементов
                name = item.find_element(By.XPATH, f'{core_path}/div/a[2]/div[1]').text
                old_price = item.find_element(By.XPATH, f'{core_path}/div/div[1]/div/div[2]/div[2]').text
                new_price_part_1 = item.find_element(By.XPATH, f'{core_path}/div/div[1]/div/div[1]').text
                new_price_part_2 = item.find_element(By.XPATH, f'{core_path}/div/div[1]/div/div[2]/div[1]').text
                new_price = f'{new_price_part_1}.{new_price_part_2}'
                url_img = item.find_element(By.XPATH, f'{core_path}/div/a[1]/img').get_property('src')

                db_sqlite.SqlDb().add_product(
                                              'Silpo',
                                              f'{name}',
                                              float(old_price),
                                              float(new_price),
                                              int(100 - ((float(new_price) / float(old_price)) * 100)),
                                              url_img)
            except:
                continue
        except:
            break
    print('Scraping Silpo ended')
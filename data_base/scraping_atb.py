from bs4 import BeautifulSoup
import requests, lxml
from data_base import db_sqlite


def scrap_atb():
    print('Scraping ATB started')
    headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    url = 'https://www.atbmarket.com/uk/promo/akciya-ekonomiya?_token=1mAzchkoNNzqm1ePtf5nxV7yoqSH00Zfg6y7bsEc&city_id=6'
    url_atb = 'https://www.atbmarket.com'   # для ссылок на картинки
    response = requests.get(url, headers=headers)
    pars = BeautifulSoup(response.text, 'lxml')

    for item in pars.find_all('div', class_='one-action-item'):
        name = item.find('div', class_='one-action-tit').text.strip()
        # старый ценник с проверкой, потому что в разделе скидок, есть товары без скидок

        try:
            old_price = item.find('div', class_='one-action-was-price').text.strip()
        except:
            old_price = '-1'

        new_price = item.find('div', class_='one-action-price-now').text.strip().replace(' ', '.')
        url_img = f"{url_atb}{item.find('div', class_='one-action-thumb').find('img').get('src')}"

        if old_price != '-1':
            db_sqlite.SqlDb().add_product(
                                          'ATB',
                                          name,
                                          float(old_price),
                                          float(new_price),
                                          int(100 - ((float(new_price) / float(old_price)) * 100)),
                                          url_img)

        print('Scraping ATB ended')

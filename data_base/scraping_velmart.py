from bs4 import BeautifulSoup
import requests, lxml
from data_base import db_sqlite


def scrap_velmart():
    print('Scraping Velmart started')
    headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    url = 'https://velmart.ua/product-of-week/'
    response = requests.get(url, headers=headers)
    pars = BeautifulSoup(response.text, 'lxml')

    cls = 'jet-woo-products__item jet-woo-builder-product col-desk-3 col-tab-2'
    for item in pars.find_all('div', class_=cls):
        name = str(item.find('h5', class_='jet-woo-product-title').find('a')).split('>')[1].split('<')[0]
        url_img = item.find('div', class_='jet-woo-product-thumbnail').find('img').get('src')

        db_sqlite.SqlDb().add_product(
                                      'Velmart',
                                      name,
                                      0,
                                      0,
                                      0,
                                      url_img)

    print('Scraping Velmart ended')

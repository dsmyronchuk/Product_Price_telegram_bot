import requests, lxml
from bs4 import BeautifulSoup
from data_base import db_sqlite


def scrap_novus():
    headers = {'UserAgent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0'}

    for page in range(1, 1000):
        url = f'https://novus.ua/sales.html?p={page}'
        response = requests.get(url, headers=headers)
        pars = BeautifulSoup(response.text, 'lxml')
        print(f'Novus page {page}')
        button_stop = False

        for item in pars.find_all('li', class_='item product product-item'):

            name = item.find('a', class_='product-item-link').text.replace(' ', '').replace('\n', '').lower()
            try:
                old_price_int = item.find('span', class_='old-price').find('span', class_='integer').text
                old_price_float = item.find('span', class_='old-price').find('span', class_='decimal').text.replace(' ', '')
                new_price_int = item.find_all('span', class_='price-container price-final_price tax weee')[1].find('span', class_='integer').text
                new_price_float = item.find_all('span', class_='price-container price-final_price tax weee')[1].find('span', class_='decimal').text.replace(' ', '')
                url_img = item.find('img', class_='product-image-photo lazy lazy-loading').get('src')

                if url_img == 'https://novus.ua/media/catalog/product/placeholder/default/270_270.jpg':
                    button_stop = True
                    break

                full_old_price = float(f'{old_price_int}.{old_price_float}')
                full_new_price = float(f'{new_price_int}.{new_price_float}')
                discount = 100 - ((full_new_price / full_old_price) * 100)

                db_sqlite.SqlDb().add_product(
                                              'Novus',
                                              name,
                                              full_old_price,
                                              full_new_price,
                                              int(discount),
                                              url_img)

            except:
                continue

        if button_stop is True:
            break
    print('Scraping Novus ended')


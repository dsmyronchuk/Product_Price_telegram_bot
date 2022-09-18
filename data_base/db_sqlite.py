import sqlite3 as sql


class SqlDb:
    def __init__(self):
        self.name_db = 'data_base/markets.db'
        self.connect = sql.connect(self.name_db)
        self.cur = self.connect.cursor()

    def reset_db(self):
        # Перезапись таблицы на актуальную
        self.connect.execute('DROP TABLE IF EXISTS product;')
        self.connect.execute('CREATE TABLE product ('
                             'market TEXT,  '
                             'product_type TEXT, '
                             'old_price FLOAT, '
                             'new_price FLOAT, '
                             'discount INTEGER, '
                             'url_ing TEXT);')
        self.connect.commit()

    def add_product(self, market, name, old_price, new_price, discount, url_img):
        data = [market, name.lower(), old_price, new_price, discount, url_img]

        self.connect.execute('INSERT INTO product VALUES (?, ?, ?, ?, ?, ?)', data)
        self.connect.commit()

    def get_input_product_from_sql(self, product_name, market_list):
        if len(market_list) == 1:
            market_list = f"('{market_list[0]}')"
        else:
            market_list = tuple(market_list)

        query = self.connect.execute(f'''SELECT * 
                                         FROM product 
                                         WHERE product_type like '%{product_name.lower()}%' 
                                         and market in {market_list}
                                         ORDER BY market;''')
        data_lst = query.fetchall()
        new_lst = []

        for i in data_lst:
            line = f'{i[5]}\n' \
                   f'Маркет - {i[0]}\n' \
                   f'Назва товару - {i[1]}\n' \
                   f'Стара ціна - {i[2]} грн\n' \
                   f'Нова ціна - {i[3]} грн\n' \
                   f'Розмір знижки - {i[4]}%'
            new_lst.append(line)
        return new_lst

    def get_all_product_from_sql(self, market_list):
        if len(market_list) == 1:
            market_list = f"('{market_list[0]}')"
        else:
            market_list = tuple(market_list)

        query = self.connect.execute(f'''SELECT *
                                         FROM product
                                         WHERE market in {market_list}
                                         ORDER BY market;''')
        data_lst = query.fetchall()
        new_lst = []

        for i in data_lst:
            line = f'{i[5]}\n' \
                   f'Маркет - {i[0]}\n' \
                   f'Назва товару - {i[1]}\n' \
                   f'Стара ціна - {i[2]} грн\n' \
                   f'Нова ціна - {i[3]} грн\n' \
                   f'Розмір знижки - {i[4]}%'
            new_lst.append(line)
        return new_lst






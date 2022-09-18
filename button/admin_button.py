from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


# кнопки клавиатуры админа
b1 = KeyboardButton('/Вибрати_потрібні_маркети')
b2 = KeyboardButton('/Шукати_продукт_по_назві')
b3 = KeyboardButton('/Показати_всі_існуючі_знижки')
b4 = KeyboardButton('/Оновити_Базу_Данних')

bt_admin = ReplyKeyboardMarkup(resize_keyboard=True)
bt_admin.add(b1)
bt_admin.add(b2)
bt_admin.add(b3)
bt_admin.add(b4)

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


b1 = KeyboardButton('/Вибрати_потрібні_маркети')
b2 = KeyboardButton('/Шукати_продукт_по_назві')
b3 = KeyboardButton('/Наш_сайт')


bt_client = ReplyKeyboardMarkup(resize_keyboard=True)
bt_client.add(b1)
bt_client.add(b2)
bt_client.add(b3)


il_b1 = InlineKeyboardButton(text='Novus', callback_data='Market_Novus')
il_b2 = InlineKeyboardButton(text='Fora', callback_data='Market_Fora')
il_b3 = InlineKeyboardButton(text='ATB', callback_data='Market_ATB')
il_b4 = InlineKeyboardButton(text='Velmart', callback_data='Market_Velmart')
il_b5 = InlineKeyboardButton(text='Silpo', callback_data='Market_Silpo')


il_client = InlineKeyboardMarkup(row_width=2)
il_client.row(il_b1, il_b2).row(il_b3, il_b4).row(il_b5)

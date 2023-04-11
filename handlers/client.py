from aiogram import types, Dispatcher
from create_bot import bot
from button import client_button
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import requests
import io


class EnterProductFSM(StatesGroup):
    user_choice = State()


async def start_handler(message: types.Message):
    welcome_text = f'Вітання! Я – бот для пошуку цін на продуки в супермаркетах України. Якщо ви маєте запитання, ' \
                   f'ви можете знайти більше інформації на нашому сайті https://productprice.store.'

    requests.post(f'http://127.0.0.1:8000/api/telegram_user/create/{message.chat.id}/')
    await message.answer(welcome_text, reply_markup=client_button.bt_client)


async def show_site_url(message: types.Message):
    text = 'https://productprice.store/'
    await message.answer(text, reply_markup=client_button.bt_client)


# When you click the Вибрати_потрібні_маркети - display inline buttons in the chat
async def choice_market_handler(message: types.Message):
    await message.answer('Оберіть потрібні магазини', reply_markup=client_button.il_client)


async def choice_market_callback(callback: types.CallbackQuery):
    selected_market = callback.data.split('_')[1]
    user_id = callback.from_user.id

    # add/remove a store from the list
    send_market = requests.post(f'http://127.0.0.1:8000/api/UserMarketRelation/{user_id}/{selected_market}/')
    send_market_message = send_market.json()['message']

    # processing the full list of stores selected by the user
    get_list_markets = requests.get(f'http://127.0.0.1:8000/api/markets_list/{user_id}/')
    list_markets = [i['name'] for i in get_list_markets.json()]

    if len(list_markets) > 0:
        format_list_markets = ', '.join(list_markets)
    else:
        format_list_markets = ''

    await callback.answer(f"{send_market_message}\n\nВаш поточний список обраних магазинів: "
                          f"{format_list_markets}",
                          show_alert=True)


async def search_products_input(message: types.Message):
    user_id = message.from_user.id

    # get a complete list of selected markets by the user
    get_list_markets = requests.get(f'http://127.0.0.1:8000/api/markets_list/{user_id}/')
    list_markets = [i['name'] for i in get_list_markets.json()]

    if len(list_markets) > 0:
        await EnterProductFSM.user_choice.set()
        await bot.send_message(message.from_user.id, 'Введіть назву продукту в чат (Українській Мовою)\n'
                                                     'Наприклад: молоко, шампунь, печиво, цукерки...',
                               reply_markup=ReplyKeyboardRemove())

    else:    # if the user does not have any selected store,  display inline buttons in the chat
        await bot.send_message(message.from_user.id, 'Спочатку виберіть потрібні вам маркети',
                               reply_markup=client_button.il_client)


async def search_products_output(message: types.Message):
    user_id = message.from_user.id
    user_input = message.text

    get_products = requests.get(f'http://127.0.0.1:8000/api/SearchProductsAPIView/{user_id}?search_text={user_input}')
    json_products = get_products.json()

    for product in json_products:
        market_name = product['market_name']
        name = product['product_name']
        price = product['price']
        old_price = product['old_price']
        discount = product['discount']
        url_img = product['url_img']

        message_text = f"Магазин: {market_name}\n" \
                       f"Назва продукту: {name}\n" \
                       f"Нова ціна: {price}\n" \
                       f"Стара ціна: {old_price}\n" \
                       f"Знижка: {discount}"

        # downloading photos to RAM
        get_img = requests.get(url_img)
        image_bytes = io.BytesIO(get_img.content)
        photo = types.InputFile(image_bytes, filename='image.jpg')  # create photo for send in message

        await bot.send_photo(message.from_user.id, photo, caption=message_text, reply_markup=client_button.bt_client)
        image_bytes.close()     # delete photos from RAM


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start', 'help'])
    dp.register_message_handler(show_site_url, commands=['Наш_сайт'])
    dp.register_message_handler(choice_market_handler, commands=['Вибрати_потрібні_маркети'])
    dp.register_message_handler(search_products_input, commands=['Шукати_продукт_по_назві'])
    dp.register_message_handler(search_products_output, state=EnterProductFSM.user_choice)
    dp.register_callback_query_handler(choice_market_callback, Text(startswith='Market_'))





from aiogram import types, Dispatcher
from create_bot import bot
from button import client_button, admin_button
from aiogram.types import ReplyKeyboardRemove
from data_base import db_sqlite
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import time


user_market_choice = [dict()]


async def command_start(message: types.Message):
    if str(message.from_user.id) == '371752657':
        await bot.send_message(message.from_user.id, 'admin mode activated', reply_markup=admin_button.bt_admin)
    else:
        await bot.send_message(message.from_user.id, 'welcome...', reply_markup=client_button.bt_client)
        await message.delete()


# Обработка команды 'Шукати_продукт_по_назві'
class EnterProductFSM(StatesGroup):
    user_choice = State()


async def input_product_part_1(message: types.Message):
    # Если юзер выбрал магазины в функции 'Обиріть потрібні маркети'
    if message.from_user.id in user_market_choice[0] and user_market_choice[0].get(message.from_user.id) != []:

        await EnterProductFSM.user_choice.set()
        await bot.send_message(message.from_user.id, 'Введіть назву продукту в чат (Українській Мовою)\n'
                                                     'Наприклад: молоко, шампунь, печиво, цукерки...',
                               reply_markup=ReplyKeyboardRemove())

    else:    # Если юзер не выбрал магазины
        await bot.send_message(message.from_user.id, 'Спочатку виберіть потрібні вам маркети',
                               reply_markup=client_button.il_client)


async def input_product_part_2(message: types.Message, state=FSMContext):
    async with state.proxy() as data:
        data['user_choice'] = message.text

    user_data = await state.get_data()      # получаю словарь со всеми записями state

    product_info = db_sqlite.SqlDb().get_input_product_from_sql(user_data['user_choice'],
                                                                user_market_choice[0][message.from_user.id])
    if len(product_info) == 0:              # Если товар в SQL не найден, переделываем список в форму для фид бэка
        product_info = [f'Товара {user_data["user_choice"]} не знайдено']

    if str(message.from_user.id) == '371752657':        # для админа после сообщений вызываю админ панель кнопок
        for i in product_info:
            await bot.send_message(message.from_user.id, i, reply_markup=admin_button.bt_admin)
    else:                                               # для юзеров после сообщений вызываю обычную панель кнопок
        for i in product_info:
            await bot.send_message(message.from_user.id, i, reply_markup=client_button.bt_client)
    await state.finish()


# Обработка команды 'Показати_всі_існуючі_знижки'
async def all_product_handler(message: types.Message):
    # Если юзер выбрал магазины в функции 'Обиріть потрібні маркети'
    if message.from_user.id in user_market_choice[0] and user_market_choice[0].get(message.from_user.id) != []:

        product_info = db_sqlite.SqlDb().get_all_product_from_sql(user_market_choice[0][message.from_user.id])
        if str(message.from_user.id) == '371752657':   # для админа после сообщений вызываю админ панель кнопок
            for i in product_info:
                try:    # Если телеграмм блочит сообщение ( из за количества ), подождать 10 сек
                    await bot.send_message(message.from_user.id, i, reply_markup=admin_button.bt_admin)
                except:
                    time.sleep(10)
                    await bot.send_message(message.from_user.id, i, reply_markup=admin_button.bt_admin)
        else:                                          # для юзеров после сообщений вызываю обычную панель кнопок
            for i in product_info:
                try:    # Если телеграмм блочит сообщение ( из за количества ), подождать 10 сек
                    await bot.send_message(message.from_user.id, i, reply_markup=client_button.bt_client)
                except:
                    time.sleep(10)
                    await bot.send_message(message.from_user.id, i, reply_markup=admin_button.bt_admin)

    else:  # Если юзер не выбрал магазины
        await bot.send_message(message.from_user.id, 'Спочатку виберіть потрібні вам маркети',
                               reply_markup=client_button.il_client)


# Обработка функции Выбор маркетов
async def choice_market_handler(message: types.Message):
    await message.answer('Обиріть потрібні маркети', reply_markup=client_button.il_client)


async def choice_market_callback(callback: types.CallbackQuery):
    res = callback.data.split('_')[1]
    user_id = callback.from_user.id

    if user_id not in user_market_choice[0]:
        user_market_choice[0][user_id] = []

    if res in user_market_choice[0][user_id]:           # Если маркет уже был выбран, удалить из списка
        user_market_choice[0][user_id].remove(res)
        await callback.answer(f'{res} прибраний зі списку, '
                              f'ваш поточний список маркетів: {", ".join(user_market_choice[0][user_id])}',
                              show_alert=True)

    else:                                               # Если Юзер ранее не выбирал маркет, добавить в список
        user_market_choice[0][user_id].append(res)
        await callback.answer(f'{res} добавлений до списку, '
                              f'ваш поточний список маркетів: {", ".join(user_market_choice[0][user_id])}',
                              show_alert=True)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(input_product_part_1, commands=['Шукати_продукт_по_назві'])
    dp.register_message_handler(input_product_part_2, state=EnterProductFSM.user_choice)
    dp.register_message_handler(all_product_handler, commands=['Показати_всі_існуючі_знижки'])
    dp.register_message_handler(choice_market_handler, commands=['Вибрати_потрібні_маркети'])
    dp.register_callback_query_handler(choice_market_callback, Text(startswith='Market_'))





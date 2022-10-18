from aiogram import types, Dispatcher
from data_base import scraping_novus, scraping_fora, scraping_atb, scraping_velmart, scraping_silpo
from data_base import db_sqlite
from create_bot import bot


async def refresh_db(message: types.Message):
    if str(message.from_user.id) == '371752657':
        await bot.send_message(message.from_user.id, 'Parsing started')
        db_sqlite.SqlDb().reset_db()
        scraping_novus.scrap_novus()
        scraping_fora.scrap_fora()
        scraping_atb.scrap_atb()
        scraping_velmart.scrap_velmart()
        scraping_silpo.scrap_silpo()

        await bot.send_message(message.from_user.id, 'Parsing completed')


# регистрирумаем хендлеры
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(refresh_db, commands=['Оновити_Базу_Данних'])




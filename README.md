# Scraping_market (Telegram Bot - ___@DiscountProductMarket_Bot___)

## Technologies used
- Aiogram
- SQLite
- requests
- BeautifulSoup
- selenium


## Description
___Scraping_market___ is a telegram bot project that collects information on all actual discounts from Ukrainian supermarkets ___Novus, Fora, ATB, Velmart, Silpo, Auchan___ and import this data into the database SQLite. 
When the user enters the telegram bot and calls the / start command, he will be asked to select the supermarkets that are relevant to him.
It can be either one supermarket or several.
After that, the user has two functions to download all the current discounts for the stores that he has chosen or to search for the product he is interested in

![imgonline-com-ua-Resize-du3HUWaGfSwq8s](https://user-images.githubusercontent.com/96794562/191487724-83241b5f-8c58-4de8-8715-40797afed8e8.jpg)

![imgonline-com-ua-Resize-WX2f28WxKlHL](https://user-images.githubusercontent.com/96794562/191489054-58aa70d2-7e0e-4f3f-a443-fa1a8b67b533.jpg)

![imgonline-com-ua-Resize-kogZD3cpVFP20V](https://user-images.githubusercontent.com/96794562/191489462-e49a7928-0248-463d-98c5-10584a87dd9d.jpg)

## Admin account
The admin of this bot has an additional button panel in which there is one more command - update the database.
When you click on the update database button, site scraping starts, the old table in the database is deleted, a new one is created with fresh data

Admin bot is determined by user_id telegram

![imgonline-com-ua-Resize-WgydtE6wxd2](https://user-images.githubusercontent.com/96794562/191496848-f0d049ff-96d4-4f7a-9971-7025b76d2510.jpg)



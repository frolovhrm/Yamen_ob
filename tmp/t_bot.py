import os
import datetime
import asyncio
from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))


dp = Dispatcher(bot)


async def send_message_every_10_sec():
    await bot.send_message(os.getenv('ID'), 'Привет!')
    while True:
        await bot.send_message(os.getenv('ID'), datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S'), disable_notification=True)
        await asyncio.sleep(10)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(send_message_every_10_sec())
    executor.start_polling(dp)

import asyncio
import telebot as tb
from telebot.async_telebot import AsyncTeleBot
from modules import test
from modules import auto_message as auto_m
from configparser import ConfigParser
cfg = ConfigParser()
#cfg.read('bot/config.cfg')

bot = AsyncTeleBot('token')

@bot.message_handler(commands=['start'])
async def send_welcome(message: tb.types.Message):
    await bot.send_message(message.chat.id, await bot.get_me())


test.init_bot(bot)


if __name__ == '__main__':
    
    print(f'{asyncio.run(bot.get_my_name()).name} is running!')
    asyncio.run(auto_m.auto_message(bot))
    asyncio.run(bot.infinity_polling())
    
    
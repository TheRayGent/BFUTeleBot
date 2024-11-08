import asyncio
import telebot as tb
from telebot.async_telebot import AsyncTeleBot
from modules import test
#from modules import auto_message as auto_m
from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('bot/config.cfg')

from background import keep_alive

bot = AsyncTeleBot(cfg.get('Default', 'bot_token'))

@bot.message_handler(commands=['start'])
async def send_welcome(message: tb.types.Message):
    await bot.send_message(message.chat.id, await bot.get_me())

async def main():
    print(f'{(await bot.get_my_name()).name} is running!')
    await bot.polling()


    


test.init_bot(bot)


if __name__ == '__main__':
    #threading.Thread(target=asyncio.run(main())).start()
    keep_alive(bot)
    asyncio.run(main())
    #auto_m.auto_message()
    
    
    
    
    
    
    
from telebot.types import *
from telebot.async_telebot import AsyncTeleBot
import aioschedule 
import asyncio
import time



    
    
async def job(bot: AsyncTeleBot, text: str, chat_id: int):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('Yes',callback_data='Yes'))
    markup.add(InlineKeyboardButton('No', callback_data='No'))
    await bot.send_message(chat_id, text, reply_markup=markup)
    #asyncio.sleep(1)



async def auto_message(bot: AsyncTeleBot):
    aioschedule.every(10).seconds.do(job, bot = bot, text='ndw', chat_id = 1217602016) #message(bot, 'ndw', 1217602016)
    #loop = asyncio.get_event_loop()
    while True:
    
        await aioschedule.run_pending()
        await asyncio.sleep(1)



    '''@bot.message_handler(commands=['autom'])
    async def test_message(message: Message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton('Text'))

        await bot.send_message(message.chat.id, 'хз', reply_markup=markup)'''
    
    #@bot.callback_query_handler(func=lambda callback: True)
    #async def callback_query(callback: CallbackQuery):
        #await bot.send_message(callback.message.chat.id, 'Ответ')
from flask import Flask
from flask import request
from threading import Thread
import time
import requests
from telebot.types import *
from telebot.async_telebot import AsyncTeleBot
import asyncio

app = Flask('')

async def message(bot: AsyncTeleBot, text: str, chat_id: int):
  markup = InlineKeyboardMarkup()
  markup.add(InlineKeyboardButton('Yes',callback_data='Yes'))
  markup.add(InlineKeyboardButton('No', callback_data='No'))
  await bot.send_message(chat_id, text, reply_markup=markup)

class X3():
  def __init__(self, bot: AsyncTeleBot):
    self.bot = bot

  

  @app.route('/')
  def home(self):
    asyncio.run(message(self.bot, 'wdw', 1217602016))
    return "I'm alive"
    
  

  def run(self):
    app.run(host='0.0.0.0', port=80)


def keep_alive(bot: AsyncTeleBot):
  #x3 = 
  t = Thread(target=X3(bot).run)
  t.start()


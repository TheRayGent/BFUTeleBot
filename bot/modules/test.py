from telebot.types import *
from telebot.async_telebot import AsyncTeleBot





def init_bot(bot: AsyncTeleBot):
    @bot.message_handler(commands=['test'])
    async def test(message: Message):
        await bot.send_message(message.chat.id, text=message.chat.id)
    
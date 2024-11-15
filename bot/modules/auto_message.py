import asyncio
from aiogram import Bot, filters, Router, F
from aiogram import types as type
from magic_filter import MagicFilter
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ujson import loads as jsonloads
import datetime
#global tz
tz = datetime.timezone(datetime.timedelta(hours=2))
from configparser import ConfigParser
cfg = ConfigParser()
config = 'bot/config.cfg'
cfg.read(config)

rt = Router()

from os import path
from sys import argv

json_file = 'schedul.json' if __name__ == '__main__' else 'modules\\schedul.json'

upweek = str(cfg.get('Default', 'upweek'))

with open(path.join(path.dirname(argv[0]), json_file), 'r', encoding='utf-8') as f:
    json_data = f.read()
    sheddict = jsonloads(json_data)
sheddict = dict(sheddict)



async def message(bot: Bot, chat_id: int, lesson: str):
    weekday = str(datetime.datetime.today().astimezone(tz= tz).isoweekday())
    #text = sheddict[upweek][weekday][lesson]

    markup = type.InlineKeyboardMarkup(
        inline_keyboard=[
            [type.InlineKeyboardButton(text='\U00002705', callback_data='x3'),
             type.InlineKeyboardButton(text='\U0000274E', callback_data='x3'),
             type.InlineKeyboardButton(text='\U0001F637', callback_data='x3')
            ]
        ]
    )

    await bot.send_message(chat_id=chat_id, text='textdwqwqdqwd', reply_markup=markup)



def sched(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Kaliningrad")
    chat_id = 1217602016
    global attendance_file, today_date_file
    today_date_file = f'modules/attendance/{datetime.datetime.today().astimezone(tz= tz).date().day}.{datetime.datetime.today().astimezone(tz= tz).date().month}.txt'
    attendance_file = open(path.join(path.dirname(argv[0]), today_date_file), mode='a', encoding='utf-8')
    

    #for i in sheddict.get('time'):
        #time = str(sheddict['time'][i]).split(':')
        #scheduler.add_job(message, trigger='cron', hour=time[0], minute=time[1], kwargs={'bot': bot, 'chat_id': chat_id, 'lesson': str(i)}, id=str(i))
    #print(scheduler.get_jobs())
    
    #scheduler.add_job(message, trigger='interval', seconds = 5, kwargs={'bot': bot, 'chat_id': chat_id, 'lesson': '1'}, id='1')

    scheduler.start()

def edit_file(text: str):
    global attendance_file, today_date_file
    attendance_file.write(text)
    attendance_file.close
    attendance_file = open(path.join(path.dirname(argv[0]), today_date_file), mode='a', encoding='utf-8')
    

@rt.message(filters.Command('upweek'))
async def upweek_command(message: type.Message):
    global upweek
    upweek = 'upweek'
    cfg.set('Default', 'upweek', upweek)
    with open(config, 'w') as config_file:
        cfg.write(config_file)

@rt.message(filters.Command('downweek'))
async def downweek_command(message: type.Message):
    global upweek
    upweek = 'downweek'
    cfg.set('Default', 'upweek', upweek)
    with open(config, 'w') as config_file:
        cfg.write(config_file)



@rt.callback_query(F.data == 'x3')
async def shudl_callback(callback: type.CallbackQuery):
    text = f'{callback.message.date.astimezone(tz= tz).day}.{callback.message.date.astimezone(tz= tz).month}_{callback.message.text} = {callback.from_user.id}\n'
    
    edit_file(text)
    await callback.message.answer(f'{callback.message.date.astimezone(tz= tz)}')




from aiogram import Bot, filters, Router, F
from aiogram import types as type
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ujson import loads as jsonloads
import datetime
#global tz
tz = datetime.timezone(datetime.timedelta(hours=2))
from configparser import ConfigParser
cfg = ConfigParser()
config = 'bot/config.cfg'
cfg.read(config)
import zipfile

rt = Router()

from os import path
from os import listdir
from sys import argv

json_file = 'schedul.json' if __name__ == '__main__' else 'modules/schedul.json'

upweek = str(cfg.get('Default', 'upweek'))
admin_list = cfg.get('Default', 'admin_list').split(',')


with open(path.join(path.dirname(argv[0]), json_file), 'r', encoding='utf-8') as f:
    json_data = f.read()
    sheddict = jsonloads(json_data)
sheddict = dict(sheddict)



async def message(bot: Bot, chat_id: int, lesson: str, thread_id: int):
    weekday = str(datetime.datetime.today().astimezone(tz= tz).isoweekday())
    try:
        text = sheddict[upweek][weekday][lesson]
    except:
        return
    markup = type.InlineKeyboardMarkup(
        inline_keyboard=[
            [type.InlineKeyboardButton(text='\U00002705', callback_data='1'),
             type.InlineKeyboardButton(text='\U0000274E', callback_data='2'),
             type.InlineKeyboardButton(text='\U0001F637', callback_data='3')
            ]
        ]
    )
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, message_thread_id=thread_id)

async def rezerv(bot: Bot, auto: bool = False):
    if auto: 
        if 8 > datetime.datetime.now().astimezone(tz=tz).hour > 20: return
    with zipfile.ZipFile('rezerv.zip', mode='w') as zip_file:
        zip_file.write('bot/modules/attendance')
        for i in listdir('bot/modules/attendance'):
            zip_file.write(f'bot/modules/attendance/{i}')
    await bot.send_document(1217602016, document=type.FSInputFile('rezerv.zip'))

async def notificate():
    time = f'{datetime.datetime.now().astimezone(tz=tz).hour}:{datetime.datetime.now().astimezone(tz=tz).minute}'
    cfg.set('Default', 'last_ping', time)
    with open(config, 'w') as config_file:
        cfg.write(config_file)

def sched(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="Europe/Kaliningrad")
    chat_id = cfg.get('Default', 'chat_id')
    thread_id = cfg.get('Default', 'thread_id')
    global attendance_file, today_date_file
    today_date_file = f'modules/attendance/{datetime.datetime.today().astimezone(tz= tz).date().day}.{datetime.datetime.today().astimezone(tz= tz).date().month}.txt'
    attendance_file = open(path.join(path.dirname(argv[0]), today_date_file), mode='a', encoding='utf-8')
    

    for i in sheddict.get('time'):
        time = str(sheddict['time'][i]).split(':')
        scheduler.add_job(message, trigger='cron', hour=time[0], minute=time[1], kwargs={'bot': bot, 'chat_id': chat_id, 'lesson': str(i), 'thread_id': thread_id}, id=str(i))
    
    #scheduler.add_job(upweek_edit, trigger='cron', hour='0')
    scheduler.add_job(rezerv, trigger='interval', hours = 2, kwargs={'bot': bot, 'auto': True})
    print(scheduler.get_jobs())

    scheduler.start()


def edit_file(text: str):
    global attendance_file, today_date_file
    attendance_file.write(text)
    attendance_file.close
    attendance_file = open(path.join(path.dirname(argv[0]), today_date_file), mode='a', encoding='utf-8')
    print(text[:-1])
    

async def upweek_edit():
    global upweek
    upweek = 'upweek' if upweek != 'upweek' else 'downweek'
    cfg.set('Default', 'upweek', upweek)
    with open(config, 'w') as config_file:
        cfg.write(config_file)
    print(f'upweek = "{upweek}"')

@rt.message(filters.Command('upweek'))
async def upweek_command(message: type.Message = None):
    if str(message.from_user.id) in admin_list:
        await upweek_edit()
        if upweek=='upweek': text = 'Неделя теперь верхняя!'
        else: text = 'Неделя теперь нижняя!'
        await message.answer(text)
    else: await message.answer('У вас нет прав для этой команды!')

@rt.message(filters.Command('rezerv'))
async def rezerv_command(message: type.Message, bot: Bot):
    await rezerv(bot)

@rt.callback_query(F.data == '1')
@rt.callback_query(F.data == '2')
@rt.callback_query(F.data == '3')
async def shudl_callback(callback: type.CallbackQuery):
    text = f'{callback.message.date.astimezone(tz= tz).day}.{callback.message.date.astimezone(tz= tz).month}_{callback.message.text}_{callback.from_user.id} = {callback.data}\n'
    edit_file(text)
    #await callback.message.answer(f'{callback.message.date.astimezone(tz= tz)}')





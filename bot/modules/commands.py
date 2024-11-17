from aiogram import Bot, Router,filters
from aiogram import types as type
import modules.gtls as gtls
import datetime
tz = datetime.timezone(datetime.timedelta(hours=2))

from configparser import ConfigParser
cfg = ConfigParser()
cfg.read('bot/config.cfg')
admin_list = cfg.get('Default', 'admin_list').split(',')
chatid = cfg.get('Default', 'chat_id')
threadid = cfg.get('Default', 'thread_id')
print(admin_list)
rt = Router()

@rt.message(filters.Command('test'))
async def test(message: type.Message):
    await message.answer("Test")

@rt.message(filters.Command('chat_id'))
async def chat_id(message: type.Message):
    #await message.answer(f'{message.chat.id}')
    print(f'{message.chat}')

@rt.message(filters.Command('thread_id'))
async def thread_id(message: type.Message):
    #await message.answer(f'{message.chat.id}')
    print(f'{message.message_thread_id}')

@rt.message(filters.Command('user_id'))
async def user_id(message: type.Message):
    #await message.answer(f'{message.from_user.id}')
    print(f'{message.from_user.id} = {message.from_user.username}')

@rt.message(filters.Command('getlist'))
async def attendance_list(message: type.Message, bot: Bot, command: filters.CommandObject):
    if str(message.from_user.id) in admin_list:
        filename = str(command.args).strip()
        if filename != 'None':
            try:
                open(f'bot/modules/attendance/{filename}.txt')
                await message.answer(await gtls.get_list(bot, filename), parse_mode='HTML')
            except FileNotFoundError:
                await message.answer('Такой файл не обнаружен!')
        else:
            filename = f'{datetime.datetime.today().astimezone(tz=tz).day}.{datetime.datetime.today().astimezone(tz=tz).month}'
            await message.answer(await gtls.get_list(bot, filename), parse_mode='HTML')
    else: await message.answer('У вас нет прав для этой команды!')

@rt.message(filters.Command('getlistgood'))
async def attendance_listgood(message: type.Message, bot: Bot, command: filters.CommandObject):
    if str(message.from_user.id) in admin_list:
        filename = str(command.args).strip()
        if filename != 'None':
            try:
                open(f'bot/modules/attendance/{filename}.txt')
                await message.answer(await gtls.get_list(bot, filename, True), parse_mode='HTML')
            except FileNotFoundError:
                await message.answer('Такой файл не обнаружен!')
        else:
            filename = f'{datetime.datetime.today().astimezone(tz=tz).day}.{datetime.datetime.today().astimezone(tz=tz).month}'
            await message.answer(await gtls.get_list(bot, filename, True), parse_mode='HTML')
    else: await message.answer('У вас нет прав для этой команды!')

@rt.message(filters.Command('donate'))
async def donate(message: type.Message):
    markup = type.InlineKeyboardMarkup(
        inline_keyboard=[
            [type.InlineKeyboardButton(text='Поддержать💸', url='https://yoomoney.ru/fundraise/16IE8OM3FQC.241117')]])
    await message.answer('🤑Поддержи разраба рублём!💵', reply_markup=markup)

@rt.message(filters.Command('customlesson'))
async def custom_lesson(message: type.Message, bot: Bot, command: filters.CommandObject):
    if str(message.from_user.id) in admin_list:
        text = str(command.args)
        if text != 'None':
            markup = type.InlineKeyboardMarkup(
            inline_keyboard=[
                [type.InlineKeyboardButton(text='\U00002705', callback_data='1'),
                type.InlineKeyboardButton(text='\U0000274E', callback_data='2'),
                type.InlineKeyboardButton(text='\U0001F637', callback_data='3')
                ]])
            await bot.send_message(chat_id=chatid, text=text, reply_markup=markup, message_thread_id=threadid)
            if chatid!=str(message.chat.id): await message.answer('Сообщение отправлено в чат "Посещаемость".')
        else: await message.answer('Вы не ввели название пары!')
    else: await message.answer('У вас нет прав для этой команды!')
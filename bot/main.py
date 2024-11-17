import asyncio
from aiogram import Bot, Dispatcher
from modules import auto_message, commands

from configparser import ConfigParser
cfg = ConfigParser()

cfg.read('bot/config.cfg')

#from aiogram.client.session.aiohttp import AiohttpSession
#session = AiohttpSession(proxy='http://proxy.server:3128')
dp = Dispatcher()
bot = Bot(token=cfg.get('Default', 'bot_token'))

async def automessage(bot: Bot, chat_id: int, text: str):
    print('1')
    await bot.send_message(chat_id=chat_id, text=text)

@dp.startup()
async def startup(bot: Bot):
    print(f'{(await bot.get_my_name()).name} is running!')

async def main() -> None:
    
    dp.include_routers(
        commands.rt,
        auto_message.rt
    )
    auto_message.sched(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
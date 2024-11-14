import asyncio
import aiogram
from aiogram import Bot, Router,filters
from aiogram import types as type

rt = Router()

@rt.message(filters.Command('test'))
async def test(message: type.Message):
    await message.answer("Hello!")
    
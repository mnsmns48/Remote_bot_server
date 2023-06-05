from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from db_pg_work import get_today_activity, take_last_guests
from filters import AdminFilter
from keyboards.admin_k import admin_basic_kb

admin_ = Router()


async def start(m: Message):
    await m.answer('Admin Mode', reply_markup=admin_basic_kb)


async def show_sales(m: Message):
    text = get_today_activity()
    await m.answer(text)


async def show_guests(m: Message):
    text = take_last_guests()
    await m.answer(text)


def register_admin_handlers():
    admin_.message.filter(AdminFilter())
    admin_.message.register(start, CommandStart())
    admin_.message.register(show_sales, F.text == 'Продажи сегодня')
    admin_.message.register(show_guests, F.text == 'Последние гости')
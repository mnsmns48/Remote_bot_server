from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import bot, hidden_vars as hv

from db_pg_work import user_spotted, get_full_list
from keyboards.user_k import user_first_kb, catalog_full_kb, catalog_brand_phones_kb

user_ = Router()


async def start(m: Message):
    user_spotted(time_=m.date,
                 id_=m.from_user.id,
                 fullname=m.from_user.full_name,
                 username=m.from_user.username)
    await bot.send_message(chat_id=hv.admin_id[0],
                           text=f"new user spotted\n"
                                f"{str(m.date).rsplit(':', maxsplit=2)[0]} "
                                f"{m.from_user.full_name} "
                                f"{m.from_user.username}\n"
                                f"{m.from_user.id}",
                           disable_notification=True
                           )
    await m.answer_photo(photo='AgACAgIAAxkBAAIFuWQVrxkxJMuUdAUGfGAuXSt448I1AAKgxjEbYxGxSFOciZYzLCoJAQADAgADeQADLwQ',
                         caption=f'Привет, {m.from_user.full_name}, этот БОТ показывает наличие и цены '
                                 f'в салоне мобильной связи ЦИФРОТЕХ\n\n'
                                 f'А также актуальные цены на продукцию под заказ',
                         reply_markup=user_first_kb)


async def catalog_all(m: Message):
    await m.answer(text='Выбери группу товаров', reply_markup=catalog_full_kb)


async def catalog_phones(m: Message):
    await m.answer(text='Выбери производителя или в конце списка есть перечень всех моделей',
                   reply_markup=catalog_brand_phones_kb)


async def phones_full_catalog(m: Message):
    text = get_full_list('Смартфон')
    await m.answer(text)


def register_user_handlers():
    user_.message.register(start, CommandStart())
    user_.message.register(catalog_all, F.text == 'В наличии')
    user_.message.register(catalog_phones, F.text == 'Смартфоны')
    user_.message.register(phones_full_catalog, F.text == "Полный список смартфонов")

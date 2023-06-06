from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import bot, hidden_vars as hv

from db_pg_work import user_spotted, get_full_list, get_goods_desc
from db_tables import avail
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
    res = '--- В наличии:\n'
    response = get_full_list(type_=avail.c.type_,
                             ty_l=['Смартфоны'],
                             brand=avail.c.type_,
                             br_l=['Смартфоны'])
    for line in response:
        res += ''.join(f"{line[0].split(' ', maxsplit=1)[1]} - {line[2]} руб")
        res += '\n'
    await m.answer(res)


async def phones_brand_avail(m: Message):
    kb = InlineKeyboardBuilder()
    brand_l = m.text.split(' / ')
    response = get_full_list(type_=avail.c.type_,
                             ty_l=['Смартфоны'],
                             brand=avail.c.brand,
                             br_l=brand_l)
    if response:
        for line in response:
            kb.row(InlineKeyboardButton(
                text=f"{line[2]} {line[0].split(' ', maxsplit=1)[1]}",
                callback_data=line[3]))
        await m.answer('Что есть в наличии:', reply_markup=kb.as_markup())
    else:
        await m.answer('Нет в наличии')


async def begin(m: Message):
    await m.answer('Выбери категорию', reply_markup=user_first_kb)


async def show_other_position(m: Message):
    kb = InlineKeyboardBuilder()
    response = get_full_list(type_=avail.c.type_,
                             ty_l=[m.text],
                             brand=avail.c.type_,
                             br_l=[m.text])
    if response:
        for line in response:
            kb.row(InlineKeyboardButton(
                text=f"{line[2]} {line[0].split(' ', maxsplit=1)[1]}",
                callback_data=line[3]))
        await m.answer('Что есть в наличии:', reply_markup=kb.as_markup())
    else:
        await m.answer('Нет в наличии')


async def show_product(c: CallbackQuery):
    response = get_goods_desc(c.data)
    text = f"{response.get('product_name')}\n{response.get('price')}\nв наличии {response.get('quantity')}\n\n"
    if response.get('full_desc'):
        text += response.get('full_desc')
    photo = response.get('link')
    print(len(text))
    await c.message.answer_photo(photo=photo, caption=text)


def register_user_handlers():
    user_.callback_query.register(show_product)
    user_.message.register(start, CommandStart())
    user_.message.register(begin, F.text == 'Перейти в начало')
    user_.message.register(catalog_all, F.text == 'В наличии')
    user_.message.register(catalog_phones, F.text == 'Смартфоны')
    user_.message.register(phones_full_catalog, F.text == "Полный список смартфонов")
    user_.message.register(phones_brand_avail, F.text.in_({
        'Xiaomi / Redmi / Poco',
        'Realme / Oppo / OnePlus',
        'Huawei / Honor',
        'Samsung',
        'Tecno / Infinix',
        'TCL'
    }))
    user_.message.register(show_other_position, F.text.in_({
        'Планшеты',
        'Умные часы',
        'Кнопочные телефоны',
        'PowerBanks'
    }))

import logging
from datetime import datetime

import pytz
from sqlalchemy import Table
from yadisk import YaDisk

from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from db_tables import optmobex_xiaomi_table, optmobex_apple_table, optmobex_samsung_table


@dataclass
class Hidden:
    bot_token: str
    admin_id: list[int]
    yatoken: str
    ssh_host: str
    ssh_username: str
    ssh_password: str
    remote_bind_address_host: str
    remote_bind_address_port: str
    server_db_username_server: str
    server_db_password_server: str


def load_config(path: str = None):
    env = Env()
    env.read_env()
    return Hidden(
        admin_id=list(map(int, env.list("ADMIN_ID"))),
        bot_token=env.str("BOT_TOKEN"),
        yatoken=env.str("YATOKEN"),
        ssh_host=env.str("SSH_HOST"),
        ssh_username=env.str("SSH_USERNAME"),
        ssh_password=env.str("SSH_PASSWORD"),
        remote_bind_address_host=env.str("REMOTE_BIND_ADDRESS_HOST"),
        remote_bind_address_port=env.int("REMOTE_BIND_ADDRESS_PORT"),
        server_db_username_server=env.str("SERVER_DB_USERNAME_SERVER"),
        server_db_password_server=env.str("SERVER_DB_PASSWORD_SERVER"),
    )


logging.basicConfig(level=logging.INFO)

hidden_vars = load_config('..env')
storage = RedisStorage.from_url('redis://@localhost:6379/0')
bot = Bot(token=hidden_vars.bot_token)
dp = Dispatcher()
y = YaDisk(token=hidden_vars.yatoken)

commands = [
    BotCommand(
        command='start',
        description='Начало работы бота'
    ),
    BotCommand(
        command='admin_message',
        description='Написать админу'
    )
]


def month_conv(m: str) -> str:
    month = {
        '01': 'Январь',
        '02': 'Февраль',
        '03': 'Март',
        '04': 'Апрель',
        '05': 'Май',
        '06': 'Июнь',
        '07': 'Июль',
        '08': 'Август',
        '09': 'Сентябрь',
        '10': 'Октябрь',
        '11': 'Ноябрь',
        '12': 'Декабрь'
    }
    return f"{month.get(m.split('-')[1])} {m.split('-')[0]}"


def price_def(s: str) -> Table:
    temp_dict = {
        'Xiaomi под заказ': optmobex_xiaomi_table,
        'Samsung под заказ': optmobex_samsung_table,
        'Apple под заказ': optmobex_apple_table
    }
    return temp_dict.get(s)


def get_date_from_db(response):
    date = response.split('T')[0]
    time = response.split('T')[1]
    old_format_date = datetime.strptime(date, '%Y-%m-%d')
    result = old_format_date.strftime('%d-%m-%Y')
    return str(result) + ' в ' + time


def title_formatting(price, name):
    del_list = list()
    if price == 'optmobex_xiaomi':
        del_list = ['EU ', 'Xiaomi ', 'CN', ' RU/СТБ', ' RU']
    if price == 'optmobex_samsung':
        del_list = ['Samsung Galaxy', 'AE', 'AH', 'KZ', 'EU', 'CN',
                    'IN', ',', 'Simfree', 'RU', 'ZA', '   ', 'TH', '/']
    for i in del_list:
        name = name.replace(i, '')
    return name


def resolution_conv(r: str) -> str:
    return f"{r.split(' x ')[1]}x{r.split(' x ')[0]}"


def date_out(date: str) -> str:
    m_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S%z")
    tz = pytz.timezone("Etc/GMT-3")
    m_date_utc3 = tz.normalize(m_date.astimezone(tz))
    out_date = m_date_utc3.strftime("%Y-%m-%d %H:%M:%S")
    return out_date

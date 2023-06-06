import logging
from yadisk import YaDisk

from aiogram.fsm.storage.redis import RedisStorage
from environs import Env
from dataclasses import dataclass

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand


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



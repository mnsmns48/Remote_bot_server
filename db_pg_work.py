from datetime import datetime, timedelta
from typing import Sequence

from sqlalchemy import create_engine, select, func, insert, desc, Column, Row
from sqlalchemy.engine.result import _TP

from config import hidden_vars as hv, y, month_conv
from sshtunnel import SSHTunnelForwarder

from db_tables import activity, guests, avail, s_main, display, energy, camera, performance


def get_today_activity() -> str:
    sales, returns, cardpay, amount = list(), list(), list(), list()
    with SSHTunnelForwarder(
            (hv.ssh_host, 22),
            ssh_username=hv.ssh_username,
            ssh_password=hv.ssh_password,
            remote_bind_address=(hv.remote_bind_address_host, hv.remote_bind_address_port)) as server:
        server.start()
        local_port = str(server.local_bind_port)
        print('Соединение с внешним сервером БД успешно')
        engine = create_engine(f"postgresql://{hv.server_db_username_server}:{hv.server_db_password_server}"
                               f"@localhost:{local_port}/activity_server",
                               echo=False)
        conn = engine.connect()
        today = datetime.now().date()
        sample = select(activity).filter(func.DATE(activity.c.time_) == today).order_by(activity.c.time_)
        response = conn.execute(sample).fetchall()
        conn.close()
    for line in response:
        if not line[8]:
            amount.append(line[6])
        if line[7]:
            cardpay.append(line[6])
        l_temp_ = [
            str(line[1]).split(' ')[1][:5],
            line[3],
            line[4],
            int(line[5]) if str(line[5]).split('.')[1] == '0' else line[5],
            int(line[6]) if str(line[6]).split('.')[1] == '0' else line[6],
            '--C--' if line[7] else ''
        ]
        if line[8]:
            returns.append(l_temp_)
            amount.remove(line[6])
        else:
            sales.append(l_temp_)
    res = str()
    for line in sales:
        for i in line:
            res += ''.join(str(i) + ' ')
        res += '\n'
    if returns:
        res += '---Возвраты:\n'
        for line in returns:
            for i in line:
                res += ''.join(str(i) + ' ')
            res += '\n'
    res += f'Всего {sum(amount)}\n' \
           f'Наличные {sum(amount) - sum(cardpay)}\n'
    if sum(cardpay):
        res += f'Картой {sum(cardpay)}'
    return res


def user_spotted(time_: datetime, id_: int, fullname: str, username: str) -> None:
    insert_data = {
        'time_': str(time_).split('+')[0],
        'id_': id_,
        'fullname': fullname,
        'username': username
    }
    with SSHTunnelForwarder(
            (hv.ssh_host, 22),
            ssh_username=hv.ssh_username,
            ssh_password=hv.ssh_password,
            remote_bind_address=(hv.remote_bind_address_host, hv.remote_bind_address_port)) as server:
        server.start()
        local_port = str(server.local_bind_port)
        print('Соединение с внешним сервером БД успешно')
        engine = create_engine(f"postgresql://{hv.server_db_username_server}:{hv.server_db_password_server}"
                               f"@localhost:{local_port}/activity_server",
                               echo=False)
        conn = engine.connect()
        conn.execute(insert(guests), insert_data)
        conn.commit()
        conn.close()


def take_last_guests() -> str:
    res = str()
    with SSHTunnelForwarder(
            (hv.ssh_host, 22),
            ssh_username=hv.ssh_username,
            ssh_password=hv.ssh_password,
            remote_bind_address=(hv.remote_bind_address_host, hv.remote_bind_address_port)) as server:
        server.start()
        local_port = str(server.local_bind_port)
        print('Соединение с внешним сервером БД успешно')
        engine = create_engine(f"postgresql://{hv.server_db_username_server}:{hv.server_db_password_server}"
                               f"@localhost:{local_port}/activity_server",
                               echo=False)
        conn = engine.connect()
        sample = select(guests).order_by(desc(guests.c.time_)).limit(2)
        response = conn.execute(sample).fetchall()
        conn.close()
        for line in response:
            res += ''.join(f"{str(line[0])} {line[1:-1]} {line[-1] if line[-1] is not None else ''}")
            res += '\n'
        return res


def get_full_list(type_: Column, ty_l: list, brand: Column, br_l: list) -> Sequence[Row[_TP]]:
    with SSHTunnelForwarder(
            (hv.ssh_host, 22),
            ssh_username=hv.ssh_username,
            ssh_password=hv.ssh_password,
            remote_bind_address=(hv.remote_bind_address_host, hv.remote_bind_address_port)) as server:
        server.start()
        local_port = str(server.local_bind_port)
        print('Соединение с внешним сервером БД успешно')
        engine = create_engine(f"postgresql://{hv.server_db_username_server}:{hv.server_db_password_server}"
                               f"@localhost:{local_port}/activity_server",
                               echo=False)
        # engine = create_engine(f"postgresql://baza:{hv.server_db_password_server}"
        #                        f"@localhost:5432/activity_client")
        conn = engine.connect()
        sample = select(avail.c.product, avail.c.quantity, avail.c.price, avail.c.code).where(type_.in_(ty_l)) \
            .where(brand.in_(br_l)).order_by(avail.c.price).order_by(avail.c.brand)
        response = conn.execute(sample).fetchall()
        conn.close()
        return response


def resolution_conv(param):
    pass


def get_goods_desc(g_desc: str) -> dict:
    with SSHTunnelForwarder(
            (hv.ssh_host, 22),
            ssh_username=hv.ssh_username,
            ssh_password=hv.ssh_password,
            remote_bind_address=(hv.remote_bind_address_host, hv.remote_bind_address_port)) as server:
        server.start()
        local_port = str(server.local_bind_port)
        print('Соединение с внешним сервером БД успешно')
        engine = create_engine(f"postgresql://{hv.server_db_username_server}:{hv.server_db_password_server}"
                               f"@localhost:{local_port}/activity_server",
                               echo=False)
        conn = engine.connect()
        sample = select(avail).where(avail.c.code == g_desc)
        response = conn.execute(sample).fetchone()
        conn.close()
    temp_dict_ = {
        'product_name': response[3],
        'link': y.get_download_link(f"/Photo/{response[2]}.jpg"),
        'quantity': str(response[4]) + ' шт',
        'price': str(response[5]) + ' руб',
    }
    model_for_link = response[3].rsplit(' ', maxsplit=2)[0].split(' ', maxsplit=1)[1]
    if response[0] == 'Смартфоны':
        with SSHTunnelForwarder(
                (hv.ssh_host, 22),
                ssh_username=hv.ssh_username,
                ssh_password=hv.ssh_password,
                remote_bind_address=(hv.remote_bind_address_host, hv.remote_bind_address_port)) as server:
            server.start()
            local_port = str(server.local_bind_port)
            print('Соединение с внешним сервером БД успешно')
            engine = create_engine(f"postgresql://{hv.server_db_username_server}:{hv.server_db_password_server}"
                                   f"@localhost:{local_port}/phones",
                                   echo=False)
            conn2 = engine.connect()
            sample = select(
                s_main.c.title,
                s_main.c.release_date,
                s_main.c.category,
                display.c.d_size,
                display.c.display_type,
                display.c.refresh_rate,
                display.c.resolution,
                energy.c.capacity,
                energy.c.max_charge_power,
                energy.c.fast_charging,
                camera.c.lenses,
                camera.c.megapixels_front,
                performance.c.storage_size,
                performance.c.ram_size,
                performance.c.chipset,
                performance.c.total_score,
                s_main.c.advantage,
                s_main.c.disadvantage) \
                .where(
                (s_main.c.title == str(model_for_link)) &
                (s_main.c.title == display.c.title) &
                (s_main.c.title == energy.c.title) &
                (s_main.c.title == camera.c.title) &
                (s_main.c.title == performance.c.title)
            )
            description = conn2.execute(sample).fetchone()
            conn2.close()
            advantages = str()
            try:
                for line in description[16]:
                    advantages += '+ ' + line + '\n'
                disadvantages = str()
                for line in description[17]:
                    disadvantages += '- ' + line + '\n'
                temp_dict_.update(
                    {
                        'full_desc':
                            f"Дата выхода: {month_conv(description[1])}\n"
                            f"Класс: {description[2]}\n"
                            f"Дисплей: {description[3]} {description[4]} {description[6]} {description[5]} Hz\n"
                            f"АКБ: {description[7]}, мощность заряда: {int(description[8])} W\n"
                            f"Быстрая зарядка: {description[9]}\n"
                            f"Основные камеры: {description[10]}\n"
                            f"Фронтальная: {int(description[11])} Мп\n"
                            f"Процессор: {description[14]}\n"
                            f"Оценка производительности: {description[15]}\n"
                            f"\nПреимущества\n"
                            f"{advantages}"
                            f"\nНедостатки\n"
                            f"{disadvantages}"
                    }
                )
            except TypeError:
                pass
    return temp_dict_

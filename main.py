import asyncio

from config import dp, bot, commands, storage
from handlers.admin_handler import admin_, register_admin_handlers
from handlers.user_handler import user_, register_user_handlers
from middleware import ThrottlingMiddleware


async def bot_working():
    dp.message.middleware.register(ThrottlingMiddleware(storage=storage))
    register_admin_handlers()
    register_user_handlers()
    dp.include_routers(admin_, user_)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    finally:
        await bot.session.close()


async def main():
    bot_task = asyncio.create_task(bot_working())
    await asyncio.gather(bot_task)


if __name__ == '__main__':
    try:
        print('Bot went to work on server')
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot Stopped')

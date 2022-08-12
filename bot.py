import asyncio
from aiogram import Bot, Dispatcher
from handlers import start
from db.all_clients_db import create_all_clients_db
from db.new_clients import create_new_clients_db




async def main():
    bot = Bot(token='5517206387:AAHeZNcPbI07xnwbxxVS9LfopJs9om7FHWc', parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(start.router)

    create_all_clients_db()
    create_new_clients_db()

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

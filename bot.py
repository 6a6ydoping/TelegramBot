import asyncio
from aiogram import Bot, Dispatcher
from handlers import start
from db.user_db import create_db



async def main():
    bot = Bot(token='5517206387:AAHeZNcPbI07xnwbxxVS9LfopJs9om7FHWc', parse_mode="HTML")
    dp = Dispatcher()

    dp.include_router(start.router)

    create_db()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

# ایمپورت‌ها از روت اصلی (بدون کلمه bot.)
from config import BOT_TOKEN
from database.session import init_db
from database.seed import seed_all
from middlewares.membership import MembershipMiddleware
from handlers import start, shop, payment, admin, wallet

async def main():
    if not BOT_TOKEN:
        raise SystemExit("❌ BOT_TOKEN تنظیم نشده!")

    await init_db()
    await seed_all()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.message.middleware(MembershipMiddleware())
    dp.callback_query.middleware(MembershipMiddleware())

    dp.include_routers(
        start.router,
        shop.router,
        payment.router,
        wallet.router,
        admin.router,
    )

    print("🚀 ربات در حال اجراست...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

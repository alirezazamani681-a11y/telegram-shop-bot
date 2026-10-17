import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.database.session import init_db
from bot.database.seed import seed_all
from bot.middlewares.membership import MembershipMiddleware
from bot.handlers import start, shop, payment, admin, wallet

# ⚠️ تنظیمات پروکسی
os.environ["HTTP_PROXY"] = "http://127.0.0.1:10809"
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:10809"

async def main():
    # 🔴 توکن اینجا قرار داده شده است 🔴
    BOT_TOKEN = "8810132906:AAGL1Xf6rA7fwXpIjnKNthLQ-kKqqd0EJ94"
    
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
import asyncio
import logging
from aiogram import Bot, Dispatcher
from src.config import BOT_TOKEN, ADMIN_ID
from src.handlers.commands import router
from src.handlers.scheduler import start_scheduler, restore_scheduled_messages

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Include routers
dp.include_router(router)


async def on_startup():
    """
    Send startup message when bot starts and restore scheduled messages
    """
    await bot.send_message(ADMIN_ID, "Bot đã khởi động")
    await restore_scheduled_messages(bot)


async def main():
    # Start the scheduler
    start_scheduler()

    # Register startup handler
    dp.startup.register(on_startup)

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

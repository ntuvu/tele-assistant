import asyncio
import logging
import threading

from aiogram import Bot, Dispatcher

from src.api.health_check_api import run_flask
from src.bot.commands import router
from src.config.config import BOT_TOKEN, ADMIN_ID
from src.schedule.scheduler import start_scheduler, restore_scheduled_messages

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

    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # This ensures the thread will exit when the main program exits
    flask_thread.start()
    logging.info("Flask API started on port 8000")

    # Register startup handler
    dp.startup.register(on_startup)

    # Start polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

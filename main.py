import asyncio
import logging
import threading

from aiogram import Bot, Dispatcher
from flask import Flask, jsonify

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

# Initialize Flask app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Bot is running"})


@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        "bot": "active",
        "version": "1.0.0"
    })


def run_flask():
    """
    Run Flask application in a separate thread
    """
    app.run(host='0.0.0.0', port=8000)


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

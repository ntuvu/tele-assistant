import logging

import aiohttp
from aiogram.types import Message

from src.config.config import WEATHER_API_KEY
# Assuming scheduler functions are in src.handlers.scheduler
# Adjust the import path if your structure is different
from src.schedule.scheduler import parse_datetime, schedule_message
from src.util.utils import format_weather

logger = logging.getLogger(__name__)


async def get_chat_info(chat_id: int, user_id: int) -> str:
    """
    Get formatted chat information
    """
    return f"Chat ID: {chat_id}\nUser ID: {user_id}"


async def handle_schedule_command(message: Message) -> str:
    """
    Parses the schedule command message, schedules the message, and returns a response string.
    """
    try:
        # Split the message text into parts
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            return (
                "Please provide date, time, and message in the format:\n"
                "/schedule dd/MM/yyyy HH:mm message"
            )

        date_str = parts[1]
        time_str = parts[2]
        content = parts[3]  # Use the actual content provided

        # Parse the datetime
        scheduled_time = parse_datetime(date_str, time_str)

        # Schedule the message using the extracted content
        # Pass message.bot explicitly if needed by schedule_message
        # Assuming schedule_message is defined as:
        # async def schedule_message(bot: Bot, chat_id: int, scheduled_time: datetime, message: str)
        await schedule_message(message.bot, message.chat.id, scheduled_time, content)

        return f"Message scheduled for {scheduled_time.strftime('%d/%m/%Y %H:%M')}"

    except ValueError as ve:
        logger.warning(f"Value error during scheduling for chat {message.chat.id}: {ve}")
        # Return the specific error message from parse_datetime
        return str(ve)
    except Exception as e:
        logger.error(f"Unexpected error during scheduling for chat {message.chat.id}: {e}", exc_info=True)
        # Return a generic error message for other exceptions
        return f"An unexpected error occurred: {str(e)}"


async def fetch_weather_by_city(city):
    url = (
        f"https://api.weatherapi.com/v1/current.json"
        f"?key={WEATHER_API_KEY}&q={city}&aqi=no&lang=vi"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as resp:
            if resp.status == 200:
                data = await resp.json()
                return format_weather(data)
    return "Xin lỗi, tôi không thể tìm thấy thời tiết cho thành phố đó."


async def fetch_weather_by_coords(latitude, longitude):
    url = (
        f"https://api.weatherapi.com/v1/current.json"
        f"?key={WEATHER_API_KEY}&q={latitude},{longitude}&aqi=no&lang=vi"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as resp:
            if resp.status == 200:
                data = await resp.json()
                return format_weather(data)
    return "Xin lỗi, tôi không thể lấy được thông tin thời tiết từ vị trí của bạn."

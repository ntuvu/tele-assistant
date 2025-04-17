from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from src.handlers.services import get_hello_message, get_chat_info
from src.handlers.decorators import admin_only
from src.handlers.scheduler import parse_datetime, schedule_message
from datetime import datetime

# Create a router for commands
router: Router = Router()


@router.message(Command("hello"))
@admin_only
async def hello_command(message: Message) -> None:
    """
    Handle the /hello command
    """
    response: str = await get_hello_message()
    await message.answer(response)


@router.message(Command("info"))
async def info_command(message: Message) -> None:
    """
    Handle the /info command - returns chat ID and user ID
    """
    chat_id: int = message.chat.id
    user_id: int = message.from_user.id
    response: str = await get_chat_info(chat_id, user_id)
    await message.answer(response)


@router.message(Command("schedule"))
@admin_only
async def schedule_command(message: Message) -> None:
    """
    Handle the /schedule command
    Format: /schedule dd/MM/yyyy HH:mm message
    """
    try:
        # Split the message text into parts
        parts = message.text.split(maxsplit=3)
        if len(parts) < 4:
            await message.answer(
                "Please provide date, time, and message in the format:\n/schedule dd/MM/yyyy HH:mm message"
            )
            return

        date_str = parts[1]
        time_str = parts[2]
        content = parts[3]

        # Parse the datetime
        scheduled_time = parse_datetime(date_str, time_str)

        # Schedule the message
        await schedule_message(message.bot, message.chat.id, scheduled_time, "Blablabla")

        await message.answer(f"Message scheduled for {scheduled_time.strftime('%d/%m/%Y %H:%M')}")
    except ValueError as e:
        await message.answer(str(e))
    except Exception as e:
        await message.answer(f"An error occurred: {str(e)}")

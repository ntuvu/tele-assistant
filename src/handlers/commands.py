import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.handlers.decorators import admin_only
from src.handlers.services import get_hello_message, get_chat_info, handle_schedule_command

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("hello"))
@admin_only
async def hello_command(message: Message) -> None:
    """
    Handle the /hello command
    """
    try:
        response: str = await get_hello_message()
        await message.answer(response)
    except Exception as e:
        logger.error(f"Error handling /hello command: {e}", exc_info=True)
        await message.answer("Sorry, something went wrong while processing the hello command.")


@router.message(Command("info"))
async def info_command(message: Message) -> None:
    """
    Handle the /info command - returns chat ID and user ID
    """
    try:
        chat_id: int = message.chat.id
        user_id: int = message.from_user.id
        response: str = await get_chat_info(chat_id, user_id)
        await message.answer(response)
    except Exception as e:
        logger.error(f"Error handling /info command for chat {message.chat.id}: {e}", exc_info=True)
        await message.answer("Sorry, something went wrong while processing the info command.")


@router.message(Command("schedule"))
@admin_only
async def schedule_command_handler(message: Message) -> None:
    """
    Handle the /schedule command by calling the service function.
    Format: /schedule dd/MM/yyyy HH:mm message
    """
    try:
        # Call the service function to handle the logic
        response_message = await handle_schedule_command(message)
        # Send the response returned by the service function
        await message.answer(response_message)
    except Exception as e:
        # Catch any unexpected errors not handled by the service layer
        logger.error(f"Critical error in schedule_command_handler for chat {message.chat.id}: {e}", exc_info=True)
        await message.answer("A critical error occurred while trying to schedule the message.")

# Ensure you have necessary imports like Bot if needed by other functions in this file

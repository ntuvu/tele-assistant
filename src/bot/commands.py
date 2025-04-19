import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from src.decorator.admin_only import admin_only
from src.service.services import get_chat_info, handle_schedule_command, fetch_weather_by_city, fetch_weather_by_coords

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("hello"))
@admin_only
async def hello_command(message: Message) -> None:
    """
    Handle the /hello command
    """
    try:
        response: str = "Hello, I'm good"
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
        logger.error(f"Error handling /info command for chat {message.chat.id}: {e}", exc_info=True, )
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
        logger.error(f"Critical error in schedule_command_handler for chat {message.chat.id}: {e}", exc_info=True, )


@router.message(Command("weather"))
async def weather_command(message: Message) -> None:
    """
    /weather command: if city is given, shows weather for city.
    Otherwise, asks for location and handles weather based on it.
    """
    try:
        args = message.text.split(maxsplit=1)
        if len(args) > 1:
            city = args[1].strip()
            await message.answer("Looking up the weather...")
            weather_info = await fetch_weather_by_city(city)
            await message.answer(weather_info)
        else:
            keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Send location", request_location=True)]],
                                           resize_keyboard=True, one_time_keyboard=True, )
            await message.answer("Please share your location to get weather info.", reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error in /weather command: {e}", exc_info=True)
        await message.answer("Sorry, something went wrong with the weather request.")


@router.message(lambda message: message.location is not None)
async def weather_by_location(message: Message) -> None:
    """
    Handle any incoming location message by sending weather for that location.
    """
    try:
        latitude = message.location.latitude
        longitude = message.location.longitude
        await message.answer("Checking local weather...")
        weather_info = await fetch_weather_by_coords(latitude, longitude)
        await message.answer(weather_info)
    except Exception as e:
        logger.error(f"Error getting weather for location: {e}", exc_info=True)
        await message.answer("Sorry, could not process your location for weather.")

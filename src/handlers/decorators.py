from functools import wraps
from aiogram.types import Message
from src.config import ADMIN_ID


def admin_only(func):
    """
    Decorator to check if the user is an admin
    """

    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        if message.from_user.id != int(ADMIN_ID):
            await message.answer("Chỉ có anh Tú mới được dùng con bot này thôi 😎")
            return None
        return await func(message, *args, **kwargs)

    return wrapper

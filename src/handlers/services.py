from typing import Tuple


async def get_hello_message() -> str:
    """
    Get the hello message
    """
    return "Hello!"


async def get_chat_info(chat_id: int, user_id: int) -> str:
    """
    Get formatted chat information
    """
    return f"Chat ID: {chat_id}\nUser ID: {user_id}"

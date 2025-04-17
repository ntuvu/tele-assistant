import json
from datetime import datetime
from typing import List, Dict, Any

STORAGE_FILE = "scheduled_messages.json"


def load_scheduled_messages() -> List[Dict[str, Any]]:
    """
    Load scheduled messages from storage file
    """
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_scheduled_messages(messages: List[Dict[str, Any]]) -> None:
    """
    Save scheduled messages to storage file
    """
    with open(STORAGE_FILE, "w") as f:
        json.dump(messages, f, default=str)


def add_scheduled_message(chat_id: int, scheduled_time: datetime, message: str, job_id: str) -> None:
    """
    Add a new scheduled message to storage
    """
    messages = load_scheduled_messages()
    messages.append(
        {"chat_id": chat_id, "scheduled_time": scheduled_time.isoformat(), "message": message, "job_id": job_id}
    )
    save_scheduled_messages(messages)


def remove_scheduled_message(job_id: str) -> None:
    """
    Remove a scheduled message from storage
    """
    messages = load_scheduled_messages()
    messages = [msg for msg in messages if msg["job_id"] != job_id]
    save_scheduled_messages(messages)

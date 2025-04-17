from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from aiogram import Bot
from src.handlers.storage import load_scheduled_messages, add_scheduled_message, remove_scheduled_message

# Initialize the scheduler
scheduler = AsyncIOScheduler()


def parse_datetime(date_str: str, time_str: str) -> datetime:
    """
    Parse date and time strings into a datetime object
    """
    try:
        date_obj: datetime = datetime.strptime(date_str, "%d/%m/%Y")
        time_obj: datetime = datetime.strptime(time_str, "%H:%M")
        return datetime.combine(date_obj.date(), time_obj.time())
    except ValueError:
        raise ValueError("Invalid date or time format. Please use dd/MM/yyyy for date and HH:mm for time")


async def schedule_message(bot: Bot, chat_id: int, scheduled_time: datetime, message: str) -> None:
    """
    Schedule a message to be sent at a specific time
    """
    job_id = f"msg_{chat_id}_{scheduled_time.timestamp()}"

    # Add job to scheduler
    scheduler.add_job(
        bot.send_message,
        trigger=DateTrigger(run_date=scheduled_time),
        args=[chat_id, message],
        id=job_id,
    )

    # Store the scheduled message
    add_scheduled_message(chat_id, scheduled_time, message, job_id)


async def restore_scheduled_messages(bot: Bot) -> None:
    """
    Restore scheduled messages from storage
    """
    messages = load_scheduled_messages()
    current_time = datetime.now()

    for msg in messages:
        scheduled_time = datetime.fromisoformat(msg["scheduled_time"])
        # Only restore messages that are in the future
        if scheduled_time > current_time:
            job_id = msg["job_id"]
            scheduler.add_job(
                bot.send_message,
                trigger=DateTrigger(run_date=scheduled_time),
                args=[msg["chat_id"], msg["message"]],
                id=job_id,
            )


def start_scheduler() -> None:
    """
    Start the scheduler
    """
    scheduler.start()

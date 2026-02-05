from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application
from src.database import get_all_birthdays_for_check
from datetime import datetime, date, timedelta
import asyncio

async def check_birthdays(application: Application):
    print("Checking birthdays...")
    birthdays = get_all_birthdays_for_check()
    today = date.today()
    
    for b in birthdays:
        # b: (id, chat_id, name, birth_date, reminder_days)
        bid, chat_id, name, birth_date_str, reminder_days = b
        
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            continue

        # Calculate next birthday
        try:
            next_birthday = birth_date.replace(year=today.year)
        except ValueError:
            # Handle Feb 29 on non-leap years
            next_birthday = birth_date.replace(year=today.year, month=3, day=1)

        if next_birthday < today:
            try:
                next_birthday = birth_date.replace(year=today.year + 1)
            except ValueError:
                next_birthday = birth_date.replace(year=today.year + 1, month=3, day=1)
        
        # Calculate notification date
        notification_date = next_birthday - timedelta(days=reminder_days)
        
        if notification_date == today:
            msg = f"🎂 ¡Recordatorio! El cumpleaños de {name} es en {reminder_days} días ({next_birthday.strftime('%d/%m')})."
            if reminder_days == 0:
                msg = f"🎂 ¡Hoy es el cumpleaños de {name}!"
            
            try:
                await application.bot.send_message(chat_id=chat_id, text=msg)
            except Exception as e:
                print(f"Error sending message to {chat_id}: {e}")

def start_scheduler(application: Application):
    scheduler = AsyncIOScheduler()
    # Check every day at 09:00 AM
    scheduler.add_job(check_birthdays, 'cron', hour=9, minute=0, args=[application])
    # Also check on startup for debugging/testing purposes (optional, maybe remove for prod)
    # scheduler.add_job(check_birthdays, 'date', run_date=datetime.now() + timedelta(seconds=10), args=[application])
    scheduler.start()

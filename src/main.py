import logging
from telegram.ext import ApplicationBuilder, CommandHandler
from src.config import TELEGRAM_TOKEN
from src.database import init_db
from src.handlers import start, add, list_birthdays, delete
from src.scheduler import start_scheduler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_TOKEN environment variable not set.")
        return

    init_db()
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("list", list_birthdays))
    application.add_handler(CommandHandler("delete", delete))

    # Start scheduler
    start_scheduler(application)
    
    print("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    main()

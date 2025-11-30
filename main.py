import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from config import TOKEN
from handlers.common import start, text_router

logging.basicConfig(level=logging.INFO)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    print("Smart Assistant started")
    app.run_polling()

if __name__ == "__main__":
    main()

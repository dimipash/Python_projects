from typing import Final
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
import logging

"""
A simple Telegram bot that responds to user messages and commands.

This bot demonstrates basic functionalities of a Telegram bot using the
python-telegram-bot library. The bot supports several commands such as /start,
/help, /custom, and /about, and it replies to user messages based on predefined
text patterns. Logging is enabled to track bot activities and errors.

Commands:
- /start: Initiates a conversation with the bot.
- /help: Provides information about available commands.
- /custom: Responds with a custom message.
- /about: Shares details about the bot's purpose.

The bot can handle text messages, responding to specific phrases, and logs all
interactions for easier debugging and monitoring.
"""

# Constants
TOKEN: Final[str] = "YOUR_BOT_TOKEN"
BOT_USERNAME: Final[str] = "@main_cool_bot"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /help to see available commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/custom - Custom command\n"
        "/about - About this bot"
    )
    await update.message.reply_text(help_text)


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command.")


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "This bot is created to demonstrate Telegram bot functionalities."
    )


def handle_response(text: str) -> str:
    processed = text.lower()

    if "hello" in processed:
        return "Hey there!"
    if "how are you" in processed:
        return "I am good."
    if "i love python" in processed:
        return "Python is cool!"
    return "I do not understand..."


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text
    logger.info(f"User ({update.message.chat.id}) in {message_type}: '{text}'")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, "").strip()
            response = handle_response(new_text)
        else:
            return
    else:
        response = handle_response(text)

    logger.info("Bot: %s", response)
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error: {context.error}")


def main():
    logger.info("Starting up the bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("about", about_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    logger.info("Polling...")
    app.run_polling(poll_interval=5)


if __name__ == "__main__":
    main()

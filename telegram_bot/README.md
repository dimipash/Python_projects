# Telegram Bot

A simple Telegram bot built with Python and the python-telegram-bot library. This bot demonstrates basic functionalities such as responding to commands and handling messages.

## Features

- Responds to basic commands (`/start`, `/help`, `/custom`, `/about`)
- Handles text messages and provides responses based on the message content
- Works in both private chats and group chats
- Logging functionality for monitoring bot activities

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone this repository.

2. Install the required packages:

   ```
   pip install python-telegram-bot
   ```

3. Create a new bot on Telegram:

   - Open Telegram and search for the BotFather.
   - Start a chat and send the command `/newbot`.
   - Follow the prompts to create your bot.
   - Save the API token provided by BotFather.

4. Configure the bot:
   - Open `main.py` in a text editor.
   - Replace `"YOUR_BOT_TOKEN"` with the API token you received from BotFather.
   - Update `BOT_USERNAME` with your bot's username.

## Usage

To run the bot, execute the following command in your terminal:

```
python main.py
```

The bot will start running, and you'll see "Starting up the bot..." and "Polling..." messages in the console.

## Available Commands

- `/start`: Starts the bot and displays a welcome message
- `/help`: Shows a list of available commands
- `/custom`: Demonstrates a custom command
- `/about`: Displays information about the bot

## Customization

You can customize the bot's behavior by modifying the following functions:

- `handle_response(text: str) -> str`: Add or modify responses to specific text inputs.
- `custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE)`: Implement your own custom command.
- Add new command handlers in the `main()` function to expand the bot's capabilities.

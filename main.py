import logging
import os
from openai import OpenAI

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Retrieve API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=openai_api_key)

if not openai_api_key or not telegram_token:
    logging.error(
        "API keys are not set correctly. Please check your environment variables.")
    exit(1)


# Constants for OpenAI API parameters
MAX_TOKENS = 50
TEMPERATURE = 0.5


async def start(update: Update, context: CallbackContext):
    """Sends a welcome message when the command /start is issued."""
    message = "Welcome to Awan Telegram Bot, Powered by ChatGPT"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def handle_message(update: Update, context: CallbackContext):
    """Handles user messages and generates responses using ChatGPT."""
    user_message = update.message.text
    chat_id = update.message.chat_id

    try:
        # Generate ChatGPT response using the new API
        response = client.chat.completions.create(model="gpt-3.5-turbo",
                                                  messages=[
                                                      {"role": "system",
                                                          "content": "You are a helpful assistant."},
                                                      {"role": "user",
                                                          "content": user_message},
                                                  ],
                                                  max_tokens=MAX_TOKENS,
                                                  temperature=TEMPERATURE)

        chatgpt_reply = response.choices[0].message.content.strip()
        # Send the response to the user
        await context.bot.send_message(chat_id=chat_id, text=chatgpt_reply)
    except Exception as e:
        logging.error(f"Error generating reply: {e}")
        await context.bot.send_message(chat_id=chat_id, text="Sorry, I couldn't process that request.")


def main():
    """Sets up the Telegram bot and starts the polling loop."""
    application = ApplicationBuilder().token(telegram_token).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()

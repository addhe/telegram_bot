import logging
import os
from openai import OpenAI
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, MessageHandler, filters

# Set up logging
logging.basicConfig(level=logging.INFO)

# Retrieve API keys
openai_api_key = os.getenv("OPENAI_API_KEY")
telegram_token = os.getenv("TELEGRAM_TOKEN")

client = OpenAI(api_key=openai_api_key)

if not openai_api_key or not telegram_token:
    logging.error(
        "API keys are not set correctly. Please check your environment variables."
    )
    exit(1)

# Constants for OpenAI API parameters
MAX_TOKENS = 2000
TEMPERATURE = 0.5

# In-memory storage for conversation history
conversation_histories = {}


async def start(update: Update, context: CallbackContext):
    """Sends a welcome message when the command /start is issued."""
    message = "Welcome to Awan Telegram Bot, Powered by ChatGPT"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)


async def handle_message(update: Update, context: CallbackContext):
    """Handles user messages and generates responses using ChatGPT, while maintaining conversation context."""
    user_message = update.message.text
    chat_id = update.message.chat_id
    bot_username = context.bot.username  # Retrieve bot username from context

    logging.info(f"Received message: {user_message}")

    if update.effective_chat.type in [Chat.GROUP, Chat.SUPERGROUP]:
        if f'@{bot_username}' not in user_message:
            logging.info("Bot not mentioned, ignoring message.")
            return  # Only respond to messages that mention the bot

    # Initialize or update conversation history
    if chat_id not in conversation_histories:
        conversation_histories[chat_id] = [
            {"role": "system",
                "content": "You are a helpful assistant. Your name AiAnakTitipanBot"}
        ]

    # Add the user's message to the conversation history
    conversation_histories[chat_id].append(
        {"role": "user", "content": user_message})

    try:
        # Generate ChatGPT response using the new API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_histories[chat_id],
            max_tokens=MAX_TOKENS,  # Increase max tokens if necessary
            temperature=TEMPERATURE,
            stream=False,
        )

        logging.debug(f"Full API response: {response}")

        # Extract the response content correctly
        chatgpt_reply = response.choices[0].message.content.strip()
        logging.info(f"Generated reply: {chatgpt_reply}")

        # Add the bot's reply to the conversation history
        conversation_histories[chat_id].append(
            {"role": "assistant", "content": chatgpt_reply})

        # Split long messages if needed and send them in parts
        for i in range(0, len(chatgpt_reply), 4000):  # 4000 characters per message
            await context.bot.send_message(chat_id=chat_id, text=chatgpt_reply[i:i+4000])
    except Exception as e:
        logging.error(f"Error generating reply: {e}")
        await context.bot.send_message(
            chat_id=chat_id, text="Sorry, I couldn't process that request."
        )


def main():
    """Sets up the Telegram bot and starts the polling loop."""
    application = ApplicationBuilder().token(telegram_token).build()

    # Register command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()

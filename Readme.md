# Awan Telegram Bot

This is a simple Telegram bot that uses the OpenAI ChatGPT API to generate responses to user messages.

# Features

Responds to user messages using the ChatGPT language model.
Basic welcome message on the /start command.
Error handling for API requests.

# Prerequisites

* Python 3.7 or higher
* OpenAI API Key: You'll need an API key from OpenAI to use the ChatGPT model.
  * Create an account on https://platform.openai.com/
  * Get your API key from https://platform.openai.com/account/api-keys
* Telegram Bot Token: Create a new bot using the BotFather on Telegram and obtain its token.
  * Search for @BotFather on Telegram and follow the instructions to create a new bot.

# Installation

1. Clone the repository:

   ```
   $ git clone https://github.com/addhe/telegram_bot.git
   $ cd telegram_bot
   ```
2. Create a virtual environment (recommended):

   ```
   $ python3 -m venv env
   $ source env/bin/activate
   ```
3. Install the required packages:
   ```
   $ pip install -r requirements.txt
   ```
4. Set environment variables:
   * Create a .env file in the root directory of the project.
   * Add your OpenAI API key and Telegram bot token to the .env file:
   ```
   OPENAI_API_KEY=your_openai_api_key
   TELEGRAM_TOKEN=your_telegram_bot_token
   ```

**Running the Bot**

1. Start the bot:
   ```
   $ python main.py
   ```
2. Interact with your bot:
   * Open Telegram and search for your bot's username.
   * Send messages to the bot and receive responses generated by ChatGPT.

**Customization**
* MAX_TOKENS (in main.py): Adjusts the maximum length of the ChatGPT responses.
* TEMPERATURE (in main.py): Controls the randomness and creativity of the ChatGPT output.

**Disclaimer**
This bot is provided as a basic example and may require further development and customization to suit your specific needs.

# Discord Chat Bot (Flask-free `:)` )
A modular, async Discord chatbot built using discord.py and JSON-based knowledge retrieval. The bot responds to user queries by searching a knowledge base and returns answers with confidence scores.

## Features
-  **Asynchronous message handling** - Non-blocking, real-time responses
-  **JSON-based knowledge base** - Easy to add Q&A entries
-  **Auto-reload** - Changes to knowledge base take effect immediately
- **Command & mention support** - Use `!ask` commands or mention the bot

## Tech Stack
Python, discord.py, asyncio, JSON, python-dotenv, aiohttp

## Setup Instructions
### 1. Clone the Repository
git clone https://github.com/DKAT-9/Discord-Chat-Bot.git

### 2. Create Virtual Environment
python3 -m venv .venv
source .venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Set Up Discord Bot Token
Edit `.env` and replace `your_discord_bot_token_here` with your actual token:


### 5. Run the Bot
.venv/bin/python -m bot.bot

### Mentions
Mention the bot with a question:
@MacQueen How do I budget my money?

## Contributing
Feel free to fork and add more features or improve the knowledge base!

## License
MIT License - Feel free to use and modify as needed.

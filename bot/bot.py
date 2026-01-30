from __future__ import annotations
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from utils.kb import KnowledgeBase
from utils.http import HTTPClient
from utils.cogs.chat import ChatCog
from utils.cogs.app import AdminCog

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")

if not TOKEN:
    raise RuntimeError(
        " Configuration Error: DISCORD_TOKEN not found in .env file. "
        "Please create a .env file with your Discord bot token."
    )

intents = discord.Intents.default()
intents.message_content = True  # needed for reading message content

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

kb = KnowledgeBase("data/knowledge_base.json")
http = HTTPClient(timeout_seconds=8)

@bot.event
async def on_ready():
    if bot.user:
        print(f"Logged in as {bot.user} (id={bot.user.id})")
    else:
        print("Bot logged in but user info is unavailable")

@bot.event
async def setup_hook():
    # Start shared HTTP session once (optimization)
    await http.start()

    # Load modular command cogs
    await bot.add_cog(ChatCog(bot, kb, http))
    await bot.add_cog(AdminCog(bot))

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
        return
    await ctx.reply(f"❌ Command Error: {type(error).__name__}\n`{error}`")

async def close_resources():
    await http.close()

def main():
    try:
        assert TOKEN is not None  # guaranteed by check above
        bot.run(TOKEN)  # type: ignore
    finally:
        # best-effort cleanup
        try:
            import asyncio
            asyncio.run(close_resources())
        except Exception:
            pass

if __name__ == "__main__":
    main()
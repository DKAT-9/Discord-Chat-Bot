from __future__ import annotations
import time
import discord
from discord.ext import commands

from utils.kb import KnowledgeBase
from utils.http import HTTPClient

class ChatCog(commands.Cog):
    def __init__(self, bot: commands.Bot, kb: KnowledgeBase, http: HTTPClient):
        self.bot = bot
        self.kb = kb
        self.http = http

    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, question: str):
        """Query the JSON knowledge base with simple confidence scoring."""
        start = time.perf_counter()
        match = self.kb.search(question)
        elapsed_ms = (time.perf_counter() - start) * 1000

        if not match:
            await ctx.reply(
                "❓ I couldn't find a confident match. Try rephrasing your question or ask about topics like budgeting, saving, emergency funds, or compound interest."
            )
            return

        entry, score = match
        await ctx.reply(f"**{entry.question}**\n{entry.answer}\n\n_Confidence: {score:.0%} • lookup: {elapsed_ms:.1f}ms_")

    @commands.command(name="pingapi")
    async def pingapi(self, ctx: commands.Context):
        """
        Demonstrates optimized async HTTP call via shared aiohttp session + caching.
        Uses a public JSON endpoint.
        """
        start = time.perf_counter()
        data = await self.http.get_json("https://api.github.com/rate_limit", ttl_seconds=20)
        elapsed_ms = (time.perf_counter() - start) * 1000

        core = data.get("resources", {}).get("core", {})
        remaining = core.get("remaining", "?")
        limit = core.get("limit", "?")

        await ctx.reply(f"GitHub API rate limit: {remaining}/{limit} (fetched in {elapsed_ms:.1f}ms)")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
        Real-time user input processing.
        If someone mentions the bot, try KB answer.
        """
        if message.author.bot:
            return
        if self.bot.user and self.bot.user.mentioned_in(message):
            text = message.content.replace(f"<@{self.bot.user.id}>", "").strip()
            if not text:
                await message.reply("👋 Hi! Please mention me with a question, or use `!ask <question>`.")
                return

            match = self.kb.search(text)
            if match:
                entry, score = match
                await message.reply(f"{entry.answer}\n\n_Confidence: {score:.0%}_")
            else:
                await message.reply("❓ I'm not confident about that one. Try `!ask` with more details or rephrase your question.")
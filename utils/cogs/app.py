from __future__ import annotations
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="sync")
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """Optional: placeholder for future slash-command sync patterns."""
        await ctx.reply("Admin command system ready. (Add slash commands later if you want.)")
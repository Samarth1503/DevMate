import discord
from discord.ext import commands

from core.config import settings


class GeneralCog(commands.Cog):
    """A Cog containing general message listeners and commands."""

    def __init__(self, bot):
        self.bot = bot

    async def _send_command_list(self, channel):
        p = settings.command_prefix
        embed = discord.Embed(
            title="DevMate Commands",
            description="Here is everything I can do:",
            color=discord.Color.teal(),
        )
        embed.add_field(
            name="🤖 General",
            value=(
                f"`{p}commands` or `{p}list` — Show this list\n"
                f"`{p}hello` — Greet the bot"
            ),
            inline=False,
        )
        embed.add_field(
            name="📊 Analytics",
            value=f"`{p}stats` — View real-time developer analytics",
            inline=False,
        )
        embed.add_field(
            name="🚀 GitHub",
            value=(
                f"`{p}repo <owner> <repo>` — View repository info\n"
                f"`{p}commits <owner> <repo>` — View recent commits"
            ),
            inline=False,
        )
        embed.add_field(
            name="🧠 AI & Knowledge Base",
            value=(
                f"`{p}ask <question>` — Ask the AI a question\n"
                f"`{p}debug <error>` — Analyze a stack trace\n"
                f"`{p}remember <id> <text>` — Save knowledge\n"
                f"`{p}search <query>` — Search the knowledge base"
            ),
            inline=False,
        )
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Triggered every time a message is sent."""
        if message.author == self.bot.user:
            return

        # A bare prefix (e.g. just '$') shows the command list.
        if message.content.strip() == settings.command_prefix:
            await self._send_command_list(message.channel)
            return

        if message.content.startswith(f"{settings.command_prefix}hello"):
            await message.channel.send("Hello!")

    @commands.command(name="commands", aliases=["list"])
    async def commands_command(self, ctx):
        """Show the list of commands."""
        await self._send_command_list(ctx.channel)


async def setup(bot):
    await bot.add_cog(GeneralCog(bot))

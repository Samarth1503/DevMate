import asyncio
import logging

import discord
from cogwatch import watch
from discord.ext import commands

from core.config import settings
from database.connection import db

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


class DevMateBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix=settings.command_prefix, intents=intents)

    @watch(path="cogs", preload=True)
    async def on_ready(self):
        logging.info(f"Logged in as {self.user} (ID: {self.user.id})")
        logging.info("Bot is ready.")

    async def setup_hook(self):
        # Initialize database connection pool
        await db.connect()

    async def close(self):
        # Close database connection pool
        await db.disconnect()
        await super().close()


async def main():
    bot = DevMateBot()
    async with bot:
        await bot.start(settings.discord_bot_token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot shutting down manually.")

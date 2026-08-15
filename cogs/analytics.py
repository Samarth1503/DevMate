import discord
from discord.ext import commands

from database.connection import db


class AnalyticsCog(commands.Cog):
    """Cog for developer analytics and metrics."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if not db.pool:
            return

        guild_id = message.guild.id if message.guild else None

        async with db.pool.acquire() as conn:
            # Update user activity
            await conn.execute(
                """
                INSERT INTO user_activity (user_id, guild_id, message_count)
                VALUES ($1, $2, 1)
                ON CONFLICT (user_id, guild_id)
                DO UPDATE SET
                    message_count = user_activity.message_count + 1,
                    last_active = CURRENT_TIMESTAMP
                """,
                message.author.id,
                guild_id,
            )

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        if not db.pool:
            return

        guild_id = ctx.guild.id if ctx.guild else None

        async with db.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO command_metrics (command_name, user_id, guild_id)
                VALUES ($1, $2, $3)
                """,
                ctx.command.name,
                ctx.author.id,
                guild_id,
            )

    @commands.command(name="stats")
    async def stats(self, ctx):
        """View real-time developer analytics for the server."""
        if not db.pool:
            await ctx.send("Database connection is not available.")
            return

        guild_id = ctx.guild.id if ctx.guild else None

        async with db.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT SUM(message_count) as total_messages, COUNT(*) as active_users
                FROM user_activity
                WHERE guild_id = $1
                """,
                guild_id,
            )

            cmd_row = await conn.fetchrow(
                """
                SELECT COUNT(*) as total_commands
                FROM command_metrics
                WHERE guild_id = $1
                """,
                guild_id,
            )

            total_msg = row["total_messages"] or 0
            active_users = row["active_users"] or 0
            total_cmd = cmd_row["total_commands"] or 0

            embed = discord.Embed(title="Server Analytics", color=discord.Color.blue())
            embed.add_field(name="Total Messages", value=str(total_msg), inline=True)
            embed.add_field(name="Active Users", value=str(active_users), inline=True)
            embed.add_field(name="Commands Executed", value=str(total_cmd), inline=True)

            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AnalyticsCog(bot))

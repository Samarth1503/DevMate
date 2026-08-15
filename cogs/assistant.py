import discord
from discord.ext import commands

from services.chroma_service import vector_store
from services.gemini_service import llm_service


class AssistantCog(commands.Cog):
    """Cog for AI Developer Assistant and Knowledge Base."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="debug")
    async def debug(self, ctx, *, error_message: str):
        """Analyze an error message using the AI. Usage: $debug <error message>"""
        await ctx.send("Analyzing error...")
        analysis = await llm_service.analyze_error(
            error_message, "Stack trace not provided."
        )

        # Discord has a 2000 character limit
        if len(analysis) > 1900:
            analysis = analysis[:1900] + "...\n[Analysis truncated]"

        await ctx.send(f"**AI Analysis:**\n{analysis}")

    @commands.command(name="ask")
    async def ask(self, ctx, *, prompt: str):
        """Ask a general programming question. Usage: $ask <question>"""
        await ctx.send("Thinking...")
        response = await llm_service.generate_response(prompt)

        if len(response) > 1900:
            response = response[:1900] + "...\n[Response truncated]"

        await ctx.send(f"**AI:**\n{response}")

    @commands.command(name="remember")
    async def remember(self, ctx, doc_id: str, *, text: str):
        """Store knowledge in the vector database. Usage: $remember <id> <text>"""
        await vector_store.add_document(doc_id, text)
        await ctx.send(f"Knowledge stored under ID: `{doc_id}`")

    @commands.command(name="search")
    async def search(self, ctx, *, query: str):
        """Search the knowledge base. Usage: $search <query>"""
        results = await vector_store.search(query, n_results=3)
        if not results:
            await ctx.send("No relevant knowledge found.")
            return

        embed = discord.Embed(
            title="Knowledge Base Search", color=discord.Color.purple()
        )
        for res in results:
            doc = res["document"]
            embed.add_field(
                name=f"ID: {res['id']}",
                value=doc[:200] + ("..." if len(doc) > 200 else ""),
                inline=False,
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(AssistantCog(bot))

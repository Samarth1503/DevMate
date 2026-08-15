import discord
from discord.ext import commands

from services.github import github_service


class GitHubCog(commands.Cog):
    """Cog for GitHub integration."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="repo")
    async def repo_info(self, ctx, owner: str, repo: str):
        """Fetch repository information. Usage: $repo owner repo"""
        data = await github_service.get_repository(owner, repo)

        if "error" in data:
            await ctx.send(f"Error: {data['error']}")
            return

        embed = discord.Embed(
            title=data.get("full_name"),
            url=data.get("html_url"),
            color=discord.Color.green(),
        )
        embed.description = data.get("description", "No description provided.")
        embed.add_field(
            name="Stars", value=data.get("stargazers_count", 0), inline=True
        )
        embed.add_field(name="Forks", value=data.get("forks_count", 0), inline=True)
        embed.add_field(
            name="Open Issues", value=data.get("open_issues_count", 0), inline=True
        )

        await ctx.send(embed=embed)

    @commands.command(name="commits")
    async def recent_commits(self, ctx, owner: str, repo: str):
        """Fetch recent commits. Usage: $commits owner repo"""
        commits = await github_service.get_recent_commits(owner, repo)

        if not commits:
            await ctx.send("No commits found or error fetching commits.")
            return

        embed = discord.Embed(
            title=f"Recent Commits for {owner}/{repo}", color=discord.Color.green()
        )
        for commit in commits[:5]:
            sha = commit.get("sha", "")[:7]
            message = commit.get("commit", {}).get("message", "No message")
            author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
            embed.add_field(
                name=f"`{sha}` by {author}",
                value=message[:100] + ("..." if len(message) > 100 else ""),
                inline=False,
            )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(GitHubCog(bot))

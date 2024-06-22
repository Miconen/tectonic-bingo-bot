import discord
from discord.ext import commands

from bot.utils.images import images
from state.state import state
from utils.teams import in_team

app_commands = discord.app_commands


class Board(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Board command is ready.")

    @app_commands.command(name="board", description="View the board of a team.")
    async def board(self, i: discord.Interaction):
        """View the board of a team."""
        await i.response.defer()

        if i.channel is None:
            res = "Submission channel is not available."
            return await i.followup.send(res, ephemeral=True)

        if not isinstance(i.channel, discord.TextChannel):
            res = "Submission channel is not a text channel."
            return await i.followup.send(res, ephemeral=True)

        if not isinstance(i.user, discord.Member):
            res = f"Command not available in DMs."
            return await i.followup.send(res, ephemeral=True)

        team = in_team(i.user, state.teams)
        if team is None:
            res = f"You are not in a bingo team, if you think this is a mistake, please contact an admin"
            return await i.followup.send(res, ephemeral=True)

        team_name = state.teams[team].get_name()

        image = images.get_image(team)
        if not image:
            res = f"Board for {team_name} is not available."
            return await i.followup.send(res)

        await i.followup.send(f"Board for {team_name}.", files=[image])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Board(bot))

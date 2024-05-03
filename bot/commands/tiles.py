import discord
from discord.ext import commands

from state.state import state
from utils.teams import in_team
from bot.utils.getters import get_tiles_embed

app_commands = discord.app_commands


class Tiles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("List command is ready.")

    @app_commands.command(name="tiles", description="List all unlocked tiles")
    async def tiles(self, i: discord.Interaction):
        """List all unlocked tiles."""
        if i.channel is None:
            return
        if not isinstance(i.channel, discord.TextChannel):
            return
        if not isinstance(i.user, discord.Member):
            return

        team = in_team(i.user, state.teams)
        if team is None:
            await i.response.send_message(
                f"You are not in a team (Teams: {len(state.teams)})"
            )
            return

        board = state.teams[team].board
        unlocked_tiles = [
            node.value for node in board.values() if node.value.is_unlocked()
        ]

        embed = get_tiles_embed(i, state.teams[team], unlocked_tiles)

        await i.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tiles(bot))

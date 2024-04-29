import discord
from discord.ext import commands

from state.state import state
from utils.teams import in_team
from bot.utils import get_tile_embed

app_commands = discord.app_commands


class List(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("List command is ready.")

    @app_commands.command(name="list", description="List all unlocked tiles")
    async def list(self, i: discord.Interaction):
        """List all unlocked tiles."""
        if i.channel is None:
            return
        if not isinstance(i.channel, discord.TextChannel):
            return

        team = in_team(i.user.id, state.teams)
        if team is None:
            await i.response.send_message(
                f"You are not in a team (Teams: {len(state.teams)})"
            )
            return

        board = state.teams[team].board
        unlocked_tiles = [
            node.value for node in board.values() if node.value.is_unlocked()
        ]

        for tile in unlocked_tiles:
            embed = get_tile_embed(i, tile)
            await i.channel.send(embed=embed)

        await i.response.send_message(f"Listing all unlocked tiles for team: **{state.teams[team].role.name}**")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(List(bot))

import discord
from discord.ext import commands

from state.state import state
from utils.teams import in_team
from bot.utils import get_tile_embed

app_commands = discord.app_commands


class Tile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Tile command is ready.")

    @app_commands.command(name="tile", description="Get information about a tile")
    @app_commands.describe(tile_id="Tile ID")
    async def tile(
        self, i: discord.Interaction, tile_id: app_commands.Range[int, 1, 36]
    ):
        """Displays inofrmation about a tile if it's unlocked."""
        if i.channel is None:
            return
        if not isinstance(i.channel, discord.TextChannel):
            return

        team = in_team(i.user.id, state.teams)

        if team is None:
            await i.response.send_message(f"You are not in a bingo team")
            return

        board = state.teams[team].board
        tile = next(
            (
                node.value
                for k, node in board.items()
                if node.value.is_unlocked() and k == tile_id
            ),
            None,
        )

        if tile is None:
            await i.response.send_message(
                f"No tile unlocked with ID #{tile_id} for team ({team})"
            )
            return

        embed = get_tile_embed(i, tile)
        await i.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tile(bot))

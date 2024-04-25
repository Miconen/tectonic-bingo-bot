import discord
from discord.ext import commands
import jsonpickle

from state.state import state

# This file houses generic/testing related commands
# ...that aren't a part of the core business logic.


app_commands = discord.app_commands


class Debug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Debug commands are ready.")

    @app_commands.command(name="sync", description="Sync the command tree with Discord")
    async def sync(self, i: discord.Interaction):
        """Sync the command tree with Discord."""
        synced = await self.bot.tree.sync()
        await i.response.send_message(f"Synced {len(synced)} command(s).")

    @app_commands.command(
        name="serialize", description="Serialize the state to a JSON file"
    )
    async def serialize(self, i: discord.Interaction):
        """Test command to serialize the game state to a JSON file."""
        state.serialize()
        await i.response.send_message(
            f"State serialized to JSON file successfully {jsonpickle.encode(state)}"
        )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Debug(bot))

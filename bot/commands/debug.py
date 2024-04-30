import discord
from discord.ext import commands
import jsonpickle

from utils.time import get_relative_time, TimestampType
from state.state import state

# This file houses generic/testing related commands
# ...that aren't a part of the core business logic.


app_commands = discord.app_commands


class Debug(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Debug commands are ready.")

    @app_commands.command(name="sync", description="Sync the command tree with Discord")
    @commands.has_permissions(manage_roles=True)
    async def sync(self, i: discord.Interaction):
        """Sync the command tree with Discord."""
        synced = await self.bot.tree.sync()
        await i.response.send_message(f"Synced {len(synced)} command(s).")

    @app_commands.command(
        name="serialize", description="Serialize the state to a JSON file"
    )
    @commands.has_permissions(manage_roles=True)
    async def serialize(self, i: discord.Interaction):
        """Test command to serialize the game state to a JSON file."""
        state.serialize()
        await i.response.send_message(
            f"State serialized to JSON file successfully {jsonpickle.encode(state)}"
        )

    @app_commands.command(name="proof", description="Get the submitted proof of a tile")
    @commands.has_permissions(manage_roles=True)
    async def proof(
        self,
        i: discord.Interaction,
        team: discord.Role,
        tile_id: app_commands.Range[int, 1, 36],
    ):
        """Get the submitted proof of a tile."""
        tile = state.teams[team.id].board[tile_id].value

        if tile.proof is None:
            return await i.response.send_message(
                f"No proof submitted for tile {tile_id}."
            )

        msg = f"# Proof check for tile {tile_id}"
        proofs = []

        for proof in tile.proof:
            res = ""

            res += f"\n**Team:** {team.name}"
            res += f"\n**Task:** {proof.amount}x {proof.task}"
            res += f"\n**Submitted:** {proof.submitted_by.display_name} {get_relative_time(TimestampType.DATE_TIME_SHORT, proof.submitted_at)} ({get_relative_time(TimestampType.RELATIVE, proof.submitted_at)})"
            if proof.approved_at is not None and proof.approved_by is not None:
                res += f"\n**Approved:** {proof.approved_by.display_name} {get_relative_time(TimestampType.DATE_TIME_SHORT, proof.approved_at)} ({get_relative_time(TimestampType.RELATIVE, proof.approved_at)})"
            if proof.message is not None:
                res += f"\n**Message:** {proof.message.jump_url}"

            proofs.append(res)

        await i.response.send_message(msg + "\n".join(proofs))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Debug(bot))

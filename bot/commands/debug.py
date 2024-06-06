import discord
from discord.ext import commands

from utils.time import get_relative_time, TimestampType
from models.tile import TileState
from state.state import state
from bot.utils.images import images
from bot.utils.getters import get_tile_embed

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
        res = "Forced a game state save to disk"
        await i.response.send_message(res)

    @app_commands.command(name="proof", description="Get the submitted proof of a tile")
    @commands.has_permissions(manage_roles=True)
    async def proof(
        self,
        i: discord.Interaction,
        role: discord.Role,
        tile_id: app_commands.Range[int, 1, 36],
    ):
        """Get the submitted proof of a tile."""
        team = state.get_team(role.id)

        if team is None:
            res = f"Team for role <@&{role.id}> not found"
            return await i.response.send_message(res)

        tile = team.board.get_tile(tile_id)
        if tile is None:
            res = f"Tile #{tile_id} not found for team {role.name}"
            return await i.response.send_message(res)

        if tile.proof is None:
            res = f"No proof submitted for tile #{tile_id}"
            return await i.response.send_message(res)

        msg = f"# Proof check for tile {tile_id}"
        proofs = []

        for proof in tile.proof:
            res = ""

            res += f"\n**Team:** {role.name}"
            res += f"\n**Task:** {proof.amount}x {proof.task}"
            res += f"\n**Submitted:** <@{proof.submitted_by}> {get_relative_time(TimestampType.DATE_TIME_SHORT, proof.submitted_at)} ({get_relative_time(TimestampType.RELATIVE, proof.submitted_at)})"
            if proof.approved_at is not None and proof.approved_by is not None:
                res += f"\n**Approved:** <@{proof.approved_by}> {get_relative_time(TimestampType.DATE_TIME_SHORT, proof.approved_at)} ({get_relative_time(TimestampType.RELATIVE, proof.approved_at)})"
            if proof.message is not None:
                res += f"\n**Message:** {proof.message}"

            proofs.append(res)

        await i.response.send_message(msg + "\n".join(proofs), silent=True)

    @app_commands.command(
        name="undo", description="Undo the last action of a tiles proof"
    )
    @commands.has_permissions(manage_roles=True)
    async def undo(
        self,
        i: discord.Interaction,
        role: discord.Role,
        tile_id: app_commands.Range[int, 1, 36],
    ):
        """Undo the last action of a tile's proof."""
        team = state.get_team(role.id)
        if team is None:
            res = f"Team for role <@&{role.id}> not found"
            return await i.response.send_message(res)

        tile = team.board.get_tile(tile_id)

        if tile is None:
            res = f"Tile #{tile_id} not found for team {role.name}"
            return await i.response.send_message(res)

        if tile.proof is None:
            res = f"No proof submitted for tile #{tile_id}"
            return await i.response.send_message(res)

        if len(tile.proof) == 0:
            res = f"No proof submitted for tile #{tile_id}"
            return await i.response.send_message(res)

        was_completed = tile.check_complete()
        proof = None if len(tile.proof) == 0 else tile.proof[-1]

        if proof is None:
            res = f"Last proof submission for tile {tile_id} not found"
            return await i.response.send_message(res)

        removed = tile.remove_submission(proof)

        if not removed:
            res = f"Last proof submission for tile {tile_id} was not removed"
            return await i.response.send_message(res)

        # Remove the proof from state
        tile.proof.pop()
        msg = f"Proof for tile {tile_id} undone by <@{i.user.id}>"

        # Incomplete the tile if removed submission was required for tile completion
        if not tile.check_complete() and was_completed:
            # Set the tile back to unlocked
            tile.state = TileState.UNLOCKED

            node = team.board.get_node(tile_id)
            team.update_neighboring(
                node, TileState.LOCKED, excludes=[TileState.COMPLETED]
            )

            # Generate updated board
            images.generate_image(team.get_id())

            msg += f"\nTile marked as incomplete and neighbors locked"

        # Save game state
        state.serialize()

        await i.response.send_message(msg, silent=True)


    @app_commands.command(
        name="check", description="Force check a teams tile"
    )
    @commands.has_permissions(manage_roles=True)
    async def undo(
        self,
        i: discord.Interaction,
        role: discord.Role,
        tile_id: app_commands.Range[int, 1, 36],
    ):
        """Forcefully displays inofrmation about a tile."""
        if i.channel is None:
            return
        if not isinstance(i.channel, discord.TextChannel):
            return
        if not isinstance(i.user, discord.Member):
            return

        team = state.get_team(role.id)
        if team is None:
            res = f"Team is not part of the bingo"
            return await i.response.send_message(res, ephemeral=True)

        board = team.board
        tile = next(
            (
                node.value
                for k, node in board.get_nodes().items()
                if k == tile_id
            ),
            None,
        )

        if tile is None:
            res = f"No tile unlocked with ID #{tile_id} for team ({team.get_name()})"
            return await i.response.send_message(res)

        embed = get_tile_embed(i, tile)
        await i.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Debug(bot))

import discord
from discord.ext import commands
from io import BytesIO

from state.state import state
from utils.teams import in_team
from models.tile import TileState
# from bot.utils import get_proof_file

app_commands = discord.app_commands


class Submit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Submit command is ready.")

    @app_commands.command(
        name="submit", description="Submit a task associated with a tile"
    )
    # @app_commands.describe(task="Task to submit for completion")
    @app_commands.describe(proof="Screenshot proof of completion")
    @app_commands.describe(amount="Optional parameter for amount, defaults to one")
    async def submit(
        self,
        i: discord.Interaction,
        task: str,
        proof: discord.Attachment,
        amount: int = 1,
    ):
        """Displays inofrmation about a tile if it's unlocked."""
        if i.channel is None:
            return
        if not isinstance(i.channel, discord.TextChannel):
            return

        # If proof MIME type not of image/jppeg or image/png return
        if proof.content_type not in ["image/jpeg", "image/png"]:
            return await i.response.send_message("Proof must be a .jpeg or .png")

        team = in_team(i.user.id, state.teams)

        if team is None:
            await i.response.send_message(f"You are not in a bingo team")
            return

        # Loop through all visible tiles and check if the task matches any tiles requirements
        match = True
        if not match:
            return

        # Check if the task has already been submitted
        # Get id of GraphNode that includes the tile that includes the task

        id = None
        status = TileState.UNKNOWN
        for tile_id, node in state.teams[team].board.items():
            print(node.value.requirements.keys())
            if task in node.value.requirements.keys():
                if node.value.state == TileState.UNKNOWN:
                    continue
                if node.value.state == TileState.LOCKED:
                    continue

                status = node.value.state

                if node.value.state == TileState.COMPLETED:
                    break

                id = tile_id
                break

        if status == TileState.COMPLETED:
            return await i.response.send_message(
                f"{task} is already completed for {team}"
            )

        if not id:
            return await i.response.send_message(
                f"{task} is not a part of an unlocked tile for {team}"
            )

        team = state.teams[team]
        board = team.board
        node = board[id]
        tile = node.value
        completed = tile.submit(task, amount)

        count = f'{amount}x ' if amount else ''

        # Check if no admins online
        # If no admins online, submit task as pending
        # If admins online, ping and ask to review task

        # We determine the input is successful and valid here, allowing for file parsing
        f = await get_proof_file(proof)
        if isinstance(f, Exception):
            return await i.response.send_message(
                f"Error reading proof: {f}\n\nPlease contact an admin."
            )

        # If task was not completed
        if not completed:
            return await i.response.send_message(
                f"{count}{task} submitted by {i.user.display_name}",
                file=discord.File(
                    fp=f, filename=f'proof.{proof.content_type.split("/")[1]}'
                ),
            )

        # If tile is entirely complete
        if tile.check_complete():
            # Complete the tile
            tile.complete()

            # Unlock neighboring non completed tiles
            node.update_neighbors(TileState.UNLOCKED, ignoring=[TileState.COMPLETED])

            return await i.response.send_message(
                f"{count}{task} completed by {i.user.display_name} completing the tile",
                file=discord.File(
                    fp=f, filename=f'proof.{proof.content_type.split("/")[1]}'
                ),
            )

        # If tile is partially complete
        return await i.response.send_message(
            f"{count}{task} submitted by {i.user.display_name}, partially completing the tile",
            file=discord.File(
                fp=f, filename=f'proof.{proof.content_type.split("/")[1]}'
            ),
        )

async def get_proof_file(proof: discord.Attachment) -> BytesIO | Exception:
    try:
        f = await proof.read()
        return BytesIO(f)
    except Exception as e:
        return e

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Submit(bot))

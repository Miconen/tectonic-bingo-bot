from dataclasses import dataclass
import discord
from discord.ext import commands
from io import BytesIO
from typing import Dict

from models.graph import GraphNode
from state.state import state
from utils.teams import in_team
from models.tile import TileState, Tile
from models.team import Team
from bot.utils import get_tile_embed, get_submission_message

app_commands = discord.app_commands


@dataclass
class Submission:
    team: Team
    board: Dict[int, GraphNode]
    node: GraphNode
    i: discord.Interaction
    tile: Tile
    amount: int
    task: str


async def accept_submission(submission: Submission):
    message = ""
    completion = submission.tile.submit(submission.task, submission.amount)

    # If task was not completed
    if not completion:
        message = "Submission successful! Did not complete the tile or task."

    # If tile is not entirely complete
    if completion:
        message = "Task completed! This tile is now completed partially."

    # If tile is entirely complete
    if submission.tile.check_complete():
        message = "Tile completed! Unlocking new tiles!"

        # Complete the tile
        submission.tile.complete()

    return get_submission_message(
        submission.i,
        submission.tile,
        message,
        "✅ Submission approved",
        submission.amount,
        submission.task,
    )


async def deny_submission(submission: Submission):
    message = ""
    completion = submission.tile.submit(submission.task, submission.amount)

    # If task was not completed
    if not completion:
        message = "This would have partially completed a task."

    # If tile is not entirely complete
    if completion:
        message = "This would have completed a task, partially completing the tile."

    # If tile is entirely complete
    if submission.tile.check_complete():
        message = "This would have completed the tile, unlocking new tiles."

    return get_submission_message(
        submission.i,
        submission.tile,
        message,
        "❌ Submission denied",
        submission.amount,
        submission.task,
    )


class Buttons(discord.ui.View):
    def __init__(self, submission: Submission, timeout=180):
        super().__init__(timeout=timeout)
        self.submission = submission

    @discord.ui.button(
        custom_id="accept", label="Accept", style=discord.ButtonStyle.green
    )
    async def accept_button(self, i: discord.Interaction, button: discord.ui.Button):
        if self.submission.i.channel is None:
            return
        if not isinstance(self.submission.i.channel, discord.TextChannel):
            return

        await i.response.edit_message(
            content=await accept_submission(self.submission), view=None
        )

        # Unlock neighboring non completed tiles
        new_tiles = self.submission.team.update_neighboring(
            self.submission.node, TileState.UNLOCKED, filter=[TileState.COMPLETED]
        )

        for tile in new_tiles:
            embed = get_tile_embed(i, tile)
            await self.submission.i.channel.send("**New tile unlocked!**", embed=embed)

    @discord.ui.button(custom_id="deny", label="Deny", style=discord.ButtonStyle.red)
    async def deny_button(self, i: discord.Interaction, button: discord.ui.Button):
        if self.submission.i.channel is None:
            return
        if not isinstance(self.submission.i.channel, discord.TextChannel):
            return

        await i.response.edit_message(
            content=await deny_submission(self.submission), view=None
        )


class Submit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Submit command is ready.")

    @app_commands.command(
        name="submit", description="Submit a task associated with a tile"
    )
    @app_commands.describe(task="Task to submit for completion")
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
            return await i.response.send_message(
                "Proof must be a .jpeg or .png, if you think this is a mistake, please try again or contact an admin"
            )

        team = in_team(i.user.id, state.teams)

        if team is None:
            await i.response.send_message(
                f"You are not in a bingo team, if you think this is a mistake, please contact an admin",
                ephemeral=True,
            )
            return

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

        # Check if the task has already been submitted
        if status == TileState.COMPLETED:
            return await i.response.send_message(
                f"{task} is already completed for {team}"
            )

        if not id:
            return await i.response.send_message(
                f"{task} is not a part of an unlocked tile for {team}"
            )

        submission = Submission(
            team=state.teams[team],
            board=state.teams[team].board,
            node=state.teams[team].board[id],
            tile=state.teams[team].board[id].value,
            amount=amount,
            task=task,
            i=i,
        )

        # We determine the input is successful and valid here, allowing for file parsing
        f = await get_proof_file(proof)
        if isinstance(f, Exception):
            return await i.response.send_message(
                f"Error reading proof: {f}\n\nPlease contact an admin."
            )

        message = ""

        # If task was not completed
        if not submission.tile.would_complete_task(task, amount):
            message = "This would complete a part of a task."

        # If tile is not entirely complete
        if submission.tile.would_complete_task(task, amount):
            message = "This would complete a task, partially completing the tile."

        # If tile is entirely complete
        if submission.tile.would_complete_tile(task, amount):
            message = "This would complete the tile, unlocking new tiles."

        await i.response.send_message(
            get_submission_message(
                i, submission.tile, message, "⌛ Pending approval...", amount, task
            ),
            file=discord.File(
                fp=f, filename=f'proof.{proof.content_type.split("/")[1]}'
            ),
            view=Buttons(submission),
        )


async def get_proof_file(proof: discord.Attachment) -> BytesIO | Exception:
    try:
        f = await proof.read()
        return BytesIO(f)
    except Exception as e:
        return e


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Submit(bot))
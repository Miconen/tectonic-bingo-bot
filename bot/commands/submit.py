from time import time
from dataclasses import dataclass
import discord
from discord.ext import commands
from io import BytesIO

from models.graph import GraphNode
from models.board import Board
from state.state import state
from utils.teams import in_team
from models.tile import TileState, Tile, Proof
from models.team import Team
from bot.utils.getters import (
    get_unlock_embed,
    get_submission_message,
    get_tile_state_by_task,
    get_tile_id_by_task,
)
from bot.utils.images import images

app_commands = discord.app_commands


@dataclass
class Submission:
    team: Team
    board: Board
    node: GraphNode
    i: discord.Interaction
    proof_index: int
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

        # Unlock neighboring non completed tiles
        new_tiles = submission.team.update_neighboring(
            submission.node, TileState.UNLOCKED, excludes=[TileState.COMPLETED]
        )

        if len(new_tiles) == 0:
            return

        # Generate updated board
        images.generate_image(submission.team.get_id())

        embed = get_unlock_embed(submission.i, submission.team, new_tiles)

        # Check if is text channel
        if submission.i.channel is None:
            return
        if not isinstance(submission.i.channel, discord.TextChannel):
            return

        await submission.i.channel.send(embed=embed)

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

    # If task was not completed
    if not submission.tile.would_complete_task(submission.task, submission.amount):
        message = "This would have partially completed a task."

    # If tile is not entirely complete
    if submission.tile.would_complete_task(submission.task, submission.amount):
        message = "This would have completed a task, partially completing the tile."

    # If tile is entirely complete
    if submission.tile.would_complete_tile(submission.task, submission.amount):
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
    def __init__(self, submission: Submission):
        super().__init__()
        self.submission = submission

    @discord.ui.button(
        custom_id="accept", label="🛡️Accept", style=discord.ButtonStyle.green
    )
    @commands.has_permissions(manage_roles=True)
    async def accept_button(self, i: discord.Interaction, button: discord.ui.Button):
        if self.submission.i.channel is None:
            return
        if not isinstance(self.submission.i.channel, discord.TextChannel):
            return
        if self.submission.tile.proof is None:
            return
        if not discord.Permissions(i.permissions.value).manage_roles:
            return

        # Accept proof
        self.submission.tile.proof[self.submission.proof_index].approved = True
        self.submission.tile.proof[self.submission.proof_index].approved_by = i.user.id
        self.submission.tile.proof[self.submission.proof_index].approved_at = time(
        )

        await i.response.edit_message(
            content=await accept_submission(self.submission), view=None
        )

        # Save the game state
        state.serialize()

    @discord.ui.button(custom_id="deny", label="🛡️Deny", style=discord.ButtonStyle.red)
    @commands.has_permissions(manage_roles=True)
    async def deny_button(self, i: discord.Interaction, button: discord.ui.Button):
        if self.submission.i.channel is None:
            return
        if not isinstance(self.submission.i.channel, discord.TextChannel):
            return
        if self.submission.tile.proof is None:
            return
        if not discord.Permissions(i.permissions.value).manage_roles:
            return
        # Remove proof
        self.submission.tile.proof = None

        await i.response.edit_message(
            content=await deny_submission(self.submission), view=None
        )

        # Save the game state
        state.serialize()


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
        if not isinstance(i.user, discord.Member):
            return

        team = in_team(i.user, state.teams)
        if team is None:
            res = f"You are not in a bingo team, if you think this is a mistake, please contact an admin"
            return await i.response.send_message(res, ephemeral=True)

        status = get_tile_state_by_task(team, task)
        # Check if the task has already been submitted
        if status == TileState.COMPLETED:
            res = f"{task} is already completed for {team}"
            return await i.response.send_message(res)

        if status != TileState.UNLOCKED:
            res = f"{task} is not a part of an unlocked tile for team: {state.teams[team].get_name()}"
            return await i.response.send_message(res)

        task_tile_id = get_tile_id_by_task(team, task)
        if task_tile_id is None:
            res = f"{task} is not a part of an unlocked tile for team: {state.teams[team].get_name()}"
            return await i.response.send_message(res)

        # If proof MIME type not of image/jppeg or image/png return
        if proof.content_type not in ["image/jpeg", "image/png"]:
            res = "Proof must be a .jpeg or .png, if you think this is a mistake, please try again or contact an admin"
            return await i.response.send_message(res)

        # We determine the input is successful and valid here, allowing for file parsing
        f = await get_proof_file(proof)
        if isinstance(f, Exception):
            res = f"Error reading proof: {f}\n\nPlease contact an admin."
            return await i.response.send_message(res)

        team = state.teams[team]
        board = team.board
        node = board.get_node(task_tile_id)
        tile = board.get_tile(task_tile_id)

        # Initialize proof list
        if tile.proof is None:
            tile.proof = []

        # Initialize boilerplate proof
        tile.proof.append(Proof(False, task, amount, time(), i.user.id))
        index = tile.proof.index(tile.proof[-1])

        submission = Submission(
            team=team,
            board=board,
            node=node,
            tile=tile,
            proof_index=index,
            amount=amount,
            task=task,
            i=i,
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
            "Proof submited!", ephemeral=True, delete_after=10
        )

        msg = await i.channel.send(
            get_submission_message(
                i, submission.tile, message, "⌛ Pending approval...", amount, task
            ),
            file=discord.File(
                fp=f, filename=f'proof.{proof.content_type.split("/")[1]}'
            ),
            view=Buttons(submission),
        )

        if submission.tile.proof is not None:
            submission.tile.proof[index].message = msg.jump_url

        # Save the game state
        state.serialize()


async def get_proof_file(proof: discord.Attachment) -> BytesIO | Exception:
    try:
        f = await proof.read()
        return BytesIO(f)
    except Exception as e:
        return e


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Submit(bot))

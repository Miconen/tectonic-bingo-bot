import discord
from discord.ext import commands
from typing import List

from models.tile import Proof
from utils.time import get_relative_time, TimestampType
from state.state import state
from utils.teams import in_team

app_commands = discord.app_commands

class Submissions(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Submssion command is ready.")

    @app_commands.command(name="submissions", description="Get your submitted proof.")
    @commands.has_permissions(manage_roles=True)
    async def submissions(
        self,
        i: discord.Interaction,
    ):
        """Get the submitted proof of a tile."""
        if i.channel is None:
            return
        if not isinstance(i.channel, discord.TextChannel):
            return
        if not isinstance(i.user, discord.Member):
            return

        team_id = in_team(i.user, state.teams)
        if team_id is None:
            res = f"You are not in a bingo team, if you think this is a mistake, please contact an admin"
            return await i.response.send_message(res, ephemeral=True)

        team = state.get_team(team_id)
        if team is None:
            res = f"You are not in a bingo team, if you think this is a mistake, please contact an admin"
            return await i.response.send_message(res, ephemeral=True)

        submissions: List[Proof] = []
        for tile in team.board.get_tiles().values():
            if tile.proof is None:
                continue

            for p in tile.proof:
                if p.submitted_by == i.user.id:
                    submissions.append(p)

        if not submissions:
            res = f"No submissions found"
            return await i.response.send_message(res, ephemeral=True)

        msg = f"# Submissions for {i.user.display_name}\n"
        proofs: List[str] = []
        for proof in submissions:
            res = f"{proof.amount}x {proof.task} - {proof.message} {get_relative_time(TimestampType.DATE_TIME_SHORT, proof.submitted_at)} ({get_relative_time(TimestampType.RELATIVE, proof.submitted_at)})"
            proofs.append(res)

        await i.response.send_message(msg + "\n".join(proofs), silent=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Submissions(bot))

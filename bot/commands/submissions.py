import discord
from discord.ext import commands
from typing import List

from models.tile import Proof
from utils.time import get_relative_time, TimestampType
from state.state import state
from utils.teams import in_team

app_commands = discord.app_commands


class Buttons(discord.ui.View):
    def __init__(self, user: discord.Member, submissions: List[Proof]):
        super().__init__(timeout=None)
        self.user = user
        self.submissions = submissions
        self.current_page = 0
        self.per_page = 8
        self.max_pages = (len(submissions) - 1) // self.per_page

        if len(submissions) <= self.per_page:
            self.clear_items()

    def get_page(self):
        start = self.current_page * self.per_page
        end = start + self.per_page
        page = self.submissions[start:end]

        msg = f"# Submissions for {self.user.display_name}\n"
        for proof in page:
            res = f"{proof.amount}x {proof.task} - {proof.message} {get_relative_time(TimestampType.DATE_TIME_SHORT, proof.submitted_at)} ({get_relative_time(TimestampType.RELATIVE, proof.submitted_at)})"
            msg += f"{res}\n"

        if self.max_pages > 0:
            msg += f"\nPage {self.current_page + 1}/{self.max_pages + 1}"

        return msg

    @discord.ui.button(
        custom_id="previous", label="Previous", style=discord.ButtonStyle.primary
    )
    async def previous_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.current_page == 0:
            return await interaction.response.send_message(
                "You are already on the first page", ephemeral=True
            )

        self.current_page -= 1
        await interaction.response.edit_message(content=self.get_page(), view=self)

    @discord.ui.button(
        custom_id="next", label="Next", style=discord.ButtonStyle.primary
    )
    async def next_page(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if self.current_page == self.max_pages:
            return await interaction.response.send_message(
                "You are already on the last page", ephemeral=True
            )

        self.current_page += 1
        await interaction.response.edit_message(content=self.get_page(), view=self)


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

        view = Buttons(i.user, submissions)
        await i.response.send_message(view.get_page(), silent=True, view=view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Submissions(bot))

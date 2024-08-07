import discord
from discord.ext import commands

from state.state import state
from models.team import Team
from models.tile import TileState
from models.board import Board
from utils.board import generate_board
from bot.utils.getters import get_by_state
from bot.utils.images import images


app_commands = discord.app_commands


class Teams(commands.GroupCog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Team commands are ready.")

    @app_commands.command(name="add", description="Add a team based on a role.")
    @commands.has_permissions(manage_roles=True)
    async def add(self, i: discord.Interaction, role: discord.Role):
        """Add a team based on a role."""
        if state.teams.get(role.id) is not None:
            res = f"{role} is already a team."
            return await i.response.send_message(res)

        # Defer the response to avoid timeout, generating the board image can take a while
        await i.response.defer()

        board = Board(generate_board())
        state.add_team(Team(role, board))
        images.generate_image(role.id)

        # Save the game state
        state.serialize()

        res = f"Added {role} as a team."
        await i.followup.send(res)

    @app_commands.command(name="remove", description="Remove a team based on a role.")
    @commands.has_permissions(manage_roles=True)
    async def remove(self, i: discord.Interaction, role: discord.Role):
        """Add a team based on a role."""
        if state.teams.get(role.id) is None:
            res = f"<@&{role.id}> is not a team."
            await i.response.send_message(res)
            return

        # Defer the response just in case as we're doing with the add command
        await i.response.defer()

        state.remove_team(role.id)
        images.remove_image(role.id)

        # Save the game state
        state.serialize()

        res = f"Removed <@&{role.id}> from teams."
        await i.followup.send(res)

    @app_commands.command(name="list", description="List all teams.")
    @commands.has_permissions(manage_roles=True)
    async def list(self, i: discord.Interaction):
        """List added teams and their discord roles."""
        if len(state.teams) == 0:
            await i.response.send_message("There are no teams.", ephemeral=True)
            return

        teams = "\n".join(
            [
                f"**Team:** <@&{team.get_id()}> - **Tiles:** {len(get_by_state(TileState.COMPLETED, team))}"
                for team in state.teams.values()
            ]
        )
        await i.response.send_message(f"# Teams / Roles\n{teams}", silent=True, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Teams(bot))

import discord
from discord.ext import commands

from state.state import state
from models.team import Team
from models.tile import TileState
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
            await i.response.send_message(f"{role} is already a team.")
            return

        # Check if the role is already a team
        state.teams[role.id] = Team(role, generate_board())
        images.generate_image(role.id)
        await i.response.send_message(f"Added {role} as a team.")
        return

    @app_commands.command(name="remove", description="Remove a team based on a role.")
    @commands.has_permissions(manage_roles=True)
    async def remove(self, i: discord.Interaction, role: discord.Role):
        """Add a team based on a role."""
        if state.teams.get(role.id) is None:
            await i.response.send_message(f"{role} is not a team.")
            return

        state.teams.pop(role.id)
        images.remove_image(role.id)
        await i.response.send_message(f"Removed {role} from teams.")
        return

    @app_commands.command(name="list", description="List all teams.")
    @commands.has_permissions(manage_roles=True)
    async def list(self, i: discord.Interaction):
        """Add a team based on a role."""
        if len(state.teams) == 0:
            await i.response.send_message("There are no teams.", ephemeral=True)
            return

        teams = "\n".join(
            [
                f"**Team:** {team.role.name} - **Tiles:** {len(get_by_state(TileState.COMPLETED, team))}"
                for team in state.teams.values()
            ]
        )
        await i.response.send_message(f"# Teams / Roles\n{teams}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Teams(bot))

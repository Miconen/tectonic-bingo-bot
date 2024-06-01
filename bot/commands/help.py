from dataclasses import dataclass
from random import choice, random

import discord
from discord.ext import commands

from bot.utils.getters import footer_texts

app_commands = discord.app_commands

@dataclass
class CommandHelp:
    name: str
    description: str
    moderator: bool = False

commands_help = {
    "tile": CommandHelp(
        name="tile",
        description="Usage: `/tile <id>`\n\nGet information about a tile such as the tile's progress and tasks. Tile IDs can be found using the `/tiles` command which will display all tiles unlocked for your team.\n\nFor more information about tasks, use the `/help tasks` command.",
    ),
    "tiles": CommandHelp(
        name="tiles",
        description="Usage: `/tiles`\n\nGet a list of all tiles unlocked for your team. You can also use the `/tile <id>` command to get more information about a specific tile.",
    ),
    "submit": CommandHelp(
        name="submit",
        description="Usage: `/submit <task> <proof> <optional amount>`\n\nSubmit a task for a tile. Task submissions take a name, proof image and an optional amount, task names are listed and available through the `/tile <id>` command.\n\nFor more information about tasks, use the `/help tasks` command.",
    ),
    "board": CommandHelp(
        name="board",
        description="Usage: `/board`\n\nGet a graph image of all tiles and their progress. This command is useful to see what tiles are unlocked, completed or locked. The image will automatically update when your team unlocks more tiles.",
    ),
    "proof": CommandHelp(
        name="proof",
        description="Usage: `/proof <role> <tile id>`\n\nGet a list of the submitted proof(s) of a tile. If a tile has proof submitted, you can view them here. You can also use the /undo command to remove proof from latest to oldest.",
        moderator=True,
    ),
    "undo": CommandHelp(
        name="undo",
        description="Usage: `/undo <role> <tile id>`\n\nRemove the latest proof submission from a tile. This command is useful if you made a mistake in your submission and want to go back, locking possibly unlocked tiles etc. Use `/board` and `/proof` to validate the undo event.",
        moderator=True,
    ),
    "tasks": CommandHelp(
        name="tasks",
        description="Submissions work by “tasks” which are basically parts of a tile. Some tiles might have a task that requires 100x of an individual thing, and some might have multiple tasks required to complete. Some might also only require some of the tasks to be completed for a tile completion."
    ),
    "submissions": CommandHelp(
        name="submissions",
        description="Submitting “tasks” for tiles should be relatively simple using the bot commands. Once you have submitted a task using the `/submit` commmand, you will need a bingo moderator to accept your submission which will automatically reveal further tiles (if unlocked).",
    ),
    "teams": CommandHelp(
        name="teams",
        description="Usage:\n`/teams add <role>`\n`/teams remove <role>`\n`/teams list`\n\nList and manage all teams and their progress. This command is useful to see and manage teams that are a part of the bingo and to track their progress.",
        moderator=True,
    ),
}

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help commands are ready.")

    @app_commands.command(name="help")
    async def help(self, i: discord.Interaction, command: str) -> None:
        """Command specific help."""
        if command not in commands_help:
            res = "Invalid command or this command does not have a help command."
            return await i.response.send_message(res, ephemeral=True)

        command_help = commands_help[command]

        if command_help.moderator and not i.permissions.manage_roles:
            res = "Invalid permissions to search for this commands help"
            return await i.response.send_message(res, ephemeral=True)

        # Add a 5% chance for an easter egg in the footer text
        footer_text = choice(footer_texts) if random() < 0.05 else "Tectonic"

        embed = discord.Embed(
                title=f"Help for `{command_help.name}`"
        )
        embed.add_field(name="Description", value=command_help.description, inline=False)
        embed.set_footer(text=footer_text).timestamp = i.created_at

        await i.response.send_message(embed=embed, ephemeral=command_help.moderator)

    @help.autocomplete(name="command")
    async def help_autocomplete(self, i: discord.Interaction, user_input: str):
        def is_authorized_command(k: str) -> bool:
            # Filter out non matching autocomplete entries
            if user_input.lower() not in k.lower():
                return False

            # Check if help command doesn't require special permissions
            c = commands_help[k]
            if not c.moderator:
                return True

            print(f"{i.user.display_name} has perms? -> {i.permissions.manage_roles}")
            return i.permissions.manage_roles

        return [
            app_commands.Choice(name=key, value=key)
            for key in commands_help
            if is_authorized_command(key)
        ]


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))

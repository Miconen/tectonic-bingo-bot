from random import choice, random
from typing import List
from models.tile import TileState
from models.team import Team
from utils.board import neighbor_map
from state.state import state
from bot.utils.printing import print_requirements, print_requirement_progress

import discord

from models.tile import Tile
from bot.utils.input import sanitize_string

footer_texts: List[str] = [
    "This is a footer",
    "Blame Max",
    "Lorem ipsum",
    "My eyes are up here",
    "Cwiiiiiiimp",
    "Hawkeye DP",
    "🥄🐀",
    "Free tile for who reads this",
]


def get_tile_embed(i: discord.Interaction, tile: Tile):
    # Add a 5% chance for an easter egg in the footer text
    footer_text = choice(footer_texts) if random() < 0.05 else "Tectonic"

    embed = discord.Embed(
        title=f"{tile.name} (#{tile.id})", color=tile.theme.value, url=tile.rules_link
    )
    embed.set_thumbnail(url=tile.image)
    embed.add_field(name="Description", value=tile.description, inline=False)
    embed.add_field(
        name=f"Tasks for completion: ({print_requirement_progress(tile)})",
        value=print_requirements(tile.requirements),
        inline=False,
    )
    embed.add_field(
        name=f"Tiles unlocked on completion",
        value=", ".join(f"#{str(n)}" for n in neighbor_map[tile.id]),
        inline=False,
    )
    embed.add_field(
        name="Info",
        value="`/board` to see the updated board.\n`/tiles` to see all unlocked tiles.\n`/submit <task name> <proof image> <amount (optional)>` to submit a task.",
        inline=False,
    )
    embed.set_footer(text=footer_text).timestamp = i.created_at

    return embed


def get_tiles_embed(i: discord.Interaction, team: Team, tiles: List[Tile]):
    # Add a 10% chance for an easter egg in the footer text
    footer_text = choice(footer_texts) if random() < 0.1 else "Tectonic"

    embed = discord.Embed(
        title=f"Unlocked tiles for {team.get_name()}", color=discord.Color.red()
    )
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/icons/979445890064470036/70b3e59890b25b8f1418e32ce32650de.webp"
    )

    embed.add_field(
        name="Current progress",
        value=f"Unlocked tiles: {len(get_by_state(TileState.UNLOCKED, team))}\nCompleted tiles: {len(get_by_state(TileState.COMPLETED, team))}",
        inline=False,
    )

    tile_list: List[str] = []
    for tile in tiles:
        tile_list.append(f"#{tile.id} - **{tile.name}**")

    embed.add_field(
        name=f"Unlocked tiles",
        value="\n".join(tile_list),
        inline=False,
    )

    embed.add_field(
        name=f"Info",
        value="`/board` to see the updated board.\n`/tile <id>` to see a specific tile.\n`/submit <task name> <proof image> <amount (optional)>` to submit a task.",
        inline=False,
    )

    embed.set_footer(text=footer_text).timestamp = i.created_at

    return embed


def get_unlock_embed(i: discord.Interaction, team: Team, tiles: List[Tile]):
    # Add a 10% chance for an easter egg in the footer text
    footer_text = choice(footer_texts) if random() < 0.1 else "Tectonic"

    embed = discord.Embed(title="New tiles unlocked!", color=discord.Color.red())
    embed.set_thumbnail(
        url="https://cdn.discordapp.com/icons/979445890064470036/70b3e59890b25b8f1418e32ce32650de.webp"
    )

    unlocks: List[str] = []
    for tile in tiles:
        unlocks.append(f"#{tile.id} - **{tile.name}**")

    embed.add_field(
        name=f"New tiles",
        value="\n".join(unlocks),
        inline=False,
    )

    embed.add_field(
        name=f"Current progress for {team.get_name()}",
        value=f"Unlocked tiles: {len(get_by_state(TileState.UNLOCKED, team))}\nCompleted tiles: {len(get_by_state(TileState.COMPLETED, team))}",
        inline=False,
    )

    embed.add_field(
        name=f"Info",
        value="`/board` to see the updated board.\n`/tile <id>` to see a specific tile.\n`/tiles` to see all unlocked tiles.\n`/submit <task name> <proof image> <amount (optional)>` to submit a task.",
        inline=False,
    )

    embed.set_footer(text=footer_text).timestamp = i.created_at

    return embed


def get_submission_message(
    i: discord.Interaction, tile: Tile, update: str, status: str, amount: int, task: str
):
    count = f"{amount}x " if amount else ""

    message = (
        "# {} (#{})\n"
        "- **{}{}** submitted by **{}**\n"
        "- **Update**: {}\n"
        "- **Status**: {}\n\n"
        "**Tasks ({})**\n"
        "{}\n\n"
        "**Tiles unlocked on completion**\n"
        "{}"
    ).format(
        tile.name,
        tile.id,
        count,
        task,
        i.user.display_name,
        update,
        status,
        print_requirement_progress(tile),
        print_requirements(tile.requirements),
        ", ".join(f"#{str(n)}" for n in neighbor_map[tile.id]),
    )
    return message


def get_by_state(status: TileState, team: Team):
    tiles = team.board.get_tiles()
    return [tile for tile in tiles.values() if tile.value.state == status]


def get_tile_state_by_task(team_id: int, task: str):
    found = None
    team = state.teams[team_id]
    board = team.board

    task = sanitize_string(task)

    for tile_id in board.get_tiles().keys():
        tile = board.get_tile(tile_id)

        for keys in tile.requirements.keys():
            task_keys = map(sanitize_string, keys.split("|"))

            if task not in task_keys:
                continue

            if tile.state == TileState.COMPLETED:
                found = tile.state
                continue

            if tile.state != TileState.UNLOCKED:
                continue

            return tile.state

    return found


def get_tile_id_by_task(team_id: int, task: str):
    found = None
    team = state.teams[team_id]
    board = team.board

    task = sanitize_string(task)

    for tile_id in board.get_tiles().keys():
        tile = board.get_tile(tile_id)

        for keys in tile.requirements.keys():
            task_keys = map(sanitize_string, keys.split("|"))

            if task not in task_keys:
                continue

            if tile.state == TileState.COMPLETED:
                found = tile_id
                continue

            if tile.state != TileState.UNLOCKED:
                continue

            return tile_id

    return found

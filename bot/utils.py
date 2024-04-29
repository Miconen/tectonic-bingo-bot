from typing import List, Dict
from random import choice, random
from models.tile import Criteria, TileState
from models.team import Team
from models.criteria import Count
from utils.board import neighbor_map

import discord

from models.tile import Tile

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

def print_requirements(requirements: Dict[str, Criteria]):
    res = []

    for key, req in requirements.items():
        completed = "✅" if req.is_satisfied() else "⬜"

        if isinstance(req, Count) and req.threshold > 1:
            res.append(f"{completed} - {key} ({req.count}/{req.threshold})")
            continue

        res.append(f"{completed} - {key}")

    return "\n".join(res)


def print_requirement_progress(tile: Tile):
    done = 0
    for req in tile.requirements.values():
        if req.is_satisfied():
            done = done + 1

    return f"{done}/{tile.required_for_completetion}"


def get_tile_embed(i: discord.Interaction, tile: Tile):
    # Add a 5% chance for an easter egg in the footer text
    footer_text = choice(footer_texts) if random() < 0.05 else "Tectonic"

    embed = discord.Embed(
        title=f"{tile.name} (#{tile.id})", color=tile.theme.value, url=tile.rules_link
    )
    embed.set_thumbnail(url=tile.image)
    embed.add_field(name="Description", value=tile.description, inline=False)
    embed.add_field(
        name=f"Tasks ({print_requirement_progress(tile)})",
        value=print_requirements(tile.requirements),
        inline=False,
    )
    embed.add_field(
        name=f"Tiles unlocked on completion",
        value=", ".join(f"#{str(n)}" for n in neighbor_map[tile.id]),
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
    return [tile for tile in team.board.values() if tile.value.state == status]


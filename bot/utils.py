from typing import List, Dict
from random import choice, random
from models.tile import Criteria
from models.criteria import Count

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

neighbor_map: Dict[int, List[int]] = {
    1: [7, 8],
    2: [7, 8, 11, 12],
    3: [11, 12, 17, 18],
    4: [17, 18, 21, 22],
    5: [26, 27],
    6: [31, 32],
    7: [1, 2],
    8: [1, 2],
    9: [11, 13],
    10: [12, 14],
    11: [2, 3, 9, 15],
    12: [2, 3, 10, 16],
    13: [9, 15],
    14: [10, 16],
    15: [11, 13, 17, 19],
    16: [12, 14, 18, 20],
    17: [3, 4, 15, 19],
    18: [3, 4, 16, 20],
    19: [15, 17, 21, 25],
    20: [16, 18, 22, 28],
    21: [4, 19, 25, 26],
    22: [4, 20, 27, 28],
    23: [29, 30],
    24: [33, 34],
    25: [19, 21, 30, 31],
    26: [5, 21, 31],
    27: [5, 22, 32],
    28: [20, 22, 32, 33],
    29: [23, 35],
    30: [23, 25, 35],
    31: [6, 25, 26, 35],
    32: [6, 27, 28, 36],
    33: [24, 28, 36],
    34: [24, 36],
    35: [29, 30, 31],
    36: [32, 33, 34],
}


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

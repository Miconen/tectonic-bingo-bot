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

def print_requirements(requirements: Dict[str, Criteria]):
    res = []

    for key, req in requirements.items():
        completed = "[X]" if req.is_satisfied() else "[ ]"

        if isinstance(req, Count) and req.threshold > 1:
            res.append(f'{completed} - {key} ({req.count}/{req.threshold})')
            continue

        res.append(f'{completed} - {key}')

    return "\n".join(res)

def print_requirement_progress(tile: Tile):
    done = 0
    for req in tile.requirements.values():
        if req.is_satisfied():
            done = done + 1

    return f"{done}/{tile.required_for_completetion}"

def get_tile_embed(i: discord.Interaction, tile: Tile):
    # Add a 10% chance for an easter egg in the footer text
    footer_text = choice(footer_texts) if random() < 0.05 else "Tectonic"

    embed = discord.Embed(title=f"{tile.name} (#{tile.id})", color=tile.theme.value)
    embed.set_thumbnail(url=tile.image)
    embed.add_field(
        name="Description",
        value=tile.description,
        inline=False
    )
    embed.add_field(
        name=f"Tasks ({print_requirement_progress(tile)})",
        value=print_requirements(tile.requirements),
        inline=False
    )
    embed.set_footer(text=footer_text).timestamp = i.created_at

    return embed


# async def get_proof_file(proof: discord.Attachment) -> BytesIO | Exception:
#     try:
#         f = await proof.read()
#         return BytesIO(f)
#     except Exception as e:
#         return e

import random
from typing import List

import discord
import discord.ext
import jsonpickle

from state.state import state
from utils.teams import in_team

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

footer_texts: List[str] = [
    "This is a footer",
    "Blame Max",
    "Lorem ipsum",
    "My eyes are up here",
]


@client.event
async def on_ready():
    """Called when the bot is ready."""
    await tree.sync()
    print("Logged on as", client.user)


@client.event
async def on_message(message: discord.Message):
    """Test command for checking bot responsiveness."""
    print(f"Message from {message.author}: {message.content}")
    if message.content.lower() == "ping":
        await message.reply("Pong!")


@tree.command(name="tile", description="Get information about a tile")
@discord.app_commands.describe(tile_id="Tile ID")
async def tile(i: discord.Interaction, tile_id: discord.app_commands.Range[int, 1, 36]):
    """Displays inofrmation about a tile if it's unlocked."""

    embed = discord.Embed(title=f"Godsword Hilts (#{tile_id})", color=0x00FF00)
    embed.set_thumbnail(
        url="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png"
    )
    embed.add_field(
        name="Description",
        value="""
            Obtain 5 unique slayer related drops. You may obtain multiple different uniques from the same boss (no dupes). Only the uniques listed below will count towards the tile.

            -----

            **Grotesque Guardians** = Granite gloves, Granite ring, Granite hammer, Tourmaline core, Jar

            **Kraken** = Full trident of the seas, Kraken tentacle, Jar

            **Sire** = Bludgeon piece, Abyssal dagger, Abyssal head, Jar

            **Thermonuclear Smoke Devil** = Smoke battlestaff, Occult Necklace, Jar

            **Alchemical Hydra** = a Brimstone ring piece, Hydra tail, Hydra leather, Hydra’s claw, Alchemical Hydra Heads, Jar

            **Cerberus** = Primordial-, Pegasian-, Eternal crystal, Smouldering Stone, Jar
        """,
    )
    embed.set_footer(text=random.choice(footer_texts)).timestamp = i.created_at
    await i.response.send_message(embed=embed)

@tree.command(name="serialize", description="Serialize the state to a JSON file")
async def serialize(i: discord.Interaction):
    """Serialize the state to a JSON file."""
    state.serialize()
    await i.response.send_message(f'State serialized to JSON file successfully {jsonpickle.encode(state)}')

@tree.command(name="list", description="List all unlocked tiles")
async def list(i: discord.Interaction):
    """List all unlocked tiles."""
    team = in_team(i.user.id, state.teams)

    print(state.teams)

    if team is None:
        await i.response.send_message(f'You are not in a team (Teams: {len(state.teams)})')
        return

    board = state.teams[team].board
    unlocked_tiles = [node.value.name for node in board if node.value.is_unlocked()]

    await i.response.send_message(f"Unlocked tiles: {', '.join(unlocked_tiles)}")

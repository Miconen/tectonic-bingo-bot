import os
import sys

from models.tile import Tile, TileState, TileTheme
from models.criteria import Count
from models.graph import GraphNode

from dotenv import load_dotenv
from bot.bot import bot
from state.state import state, Team


if __name__ == "__main__":
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        print("No token provided in environment variables. Exiting...")
        sys.exit(1)

    # Generate board -> team -> state

    tiles = [
        Tile(
            1,
            "https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            "Lorem ipsum tile",
            "dolor sit amet",
            TileState.UNLOCKED,
            TileTheme.MISCELLANEOUS,
            2,
            {"Fang": Count(1), "Purple Sweets": Count(100)},
        ),
        Tile(
            2,
            "https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            "Slayer tile",
            """
                Obtain 5 unique slayer related drops. You may obtain multiple different uniques from the same boss (no dupes). Only the uniques listed below will count towards the tile.
            """,
            TileState.UNLOCKED,
            TileTheme.DROPS,
            1,
            {"Shadow": Count(1)},
        ),
    ]

    board = {}
    for tile in tiles:
        board.update({tile.id: GraphNode(tile)})

    team = Team([136856906139566081], board)

    state.teams.update({"Team 1": team})

    bot.run(token)

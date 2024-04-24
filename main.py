import os
import sys

from models.tile import Tile, TileState
from models.criteria import Count
from models.graph import GraphNode

from dotenv import load_dotenv
from bot.bot import client as bot
from state.state import state, State, Team


def __main__():
    load_dotenv()

    token = os.getenv("BOT_TOKEN")
    if not token:
        print("No token provided in environment variables. Exiting...")
        sys.exit(1)

    tile = Tile(
        1,
        "Lorem ipsum",
        "dolor sit amet",
        TileState.UNLOCKED,
        2,
        {"Fang": Count(1), "Purple Sweets": Count(100)},
    )
    board = [GraphNode(tile)]
    team = Team("Team 1", ["136856906139566081"], board)

    state.teams.append(team)

    bot.run(token)


__main__()

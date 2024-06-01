from typing import List

import discord

from models.graph import GraphNode
from models.board import Board
from models.tile import Tile, TileState


class Team(object):
    """Represents a bingo team which gets binded to a discord role."""
    id: int
    name: str
    board: Board

    def __init__(self, role: discord.Role, board: Board):
        self.board = board
        self.id = role.id
        self.name = role.name

    def get_name(self):
        """Get the name of the team."""
        return self.name

    def get_id(self):
        """Get the ID of the team."""
        return self.id

    def update_neighboring(
        self,
        node: GraphNode,
        new_state: TileState,
        excludes: List[TileState] | None = None,
    ):
        """Update the state of neighboring tiles of a given tile. Returning the updated tiles."""
        result: List[Tile] = []

        for neighbor_id in node.neighbors:
            tile = self.board.get_node(neighbor_id)

            if excludes and tile.value.state in excludes:
                continue

            if any(tile.value.id == res.id for res in result):
                continue

            # More than one completed neighbors
            # We check this to prevent unflipping more than once unlocked tiles
            completed_neighbors = 0
            for neighbor in tile.neighbors:
                if self.board.get_tile(neighbor).state == TileState.COMPLETED:
                    completed_neighbors += 1

            if completed_neighbors > 1:
                continue

            tile.value.state = new_state
            result.append(tile.value)

        return result

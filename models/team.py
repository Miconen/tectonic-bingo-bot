import discord

from typing import List, Dict
from models.graph import GraphNode
from models.tile import Tile, TileState


class Team(object):
    id: int
    name: str
    board: Dict[int, GraphNode]

    def __init__(self, role: discord.Role, board: Dict[int, GraphNode]):
        self.board = board
        self.id = role.id
        self.name = role.name

    def get_node(self, tile_id: int):
        return self.board[tile_id]

    def get_tile(self, tile_id: int):
        return self.board[tile_id].value

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def update_neighboring(
        self,
        node: GraphNode,
        new_state: TileState,
        filter: List[TileState] | None = None,
    ):
        """Update the state of neighboring tiles of a given tile. Returning the updated tiles."""
        result: List[Tile] = []

        for neighbor_id in node.neighbors:
            tile = self.board[neighbor_id]

            if filter and tile.value.state in filter:
                continue

            if any(tile.value.id == res.id for res in result):
                continue

            # More than one completed neighbors
            # We check this to prevent unflipping more than once unlocked tiles
            completed_neighbors = 0
            for neighbor in tile.neighbors:
                if self.board[neighbor].value.state == TileState.COMPLETED:
                    completed_neighbors += 1

            if completed_neighbors > 1:
                continue

            tile.value.state = new_state
            result.append(tile.value)

        return result

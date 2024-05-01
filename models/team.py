import discord

from typing import List, Dict
from models.graph import GraphNode
from models.tile import Tile, TileState

class Team(object):
    role: discord.Role
    board: Dict[int, GraphNode]

    def __init__(self, role: discord.Role, board: Dict[int, GraphNode]):
        self.board = board
        self.role = role

    def get_tile(self, tile_id: int):
        return self.board[tile_id]

    def get_name(self):
        return self.role.name

    def get_id(self):
        return self.role.id

    def update_neighboring(self, node: GraphNode, new_state: TileState, filter: List[TileState] | None = None):
        """Update the state of neighboring tiles of a given tile. Returning the updated tiles."""
        result: List[Tile] = []

        for neighbor_id in node.neighbors:
            tile = self.board[neighbor_id]

            if filter and tile.value.state in filter:
                continue

            tile.value.state = new_state
            result.append(tile.value)

        return result

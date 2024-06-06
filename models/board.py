from dataclasses import dataclass
from typing import Dict

from models.graph import GraphNode

@dataclass
class Board:
    tiles: Dict[int, GraphNode]

    def get_node(self, tile_id: int):
        return self.tiles[tile_id]

    def get_tile(self, tile_id: int):
        return self.get_node(tile_id).value

    def get_nodes(self):
        return self.tiles

    def get_tiles(self):
        return { tile: self.get_tile(tile) for tile in self.tiles }

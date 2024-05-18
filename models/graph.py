from typing import List
from models.tile import Tile

class GraphNode(object):
    value: Tile
    neighbors: List[int]

    def __init__(self, value):
        self.value = value
        self.neighbors = []

    def add_neighbor(self, neighbor_id: int):
        self.neighbors.append(neighbor_id)

    def __repr__(self):
        return f"GraphNode({self.value.name})"

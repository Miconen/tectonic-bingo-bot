from typing import List
from models.tile import Tile, TileState


class GraphNode:
    value: Tile
    neighbors: List["GraphNode"]

    def __init__(self, value):
        self.value = value
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        return self

    def update_neighbors(self, new_state: TileState, ignoring: List[TileState] | None = None):
        for neighbor in self.neighbors:
            if not ignoring:
                continue

            if neighbor.value.state in ignoring:
                continue

            neighbor.value.state = new_state

    def __repr__(self):
        return f"GraphNode({self.value.name})"

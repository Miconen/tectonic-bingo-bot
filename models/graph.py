from typing import List
from models.tile import Tile, TileState

class GraphNode:
    value: Tile
    neighbors: List['GraphNode']

    def __init__(self, value):
        self.value = value
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)
        return self

    def update_neighbors(self, new_state: TileState):
        for neighbor in self.neighbors:
            # This has and edge case where if the neighbor is already completed, it will not hide the neighbor
            if neighbor.value.state == TileState.COMPLETED: return
            neighbor.value.state = new_state

    def __repr__(self):
        return f"GraphNode({self.value.name})"

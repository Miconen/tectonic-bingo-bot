from models.tile import Tile, TileState
from models.criteria import Count
from models.graph import GraphNode

def __main__():
    tile = Tile(1, "Lorem ipsum", "dolor sit amet", TileState.UNLOCKED, 2, {"Fang": Count(1), "Purple Sweets": Count(100)})
    print(tile.is_complete())

    node = GraphNode(tile).add_neighbor(GraphNode(tile))
    print(node)

__main__()

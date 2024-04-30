from typing import List, Dict

from models.graph import GraphNode

from models.tile import Tile, TileState, TileTheme
from models.criteria import Count, OneOf

neighbor_map: Dict[int, List[int]] = {
    1: [7, 8],
    2: [7, 8, 11, 12],
    3: [11, 12, 17, 18],
    4: [17, 18, 21, 22],
    5: [26, 27],
    6: [31, 32],
    7: [1, 2],
    8: [1, 2],
    9: [11, 13],
    10: [12, 14],
    11: [2, 3, 9, 15],
    12: [2, 3, 10, 16],
    13: [9, 15],
    14: [10, 16],
    15: [11, 13, 17, 19],
    16: [12, 14, 18, 20],
    17: [3, 4, 15, 19],
    18: [3, 4, 16, 20],
    19: [15, 17, 21, 25],
    20: [16, 18, 22, 28],
    21: [4, 19, 25, 26],
    22: [4, 20, 27, 28],
    23: [29, 30],
    24: [33, 34],
    25: [19, 21, 30, 31],
    26: [5, 21, 31],
    27: [5, 22, 32],
    28: [20, 22, 32, 33],
    29: [23, 35],
    30: [23, 25, 35],
    31: [6, 25, 26, 35],
    32: [6, 27, 28, 36],
    33: [24, 28, 36],
    34: [24, 36],
    35: [29, 30, 31],
    36: [32, 33, 34],
}


def generate_board():
    tiles = [
        Tile(
            TileState.UNLOCKED,
            TileTheme.MISCELLANEOUS,
            {"Fang": Count(1), "Purple Sweets": Count(100)},
            id=1,
            image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            name="Tile with multiple requirements",
            description="This is a description of the tile. It has multiple requirements.",
            required_for_completetion=2,
        ),
        Tile(
            TileState.UNLOCKED,
            TileTheme.DROPS,
            {"Shadow": Count(1)},
            id=2,
            image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            name="Slayer tile",
            description="""
                Obtain 5 unique slayer related drops. You may obtain multiple different uniques from the same boss (no dupes). Only the uniques listed below will count towards the tile.
            """,
            required_for_completetion=1,
            rules_link="https://www.google.com",
        ),
        Tile(
            TileState.LOCKED,
            TileTheme.DROPS,
            {"Shadow": Count(1)},
            id=3,
            image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            name="Locked by default tile",
            description="""
                Obtain 5 unique slayer related drops. You may obtain multiple different uniques from the same boss (no dupes). Only the uniques listed below will count towards the tile.
            """,
            required_for_completetion=1,
            rules_link="https://www.google.com",
        ),
        Tile(
            TileState.UNLOCKED,
            TileTheme.DROPS,
            {"Scythe": Count(1), "Shadow": Count(1), "Twisted Bow": Count(1)},
            id=3,
            image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            name="Raid Megarare",
            description="Obtain any megarare raid drop. (Scythe, Twisted Bow, or Shadow)",
            required_for_completetion=1,
            rules_link="https://www.google.com",
        ),
        Tile(
            TileState.UNLOCKED,
            TileTheme.DROPS,
            {
                "Scythe": Count(1),
                "Shadow|Twisted Bow": OneOf({"Shadow": Count(1), "Twisted Bow": Count(1)}),
            },
            id=4,
            image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            name="Raid Megarare",
            description="Obtain any megarare raid drop. (Scythe, Twisted Bow, or Shadow)",
            required_for_completetion=1,
            rules_link="https://www.google.com",
        ),
    ]

    # Fille the rest of tiles
    for i in range(len(tiles) + 1, 36):
        tiles.append(
            Tile(
                TileState.LOCKED,
                TileTheme.DROPS,
                {f"Tile {i} req": Count(1)},
                id=i,
                image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
                name="AUTOGENERATED locked test tile",
                description="""
                    This tile was autogenerated for testing purposes.
                """,
                required_for_completetion=1,
                rules_link="https://www.google.com",
            )
        )

    # Generate board connections
    board: Dict[int, GraphNode] = {}
    for tile in tiles:
        node = board.setdefault(tile.id, GraphNode(tile))
        for n in neighbor_map[tile.id]:
            node.add_neighbor(n)

    return board
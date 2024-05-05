from typing import List, Dict

from models.graph import GraphNode

from models.tile import Tile, TileState, TileTheme
from models.criteria import Count, Some

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
            TileTheme.MISCELLANEOUS,
            {"Purple Sweets": Count(100)},
            id=18,
            image="https://oldschool.runescape.wiki/images/Purple_sweets_detail.png",
            name="Clue tile",
            description="This is a description of the tile. It has multiple requirements.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Odium 1|Malediction 1": Some(
                    {"Odium 1": Count(1), "Malediction 1": Count(1)},
                ),
                "Odium 2|Malediction 2": Some(
                    {"Odium 2": Count(1), "Malediction 2": Count(1)},
                ),
                "Odium 3|Malediction 3": Some(
                    {"Odium 3": Count(1), "Malediction 3": Count(1)},
                ),
            },
            id=16,
            image="https://oldschool.runescape.wiki/images/Malediction_ward_detail.png",
            name="Wilderness Shield",
            description="Obtain wildy shield fragments 1, 2, & 3. Each fragment can be from either of the shields I.e malediction shard 1, odium shard 2, odium shard 3.",
            required_for_completetion=3,
        ),
        Tile(
            TileTheme.RAIDS,
            {
                "Cursed phalanx|Holy ornament kit|Sanguine ornament kit": Some(
                    {
                        "Cursed phalanx": Count(5),
                        "Twisted ancestral colour kit": Count(1),
                        "Holy ornament kit": Count(1),
                        "Sanguine ornament kit": Count(1),
                    },
                    2,
                ),
                "Metamorphic dust|Sanguine dust": Some(
                    {"Metamorphic dust": Count(1), "Sanguine dust": Count(1)}
                ),
            },
            id=5,
            image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            name="Hard Modes",
            description="Mix of all possible hard mode raid drops.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Chef's hat": Count(1),
            },
            state=TileState.UNLOCKED,
            id=4,
            image="https://oldschool.runescape.wiki/images/Chef's_hat_detail.png",
            name="Let them cook",
            description="To kick it off, obtain a chef's hat.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Scythe of Vitur": Count(1),
                "Tumeken's Shadow": Count(1),
                "Twisted Bow": Count(1),
            },
            id=34,
            image="https://oldschool.runescape.wiki/images/Zamorak_hilt_detail.png",
            name="Raid Megarare",
            description="Obtain any megarare raid drop. (Scythe, Twisted Bow, or Shadow)",
        ),
        Tile(
            TileTheme.HARD,
            {
                "Infernal Cape": Count(5),
            },
            id=10,
            image="https://oldschool.runescape.wiki/images/Infernal_cape_detail.png",
            name="Inferno",
            description="TBD: Something inferno related",
        ),
        Tile(
            TileTheme.HARD,
            {
                "Torva platebody|Torva plaelegs|Torva helmet|Ancient hilt|Nihil horn": Count(
                    2
                ),
            },
            id=9,
            image="https://oldschool.runescape.wiki/images/Torva_full_helm_detail.png",
            name="Nex",
            description="TBD: Something Nex related",
        ),
        Tile(
            TileTheme.HARD,
            {
                "Sunfire splinter": Count(150000),
            },
            id=6,
            image="https://oldschool.runescape.wiki/images/Sunfire_splinters_4_detail.png",
            name="Blessings of Ralos",
            description="TBD: Sunfire splinters",
        ),
    ]

    # Fill the rest of tiles
    tile_dict = {tile.id: tile for tile in tiles}
    for i in range(1, 37):
        if i in tile_dict:
            continue

        tile_dict[i] = Tile(
            TileTheme.MISCELLANEOUS,
            {f"Autogenerated {i}": Count(1)},
            id=i,
            image="https://oldschool.runescape.wiki/images/Cake_of_guidance_detail.png",
            name="Autogenerated tile",
            description="This tile was autogenerated for testing purposes just to fill the whole board.",
        )

    # Generate board connections
    board: Dict[int, GraphNode] = {}
    for key, tile in tile_dict.items():
        node = board.setdefault(key, GraphNode(tile))
        for n in neighbor_map[key]:
            node.add_neighbor(n)

    return board

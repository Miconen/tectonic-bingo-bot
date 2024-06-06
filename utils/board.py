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
            image="https://oldschool.runescape.wiki/images/Twisted_ancestral_colour_kit_detail.png",
            name="Hard Modes",
            description="Mix of all possible hard mode raid drops.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Mudskipper hat": Count(1),
                "Flippers": Count(1),
            },
            state=TileState.UNLOCKED,
            id=4,
            image="https://oldschool.runescape.wiki/images/thumb/Flippers_detail.png/1024px-Flippers_detail.png",
            name="Mogre Dropper",
            description="To kick it off the summer bingo, obtain a mudskipper hat and flippers.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Staff of the dead": Count(1),
                "Saradomin's light": Count(1),
            },
            id=7,
            image="https://oldschool.runescape.wiki/images/Staff_of_light_detail.png",
            name="Staff of Light",
            description="Get both pieces for a full Staff of Light as a team.\nZamorak/Saradomin hilt is a wildcard (can be submitted for either Staff of Light Piece)",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Wilderness unique": Count(3)},
            id=8,
            image="https://oldschool.runescape.wiki/images/Voidwaker_hilt_detail.png",
            name="VW and Rings",
            description="""
                Obtain any mix of three Voidwaker pieces and wilderness rings
            """,
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Strange old lockpick|Ring of endurance|Giant Squirrel": Some(
                    {
                        "Strange old lockpick": Count(3),
                        "Ring of endurance": Count(1),
                        "Giant Squirrel": Count(1),
                    }
                ),
            },
            id=2,
            name="Hallowed Sepulchre",
            image="https://oldschool.runescape.wiki/images/Strange_old_lockpick_(full)_detail.png",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "ToB Purple": Count(4),
                "Scythe of Vitur": Count(1),
            },
            id=3,
            image="https://oldschool.runescape.wiki/images/Lil'_Zik.png",
            name="Theatre of Blood",
            required_for_completetion=1,
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Barrows unique": Count(10)},
            id=11,
            image="https://oldschool.runescape.wiki/images/Dharok's_greataxe_detail.png",
            name="Barrows",
            description="Acquire 10 barrows uniques.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Zulrah unique": Count(5)},
            id=12,
            image="https://oldschool.runescape.wiki/images/Snakeling.png",
            name="Barrows",
            description="""
                Acquire 5 Zulrah uniques as a team. Duplicates count.\n
                Tanzanite fang
                Magic fang
                Serpentinve visage
                Uncut onyx
                Tanzanite mutagen
                Magma mutagen
                Jar of swamp
                Pet snakeling
            """,
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Bandos boots|Ardmadyl helmet": Some(
                    {"Bandos boots": Count(1), "Armadyl helmet": Count(1)},
                ),
                "Bandos chestplate|Armadyl chestplate": Some(
                    {"Bandos chestplate": Count(1), "Armadyl chestplate": Count(1)},
                ),
                "Bandos tassets|Armadyl chainskirt": Some(
                    {"Bandos tassets": Count(1), "Armadyl chainskirt": Count(1)},
                ),
            },
            id=13,
            image="https://oldschool.runescape.wiki/images/Bandos_tassets_detail.png",
            name="Bandos/Kree armor",
            description="Mix and match a full set of Bandos/Armadyl armor. If you manage to get a hilt you can submit it under any armor piece of your choosing as a proof image.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Spirit shield|Holy elixir": Some(
                    {
                        "Spirit shield": Count(1),
                        "Holy elixit": Count(1),
                    },
                    required=2,
                ),
                "Spectral sigil|Arcane sigil|Elysian sigil|Jar of spirits|Pet dark core": Some(
                    {
                        "Spectral sigil": Count(1),
                        "Arcane sigil": Count(1),
                        "Elysian sigil": Count(1),
                        "Jar of spirits": Count(1),
                        "Pet dark core": Count(1),
                    }
                ),
            },
            id=14,
            image="https://oldschool.runescape.wiki/images/Blessed_spirit_shield_detail.png",
            name="Corporeal Blessing",
            description="A full blessed spirit shield (spirit shield + holy elixr). Alternatively get any sigil, jar or pet to instantly complete the tile.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Big Bass|Cockatrice Head|Big Swordfish|Big Harpoonfish|Basilisk Head|Big Shark|Kurask Head|KBD Heads|KQ Head|Vorkath Head": Some(
                    {
                        "Big Bass": Count(1),
                        "Cockatrice Head": Count(1),
                        "Big Swordfish": Count(1),
                        "Big Harpoonfish": Count(1),
                        "Basilisk Head": Count(1),
                        "Big Shark": Count(1),
                        "Kurask Head": Count(1),
                        "KBD Heads": Count(1),
                        "KQ Head": Count(1),
                        "Vorkath Head": Count(1),
                    },
                    5,
                )
            },
            required_for_completetion=5,
            id=15,
            image="https://oldschool.runescape.wiki/images/Vorkath's_head_detail.png",
            name="Stuffables",
            description="""
                Stuffable means an item that the taxidermist will stuff for your POH.\n
                Crawling hand will not count for this tile as it is too common.
                Sire and Hydra heads also will not count for this tile, as they count for the slayer boss tile.
                Guaranteed Vorkath (50kc) and KQ (Tattered) heads do not count.
                Only unique, non duplicate submissions count.
            """,
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Raid purple": Count(1),
                "Raid pet": Count(1),
            },
            id=17,
            image="https://oldschool.runescape.wiki/images/Purple_partyhat_detail.png",
            name="Any Purple",
            description="Any purple or pet from any raid. This purple will not count for future raid tiles.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Scurrius' spine": Count(10)},
            id=18,
            image="https://oldschool.runescape.wiki/images/Scurrius'_spine_detail.png",
            name="Scurrius",
            description="Obtain 10 scurrius' spines as a team.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Purple sweets": Count(250)},
            id=19,
            image="https://oldschool.runescape.wiki/images/Purple_sweets_detail.png",
            name="Purple Clues",
            description="Obtain 250 purple sweets; Must submit proof that you have no pre-stacked caskets.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Granite boots|Granite sword|Granite legs|Granite shield|Granite helm|Granite maul": Some(
                    {
                        "Granite boots": Count(1),
                        "Granite sword": Count(1),
                        "Granite legs": Count(1),
                        "Granite shield": Count(1),
                        "Granite helm": Count(1),
                        "Granite maul": Count(1),
                    },
                    4,
                ),
            },
            id=20,
            image="https://oldschool.runescape.wiki/images/Granite_maul_detail.png",
            name="Granite Chad",
            description="Obtain any 4: granite boots, granite swords, granite legs, granite shield, granite helm, granite maul.",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Granite gloves|Granite ring|Granite hammer|Tourmaline core|Full trident of the seas|Kraken tentacle|Bludgeon piece|Abyssal dagger|Abyssal head|Smoke battlestaff|Occult Necklace|Brimstone ring piece|Hydra tail|Hydra leather|Hydra’s claw|Alchemical Hydra Heads|Pegasian crystal|Eternal crystal|Primordial crystal|Smouldering Stone": Some(
                    {
                        "Granite gloves": Count(1),
                        "Granite ring": Count(1),
                        "Granite hammer": Count(1),
                        "Tourmaline core": Count(1),
                        "Full trident of the seas": Count(1),
                        "Kraken tentacle": Count(1),
                        "Bludgeon piece": Count(1),
                        "Abyssal dagger": Count(1),
                        "Abyssal head": Count(1),
                        "Smoke battlestaff": Count(1),
                        "Occult Necklace": Count(1),
                        "Brimstone ring piece": Count(1),
                        "Hydra tail": Count(1),
                        "Hydra leather": Count(1),
                        "Hydra’s claw": Count(1),
                        "Alchemical Hydra Heads": Count(1),
                        "Pegasian crystal": Count(1),
                        "Eternal crystal": Count(1),
                        "Primordial crystal": Count(1),
                        "Smouldering Stone": Count(1),
                    },
                    5,
                )
            },
            id=21,
            image="https://oldschool.runescape.wiki/images/Slayer_helmet_detail.png",
            name="Slayer Bosses",
            description="""
                Obtain 5 unique slayer related drops. You may obtain multiple different uniques from the same boss (no dupes). Only the uniques listed below will count towards the tile. Pets & jars will count as uniques.

                (only 1 bludgeon piece will count towards the tile)
                (only 1 piece of brimstone ring will count towards the tile)
            """,
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Pharaoh's sceptre": Count(1), "Rocky": Count(1)},
            id=22,
            image="https://oldschool.runescape.wiki/images/Pharaoh's_sceptre_(uncharged)_detail.png",
            name="Pyramid Curse",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Burnt Page": Count(100), "Tome of Fire": Count(1), "Phoenix": Count(1)},
            id=23,
            image="https://oldschool.runescape.wiki/images/Burnt_page_detail.png",
            name="Wintertodt",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Crystal armour seed": Count(3),
                "Enhanced crystal weapon seed": Count(1),
                "Youngllef": Count(1),
            },
            id=24,
            image="https://oldschool.runescape.wiki/images/Youngllef_chathead.png",
            name="Crystal Grail",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"CoX Purple": Count(3), "CoX Megarare": Count(1)},
            id=25,
            image="https://oldschool.runescape.wiki/images/Arcane_prayer_scroll_detail.png",
            name="Chambers of Xeric",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Moons unique": Count(5)},
            id=26,
            image="https://oldschool.runescape.wiki/images/Blood_moon_helm_detail.png",
            name="Moons of Peril",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Abyssal whip|Brine sabre|Leaf bladed battleaxe|Leaf bladed sword|Black mask|Dark bow|Warped sceptre|Sulphur blades|Dragon chainbody|Long bone|Xeric’s talisman|Eternal gem|Basilisk jaw": Some(
                    {
                        "Abyssal whip": Count(1),
                        "Brine sabre": Count(1),
                        "Leaf bladed battleaxe": Count(1),
                        "Leaf bladed sword": Count(1),
                        "Black mask": Count(1),
                        "Dark bow": Count(1),
                        "Warped sceptre": Count(1),
                        "Sulphur blades": Count(1),
                        "Dragon chainbody": Count(1),
                        "Long bone": Count(1),
                        "Xeric’s talisman": Count(1),
                        "Eternal gem": Count(1),
                        "Basilisk jaw": Count(1),
                    },
                    5,
                ),
                "Imbued heart": Count(1),
            },
            id=27,
            image="https://oldschool.runescape.wiki/images/Twisted_slayer_helmet_detail.png",
            name="Miscellaneous Slayer",
            description="Achieve five miscellaneous slayer related items from the list or get an imbued heart."
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"ToA Purple": Count(5), "Tumeken's Shadow": Count(1)},
            id=28,
            image="https://oldschool.runescape.wiki/images/Fossilised_dung_detail.png",
            name="Tombs of Amascut",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Sarachnis cudgel": Count(3), "Jar of eyes": Count(1), "Sraracha": Count(1)},
            id=30,
            image="https://oldschool.runescape.wiki/images/Giant_egg_sac(full)_detail.png",
            name="Sarachnis",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Guild hunter outfit piece": Count(5), "Quetzin": Count(1)},
            id=31,
            image="https://oldschool.runescape.wiki/images/Quetzin_detail.png",
            name="Hunter Rumors",
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"DK Ring": Count(6)},
            id=32,
            image="https://oldschool.runescape.wiki/images/Berserker_ring_detail.png",
            name="DKS Rings",
            description="Any 6 ring drops. Ring of life not included."
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"DT2 Unique": Count(3), "DT2 Pet": Count(1)},
            id=33,
            image="https://oldschool.runescape.wiki/images/Executioner's_axe_head_detail.png",
            name="Desert Treasure II",
            description="Any 3 Desert Treasure II uniques, including ingots. Any DT2 pet will also complete the tile."
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {"Perilous Moons Colosseum": Count(1)},
            id=35,
            image="https://oldschool.runescape.wiki/images/Executioner's_axe_head_detail.png",
            name="Bonk Bonk",
            description="Complete the Colosseum using gear from Moons of Peril for each applicable slot (Rest is fine to fill in)."
        ),
        Tile(
            TileTheme.MISCELLANEOUS,
            {
                "Soaked Page|Tome of Water|Tiny Tempor": Some(
                    {
                        "Soaked Page": Count(100),
                        "Tome of Water": Count(1),
                        "Tiny Tempor": Count(1),
                    }
                ),
            },
            id=36,
            image="https://oldschool.runescape.wiki/images/Soaked_page_detail.png",
            name="Tempoross",
            description="Be sure to send an image of an empty reward pool before pulling rewards that you're gong to submit for this tile.",
        ),
        # Hard tiles
        Tile(
            TileTheme.HARD,
            {"Infernal Cape": Count(3)},
            id=10,
            image="https://oldschool.runescape.wiki/images/Infernal_cape_detail.png",
            name="Inferno",
            description="Acquire three infernal capes (Zuk tasks allowed).",
        ),
        Tile(
            TileTheme.HARD,
            {"Nex Unique": Count(2)},
            id=9,
            image="https://oldschool.runescape.wiki/images/Torva_full_helm_detail.png",
            name="Nex",
            description="""
                Obtain any two nex uniques (Dupes and pets allowed)\n
                Torva platebody
                Torva plaelegs
                Torva helmet
                Ancient hilt
                Nihil horn
                Nexling
            """,
        ),
        Tile(
            TileTheme.HARD,
            {"Sunfire splinter": Count(150000)},
            id=6,
            image="https://oldschool.runescape.wiki/images/Sunfire_splinters_4_detail.png",
            name="Blessings of Ralos",
            description="""
                Acquire 150k total splinters from the Colosseum. Unique items can be submitted at the below values worth of sunfire splinters.\n
                Echo crystal: 5k each
                Sunfire armor: 10k each piece
                Tonalztics of ralos: 15k
                Dizana's quiver: 4k each
            """,
        ),
        # Challenge tiles
        Tile(
            TileTheme.CHALLENGE,
            {
                "Sunfire splinter": Count(150000),
            },
            id=1,
            image="https://oldschool.runescape.wiki/images/Quests.png",
            name="Wiki Gear",
            description="TBD",
        ),
        Tile(
            TileTheme.CHALLENGE,
            {
                "Sledding time": Count(1),
            },
            id=34,
            image="https://oldschool.runescape.wiki/images/Sled_(unwaxed)_detail.png",
            name="Cool for the Summer",
            description='Achieve a sub 50 second sled time. To learn more about this activity, search for "Sled Racing" on the Wiki.',
        ),
        Tile(
            TileTheme.CHALLENGE,
            {
                "Sunfire splinter": Count(150000),
            },
            id=29,
            image="https://oldschool.runescape.wiki/images/Tzkal_slayer_helmet_detail.png",
            name="Zoomies",
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
            description="This tile was autogenerated for testing purposes just to fill the whole board.\nIf this shows up DURING bingo, which it NEVER should, something has gone HORRIBLY wrong and you should contact bingo moderation immideately :)",
        )

    # Generate board connections
    board: Dict[int, GraphNode] = {}
    for key, tile in tile_dict.items():
        tile.state = TileState.UNLOCKED
        node = board.setdefault(key, GraphNode(tile))
        for n in neighbor_map[key]:
            node.add_neighbor(n)

    return board

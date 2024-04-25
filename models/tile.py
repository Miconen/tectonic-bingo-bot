from dataclasses import dataclass
from typing import Dict
from enum import Enum
from abc import ABC, abstractmethod


class Color(Enum):
    GREEN = 0x00FF00
    RED = 0xFF0000
    BLUE = 0x0000FF
    YELLOW = 0xFFFF00
    PURPLE = 0x800080
    ORANGE = 0xFFA500
    BLACK = 0x000000
    WHITE = 0xFFFFFF
    GREY = 0x808080
    PINK = 0xFFC0CB
    BROWN = 0xA52A2A
    CYAN = 0x00FFFF
    TEAL = 0x008080
    LIME = 0x00FF00
    MAROON = 0x800000
    NAVY = 0x000080
    OLIVE = 0x808000
    SILVER = 0xC0C0C0
    AQUA = 0x00FFFF
    FUCHSIA = 0xFF00FF
    LAVENDER = 0xE6E6FA
    TURQUOISE = 0x40E0D0
    VIOLET = 0xEE82EE
    INDIGO = 0x4B0082
    KHAKI = 0xF0E68C
    MAGENTA = 0xFF00FF
    SALMON = 0xFA8072
    SEAGREEN = 0x2E8B57
    SKYBLUE = 0x87CEEB
    THISTLE = 0xD8BFD8
    TOMATO = 0xFF6347
    WHEAT = 0xF5DEB3
    BEIGE = 0xF5F5DC
    CRIMSON = 0xDC143C
    DARKGREEN = 0x006400
    DARKORANGE = 0xFF8C00
    DARKVIOLET = 0x9400D3
    DEEPPINK = 0xFF1493
    FIREBRICK = 0xB22222
    GOLDENROD = 0xDAA520
    LIGHTBLUE = 0xADD8E6
    LIGHTCORAL = 0xF08080
    LIGHTGREEN = 0x90EE90
    LIGHTPINK = 0xFFB6C1
    LIGHTSALMON = 0xFFA07A


class TileState(Enum):
    UNKNOWN = 0
    UNLOCKED = 1
    LOCKED = 2
    COMPLETED = 3


class TileTheme(Enum):
    SKILLING = Color.LIGHTBLUE.value
    CA = Color.RED.value
    DROPS = Color.ORANGE.value
    PVM = Color.YELLOW.value
    MINIGAMES = Color.PURPLE.value
    MISCELLANEOUS = Color.WHITE.value


class Criteria(ABC):
    @abstractmethod
    def is_satisfied(self) -> bool:
        pass

    @abstractmethod
    def submit(self, inc: int, key: str) -> bool:
        pass


@dataclass
class Submission:
    player: str
    url: str
    approved: bool
    approved_by: str
    timestamp: str


@dataclass
class Tile:
    id: int
    image: str
    name: str
    description: str
    state: TileState
    theme: TileTheme
    required_for_completetion: int
    requirements: Dict[str, Criteria]

    # Additional functionalities can be added as methods within the class
    def is_complete(self) -> bool:
        """Check if the tile is complete."""
        return self.state == TileState.COMPLETED

    def is_unlocked(self) -> bool:
        """Check if the tile is unlocked."""
        return self.state == TileState.UNLOCKED

    def check_complete(self) -> bool:
        """Check if the tile requirements are completed."""
        for requirement in self.requirements.values():
            if not requirement.is_satisfied():
                return False

        return True

    def complete(self):
        """Mark the tile as completed."""
        self.state = TileState.COMPLETED

    def submit(self, key: str, amount: int):
        """Submit a requirement to unlock the tile."""
        done = False
        if key in self.requirements:
            done = self.requirements[key].submit(amount, key)

        return done

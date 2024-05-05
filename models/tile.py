import discord

from dataclasses import dataclass
from typing import Dict, List
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
    CHALLENGE = Color.PURPLE.value
    HARD = Color.RED.value
    RAIDS = Color.YELLOW.value
    MISCELLANEOUS = Color.ORANGE.value


class Criteria(ABC):
    threshold: int

    @abstractmethod
    def is_satisfied(self) -> bool:
        pass

    @abstractmethod
    def submit(self, inc: int, key: str) -> bool:
        pass

    @abstractmethod
    def would_complete(self, inc: int, key: str) -> bool:
        pass

    @abstractmethod
    def get_count(self) -> int:
        pass


@dataclass
class Submission:
    player: str
    url: str
    approved: bool
    approved_by: str
    timestamp: str


@dataclass
class Proof:
    approved: bool
    task: str
    amount: int
    submitted_at: float
    submitted_by: int
    message: str | None = None
    approved_at: float | None = None
    approved_by: int | None = None


@dataclass
class Tile:
    theme: TileTheme
    requirements: Dict[str, Criteria]
    id: int = 0
    state: TileState = TileState.LOCKED
    image: str = ""
    name: str = ""
    description: str = ""
    required_for_completetion: int = 1
    rules_link: str = ""
    proof: List[Proof] | None = None

    # Additional functionalities can be added as methods within the class
    def is_complete(self) -> bool:
        """Check if the tile is complete."""
        return self.state == TileState.COMPLETED

    def is_unlocked(self) -> bool:
        """Check if the tile is unlocked."""
        return self.state == TileState.UNLOCKED

    def check_complete(self) -> bool:
        """Check if the tile requirements are completed."""
        count = 0
        for requirement in self.requirements.values():
            if requirement.is_satisfied():
                count += 1

        return count >= self.required_for_completetion

    def complete(self):
        """Mark the tile as completed."""
        self.state = TileState.COMPLETED

    def remove_submission(self, proof: Proof):
        """Remove a submission from the tile."""
        removed = False

        for k in self.requirements.keys():
            if proof.task in k.split("|"):
                self.requirements[k].submit(-proof.amount, proof.task)
                removed = True

        return removed

    def submit(self, key: str, amount: int):
        """Submit a requirement to unlock the task."""
        done = False

        for k in self.requirements.keys():
            if key in k.split("|"):
                done = self.requirements[k].submit(amount, key)

        return done

    def would_complete_task(self, key: str, amount: int):
        """Check if submitting a requirement would complete the task."""
        # Split the key by "|", this is a hacky way to support multiple keys in one string
        keys = key.split("|")
        for k in keys:
            if k in self.requirements:
                return self.requirements[k].would_complete(amount, k)

        return False

    def would_complete_tile(self, key: str, amount: int):
        """Check if submitting a requirement would complete the tile."""
        for requirement in self.requirements.values():
            if not requirement.is_satisfied() and not requirement.would_complete(
                amount, key
            ):
                return False

        return True

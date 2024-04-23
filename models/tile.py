from dataclasses import dataclass
from typing import Dict
from enum import Enum
from abc import ABC, abstractmethod

class TileState(Enum):
    UNKNOWN = 0
    UNLOCKED = 1
    LOCKED = 2
    COMPLETED = 3

class Criteria(ABC):
    @abstractmethod
    def is_satisfied(self) -> bool:
        pass
    @abstractmethod
    def submit(self, inc: int, key: str) -> bool:
        pass

@dataclass
class Tile:
    id: int
    name: str
    # TODO: Add image field
    description: str
    state: TileState
    required_for_completetion: int
    requirements: Dict[str, Criteria]

    # Additional functionalities can be added as methods within the class
    def is_complete(self) -> bool:
        """Check if the tile is complete."""
        return self.state == TileState.COMPLETED

    def is_unlocked(self) -> bool:
        """Check if the tile is unlocked."""
        return self.state != TileState.LOCKED

    def complete(self):
        """Mark the tile as completed."""
        for requirement in self.requirements.values():
            if not requirement.is_satisfied(): return

        self.state = TileState.COMPLETED

    def submit(self, key: str, inc: int):
        """Submit a requirement to unlock the tile."""
        done = False
        if key in self.requirements:
            done = self.requirements[key].submit(inc, key)

        if done: return "Requirement completed"

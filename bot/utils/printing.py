from typing import Dict
from models.tile import Criteria
from models.criteria import Count
from models.tile import Tile


def print_requirements(requirements: Dict[str, Criteria]):
    res = []

    for key, req in requirements.items():
        completed = "✅" if req.is_satisfied() else "⬜"

        k = key.split("|")
        # Formats the key like so: 1, 2, 3, 4 or 5
        joined_key = k[0] if len(k) == 1 else ", ".join(k[:-1]) + " or " + k[-1]

        if isinstance(req, Count) and req.threshold > 1:
            res.append(f"{completed} - {joined_key} ({req.count}/{req.threshold})")
            continue

        res.append(f"{completed} - {joined_key}")

    return "\n".join(res)


def print_requirement_progress(tile: Tile):
    done = 0
    for req in tile.requirements.values():
        if req.is_satisfied():
            done = done + 1

    return f"{done}/{tile.required_for_completetion}"

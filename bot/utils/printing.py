from typing import Dict
from models.criteria import Some, Count
from models.tile import Criteria
from models.tile import Tile


def print_requirements(requirements: Dict[str, Criteria]):
    res = []

    for key, req in requirements.items():
        completed = "✅" if req.is_satisfied() else "⬜"

        if isinstance(req, Some):
            group_title = f"{completed} **Complete {req.threshold} of the following**"
            res.append(group_title)

            for k, v in req.criteria.items():
                c = "✅" if v.is_satisfied() else "⬜"
                s = get_req_string(k, v, c)
                res.append(s)

        if isinstance(req, Count):
            group_title = f"{completed} **Complete the following**"
            res.append(group_title)

            s = get_req_string(key, req, completed)
            res.append(s)

        res.append("")

    return "\n".join(res)


def get_req_string(string: str, criteria: Criteria, status: str):
    req_base = "\u1CBC\u1CBC\u1CBC{} {}{}"

    return req_base.format(
        status,
        string,
        (
            f" ({criteria.get_count()}/{criteria.threshold})"
            if criteria.threshold > 1
            else ""
        ),
    )


def print_requirement_progress(tile: Tile):
    done = 0
    for req in tile.requirements.values():
        if req.is_satisfied():
            done = done + 1

    return f"{done}/{tile.required_for_completetion} completed"

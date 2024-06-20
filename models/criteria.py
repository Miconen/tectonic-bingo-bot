from typing import Dict
from functools import reduce

from bot.utils.input import sanitize_string
from models.tile import Criteria


class Count(Criteria, object):
    threshold: int
    count: int

    def __init__(self, threshold: int):
        self.threshold = threshold
        self.count = 0

    def is_satisfied(self) -> bool:
        return self.count >= self.threshold

    def submit(self, inc: int, key: str) -> bool:
        self.count += inc
        return self.is_satisfied()

    def would_complete(self, inc: int, key: str) -> bool:
        """
        Used by submissions to check if the requirement would complete the tile before the submission is accepted.
        """
        return self.count + inc >= self.threshold

    def get_count(self) -> int:
        return self.count


class Some(Criteria, object):
    criteria: Dict[str, Criteria]
    threshold: int

    def __init__(self, criteria: Dict[str, Criteria], required: int = 1):
        self.criteria = criteria
        self.threshold = required

    def is_satisfied(self) -> bool:
        count = 0
        for criteria in self.criteria.values():
            if criteria.is_satisfied():
                count += 1

        return count >= self.threshold

    def submit(self, inc: int, key: str) -> bool:
        for k, criteria in self.criteria.items():
            criteria_key = sanitize_string(k)
            if criteria_key == key:
                return criteria.submit(inc, key)

        return False

    def would_complete(self, inc: int, key: str) -> bool:
        count = 0
        for k, criteria in self.criteria.items():
            if k != key:
                continue
            if criteria.is_satisfied():
                count += 1
                continue

            if criteria.would_complete(inc, key):
                count += 1
                continue

        return count >= self.threshold

    def get_count(self) -> int:
        return reduce(
            lambda acc, elem: acc + int(elem.is_satisfied()), self.criteria.values(), 0
        )

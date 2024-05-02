from typing import Dict

from models.tile import Criteria


class Count(Criteria):
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


class OneOf(Criteria):
    criteria: Dict[str, Criteria]
    required_for_completion: int

    def __init__(self, criteria: Dict[str, Criteria], required: int = 1):
        self.criteria = criteria
        self.required_for_completion = required

    def is_satisfied(self) -> bool:
        count = 0
        for criteria in self.criteria.values():
            if criteria.is_satisfied():
                count += 1

        return count >= self.required_for_completion

    def submit(self, inc: int, key: str) -> bool:
        for k, criteria in self.criteria.items():
            if k == key:
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

        return count >= self.required_for_completion

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

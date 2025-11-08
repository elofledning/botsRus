from typing import List
from src.bot import Bot


class BotRoster:
    """Simple roster managing available bots."""

    def __init__(self, bots: List[Bot] = None):
        self.bots: List[Bot] = bots or []

    def add(self, bot: Bot) -> None:
        self.bots.append(bot)

    def get_bots(self, n: int) -> List[Bot]:
        return self.bots[:n]

    def all(self) -> List[Bot]:
        return list(self.bots)

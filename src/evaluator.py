from typing import Iterable
from src.deck import Card


def best_high_card(cards: Iterable[Card]) -> int:
    """Return the highest card rank found in `cards`."""
    ranks = [c.rank for c in cards]
    return max(ranks) if ranks else 0

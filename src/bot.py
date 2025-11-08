from typing import List, Optional
from src.deck import Card
import uuid


class Bot:
    """Simple Bot base class storing an id, name and current hand."""

    def __init__(self, name: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name or f"Bot-{self.id[:8]}"
        self.hand: List[Card] = []

    def receive(self, card: Card) -> None:
        """Receive a single card (called by Dealer)."""
        self.hand.append(card)

    def reset_hand(self) -> None:
        self.hand = []


class RandomBot(Bot):
    """A bot with no strategy; used for simulation and testing."""

    def __init__(self, name: Optional[str] = None):
        super().__init__(name)

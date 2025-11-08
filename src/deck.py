from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Sequence, Union
import random


class Suit(Enum):
    HEARTS = 'Hearts'
    CLUBS = 'Clubs'
    DIAMONDS = 'Diamonds'
    SPADES = 'Spades'


@dataclass(frozen=True)
class Card:
    """Immutable playing card.

    rank: int where 2..14 (Ace=14)
    suit: Suit
    """
    suit: Suit
    rank: int

    def __str__(self) -> str:
        name = {11: 'Jack', 12: 'Queen', 13: 'King', 14: 'Ace'}.get(self.rank, str(self.rank))
        return f"{name} {self.suit.value}"

    def to_short_string(self) -> str:
        """Returns a compact representation like 'A♠' for web display"""
        rank_map = {
            14: 'A', 13: 'K', 12: 'Q', 11: 'J',
            10: '10', 9: '9', 8: '8', 7: '7',
            6: '6', 5: '5', 4: '4', 3: '3', 2: '2'
        }
        suit_map = {
            Suit.HEARTS: '♥',
            Suit.DIAMONDS: '♦',
            Suit.CLUBS: '♣',
            Suit.SPADES: '♠'
        }
        return f"{rank_map[self.rank]}{suit_map[self.suit]}"

    def __repr__(self) -> str:
        return f"Card(suit={self.suit}, rank={self.rank})"


class Deck:
    """Standard 52-card deck with safe dealing API."""

    def __init__(self, rng: Optional[random.Random] = None):
        self._rng = rng or random.Random()
        self.cards: List[Card] = []
        self.build()

    def build(self) -> None:
        """(Re)build a fresh 52-card deck. Ranks 2..14 (Ace high)."""
        self.cards = [Card(suit, rank) for suit in Suit for rank in range(2, 15)]

    def reset(self) -> None:
        self.build()

    def shuffle(self, seed: Optional[int] = None) -> None:
        """Shuffle the deck. If seed is provided, use deterministic RNG for tests."""
        if seed is not None:
            self._rng = random.Random(seed)
        # use the instance RNG for deterministic shuffling when seeded
        self._rng.shuffle(self.cards)

    def remaining(self) -> int:
        return len(self.cards)

    def deal(self, count: int = 1) -> Union[Card, List[Card]]:
        """Deal `count` cards from the top of the deck.

        Raises:
            ValueError: if there are not enough cards to deal.
        """
        if count < 1:
            raise ValueError("count must be >= 1")
        if count > len(self.cards):
            raise ValueError(f"Not enough cards to deal: requested {count}, available {len(self.cards)}")
        if count == 1:
            return self.cards.pop()
        dealt: List[Card] = [self.cards.pop() for _ in range(count)]
        # return in same order as drawn (top-first)
        return dealt

    def burn(self, n: int = 1) -> None:
        """Discard n cards from the top of the deck."""
        if n < 0:
            raise ValueError("n must be >= 0")
        if n > len(self.cards):
            raise ValueError("Not enough cards to burn")
        for _ in range(n):
            self.cards.pop()

    def peek(self, n: int = 1) -> List[Card]:
        """Return top `n` cards without removing them."""
        if n < 0:
            raise ValueError("n must be >= 0")
        return list(reversed(self.cards[-n:])) if n else []

    def cut(self, position: Optional[int] = None) -> None:
        """Cut the deck at `position` (0..remaining), default random cut."""
        if position is None:
            position = self._rng.randint(0, len(self.cards))
        if not (0 <= position <= len(self.cards)):
            raise ValueError("position out of range")
        self.cards = self.cards[position:] + self.cards[:position]


class Dealer:
    """Dealer that owns a deck and can deal to players or the table.

    This class focuses on card movement only; player/bot state lives elsewhere.
    """

    def __init__(self, deck: Optional[Deck] = None):
        self.deck = deck or Deck()
        self.community: List[Card] = []

    def deal_to_players(self, players: Sequence['PlayerLike'], cards_each: int = 2) -> None:
        """Deal `cards_each` cards to each player. Players must implement `receive(cards: List[Card])`."""
        for _ in range(cards_each):
            for p in players:
                card = self.deck.deal()
                # assume player's receive accepts a single Card
                p.receive(card)

    def deal_community(self, n: int) -> List[Card]:
        """Deal `n` community cards and append to self.community."""
        cards = self.deck.deal(n) if n > 1 else [self.deck.deal()]
        # ensure list
        if isinstance(cards, Card):
            cards = [cards]
        # top of deck is last popped, preserve dealing order
        self.community.extend(cards)
        return cards

    def burn(self, n: int = 1) -> None:
        self.deck.burn(n)


# A minimal protocol hint for player-like objects used by Dealer.deal_to_players
class PlayerLike:
    def receive(self, card: Card) -> None:  # pragma: no cover - simple protocol
        raise NotImplementedError


__all__ = ["Card", "Suit", "Deck", "Dealer"]
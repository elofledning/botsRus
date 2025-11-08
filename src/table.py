import random
from typing import List, Dict, Optional
from src.deck import Deck, Dealer, Card
from src.bot import Bot
from src.evaluator import best_high_card


class Table:
    """Table orchestrates many hands between a set of bots and awards points to winners.

    Simplified rules: each hand deals 2 hole cards to each player and 5 community cards.
    Winner is determined by the highest single card rank across the 7-card pool (hole + community).
    Ties are broken randomly.
    """

    def __init__(self, players: List[Bot], dealer: Optional[Dealer] = None, games_to_play: int = 1000):
        if len(players) < 2:
            raise ValueError("Table requires at least two players")
        self.players = players
        self.dealer = dealer or Dealer(Deck())
        self.games_to_play = games_to_play

    def run(self, num_games: Optional[int] = None, rng: Optional[random.Random] = None) -> Dict[str, int]:
        rng = rng or random.Random()
        games = num_games or self.games_to_play
        scores: Dict[str, int] = {p.id: 0 for p in self.players}

        for _ in range(games):
            # prepare deck and players
            self.dealer.deck.reset()
            self.dealer.deck.shuffle()
            self.dealer.community = []
            for p in self.players:
                p.reset_hand()

            # deal two hole cards to each player
            self.dealer.deal_to_players(self.players, cards_each=2)

            # deal 5 community cards (flop+turn+river simplified)
            community = self.dealer.deal_community(5)

            # evaluate each player's best high card
            best_value = -1
            best_players = []
            for p in self.players:
                pool = p.hand + self.dealer.community
                value = best_high_card(pool)
                if value > best_value:
                    best_value = value
                    best_players = [p]
                elif value == best_value:
                    best_players.append(p)

            # choose a winner among best_players randomly
            winner = rng.choice(best_players)
            scores[winner.id] += 1

        return scores

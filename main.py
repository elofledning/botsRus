#!/usr/bin/env python3

import sys
import os
from typing import Dict, List

# ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.bot import RandomBot
from src.roster import BotRoster
from src.floor import FloorManager


def print_scores(scores: Dict[str, int], bot_names: Dict[str, str]) -> None:
    """Print tournament results sorted by score."""
    print("\nTournament Results:")
    print("-" * 40)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    for bot_id, score in sorted_scores:
        name = bot_names[bot_id]
        print(f"{name:<20} {score:>6} points")


def main():
    # Create 12 random bots (will be split into 2 tables of 6)
    bots = [RandomBot(f"Bot-{i+1:02d}") for i in range(12)]
    bot_names = {bot.id: bot.name for bot in bots}

    # Register bots with roster
    roster = BotRoster(bots)

    # Create floor manager and run tournament
    floor = FloorManager(roster)
    print("Starting tournament with 12 bots across 2 tables...")
    print("Playing 1000 hands per table...")
    scores = floor.run_tournament(players_per_table=6, games_per_table=1000)

    # Print results
    print_scores(scores, bot_names)


if __name__ == "__main__":
    main()
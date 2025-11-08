import os
import sys

# ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.bot import RandomBot
from src.table import Table


def test_table_runs_and_awards_points():
    bots = [RandomBot(name=f"B{i}") for i in range(3)]
    table = Table(bots, games_to_play=100)
    scores = table.run()
    # total points must equal number of games
    total = sum(scores.values())
    assert total == 100
    # each bot must have an entry
    for b in bots:
        assert b.id in scores

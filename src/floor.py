from typing import List, Dict
from src.roster import BotRoster
from src.table import Table
from src.bot import Bot


class FloorManager:
    """High level orchestrator: assigns bots to tables and runs tournaments."""

    def __init__(self, roster: BotRoster):
        self.roster = roster

    def run_tournament(self, players_per_table: int = 6, games_per_table: int = 1000) -> Dict[str, int]:
        bots = self.roster.all()
        ranking: Dict[str, int] = {b.id: 0 for b in bots}

        # partition bots into tables
        for i in range(0, len(bots), players_per_table):
            table_bots = bots[i : i + players_per_table]
            if len(table_bots) < 2:
                continue
            table = Table(table_bots, games_to_play=games_per_table)
            scores = table.run()
            # award points: winner per hand already tallied; aggregate into ranking
            for bot_id, pts in scores.items():
                ranking[bot_id] = ranking.get(bot_id, 0) + pts

        return ranking

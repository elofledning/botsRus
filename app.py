from flask import Flask, render_template, jsonify
from src.bot import RandomBot
from src.roster import BotRoster
from src.floor import FloorManager
import json
from datetime import datetime

app = Flask(__name__)

# Store tournament history
tournament_history = []

def run_tournament():
    """Run a tournament and return the results including per-game history."""
    bots = [RandomBot(f"Bot-{i+1:02d}") for i in range(12)]
    bot_names = {bot.id: bot.name for bot in bots}
    roster = BotRoster(bots)
    floor = FloorManager(roster)

    result = floor.run_tournament(players_per_table=6, games_per_table=1000)

    # Format aggregated scores for the frontend and attach history with names
    scores = [{'name': bot_names.get(bot_id, bot_id), 'points': points} for bot_id, points in result['scores'].items()]

    # history: list of {game, winner_id, winner_name, winning_value}
    history = []
    for entry in result['history']:
        history.append({
            'game': entry['game'],
            'winner_id': entry['winner_id'],
            'winner_name': bot_names.get(entry['winner_id'], entry['winner_id']),
            'winning_value': entry.get('winning_value'),
        })

    payload = {
        'timestamp': datetime.now().isoformat(),
        'scores': sorted(scores, key=lambda x: x['points'], reverse=True),
        'history': history,
    }
    tournament_history.append(payload)
    return payload

@app.route('/')
def index():
    """Render the dashboard page."""
    return render_template('index.html')

@app.route('/api/tournament/latest')
def get_latest_tournament():
    """Return the latest tournament results."""
    if not tournament_history:
        result = run_tournament()
    else:
        result = tournament_history[-1]
    return jsonify(result)

@app.route('/api/tournament/new')
def new_tournament():
    """Run a new tournament and return results."""
    result = run_tournament()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
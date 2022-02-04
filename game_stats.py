import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize stats."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = self._read_stats_json()

    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.ships_remaining = self.settings.ship_limit
        self.score = 0

    def _read_stats_json(self):
        """Reads the JSON file and sees if we already have a high score."""
        try: 
            with open('stats/score.json') as f:
                data = json.load(f)
                return data["high score"]
        except FileNotFoundError:
            return 0
        except json.decoder.JSONDecodeError:
            return 0    


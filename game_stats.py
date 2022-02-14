import json

from enum import Enum, unique 

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize stats."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self._read_stats_json()
        self.MAINMENU = 1
        self.GAMEPLAY = 2
        self.PAUSE = 3
        self.GAMEOVER = 4
        self.state = self.MAINMENU


    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.ships_remaining = self.settings.ship_limit
        self.charges_remaining = self.settings.beam_limit
        self.score = 0

    def _read_stats_json(self):
        """Reads the score.json file and sees if we already have a high score."""
        try: 
            with open('stats/score.json') as f:
                data = json.load(f)
                return data["high score"]
        except FileNotFoundError:
            return 0
        except json.decoder.JSONDecodeError:
            return 0    


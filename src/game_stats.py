import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize stats."""
        self.game = ai_game
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self._read_stats_json()
        self.game.settings.play_music = self._read_music_json()
        self.game.settings.play_sfx = self._read_sfx_json()
        self.game.settings.turbo_speed = self._read_turbo_json()
        self.game.settings.cinematic_bars = self._read_vfx_json()
        self.game.settings.scaled_gfx = self._read_gfx_json()
        self.game.keybinds.current_scheme = self._read_controls_json()
        self.game.keybinds.set_movement_scheme()
        self.game.keybinds.set_combat_scheme()
        self.game.options_menu._change_controls_text()
        self.game.options_menu._change_gfx_text()
        self.game.options_menu._change_window_size()
        self.MAINMENU = 1
        self.GAMEPLAY = 2
        self.PAUSE = 3
        self.GAMEOVER = 4
        self.OPTIONSMENU = 5
        self.state = self.MAINMENU
        self.pause_state = 0
        self.music_state = {"GAMEPLAY": False, "MENU": False, "GAMEOVER": False, "PAUSE": False}

    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.ships_remaining = self.settings.ship_limit
        self.charges_remaining = self.settings.beam_limit
        self.score = 0
        self.hidden_score = 0

    def _read_stats_json(self):
        """Reads the score.json file and sees if we already have a high score."""
        try: 
            with open('stats/score.json') as f:
                data = json.load(f)
                return data["high_score"]
        except FileNotFoundError:
            return 0
        except json.decoder.JSONDecodeError:
            return 0    
        except KeyError: 
            return 0

    def _read_music_json(self):
        """Reads the settings.json file and sees if we already have an option for playing music."""
        try: 
            with open('stats/settings.json') as f:
                data = json.load(f)
                return data["play_music"]
        except FileNotFoundError:
            return True
        except json.decoder.JSONDecodeError:
            return True 
        except KeyError: 
            return True

    def _read_sfx_json(self):
        """Reads the settings.json file and sees if we already have an option for playing SFX."""
        try: 
            with open('stats/settings.json') as f:
                data = json.load(f)
                return data["play_sfx"]
        except FileNotFoundError:
            return True
        except json.decoder.JSONDecodeError:
            return True 
        except KeyError: 
            return True

    def _read_vfx_json(self):
        """Reads the settings.json file and sees if we already have an option for cinematic bars."""
        try: 
            with open('stats/settings.json') as f:
                data = json.load(f)
                return data["cinematic_mode"]
        except FileNotFoundError:
            return True
        except json.decoder.JSONDecodeError:
            return True 
        except KeyError: 
            return True

    def _read_turbo_json(self):
        """Reads the settings.json file and sees if we already have an option for turbo mode."""
        try: 
            with open('stats/settings.json') as f:
                data = json.load(f)
                return data["game_speed"]
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError:
            return False
        except KeyError: 
            return False

    def _read_controls_json(self):
        """Reads the settings.json file and sees if we already have an option for controls bars."""
        try: 
            with open('stats/settings.json') as f:
                data = json.load(f)
                return data["control_scheme"]
        except FileNotFoundError:
            return 1
        except json.decoder.JSONDecodeError:
            return 1
        except KeyError: 
            return 1

    def _read_gfx_json(self):
        """Reads the settings.json file and sees if we already have an option for window size."""
        try: 
            with open('stats/settings.json') as f:
                data = json.load(f)
                return data["window_mode"]
        except FileNotFoundError:
            return False
        except json.decoder.JSONDecodeError:
            return False
        except KeyError: 
            return True


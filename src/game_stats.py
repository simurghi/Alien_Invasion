import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize stats."""
        self.game = ai_game
        self.settings = ai_game.settings
        self.reset_stats()
        self.options_data = self._read_options_json()
        self.high_score = self._read_stats_json()
        self._set_json_options_settings()
        self._set_json_keybinds()
        self._update_menu_text_json()
        self._create_game_states()

    def _set_json_options_settings(self):
        """Sets current options preferences based on JSON file."""
        self.game.settings.play_music = self._read_music_json()
        self.game.settings.play_sfx = self._read_sfx_json()
        self.game.settings.turbo_speed = self._read_turbo_json()
        self.game.settings.cinematic_bars = self._read_vfx_json()
        self.game.settings.scaled_gfx = self._read_gfx_json()

    def _set_json_keybinds(self):
        """Sets key preset preference based on JSON file."""
        self.game.keybinds.current_scheme = self._read_controls_json()
        self.game.keybinds.set_movement_scheme()
        self.game.keybinds.set_combat_scheme()

    def _update_menu_text_json(self):
        """Updates menu text based on JSON file preferences."""
        self.game.options_menu._change_controls_text()
        self.game.options_menu._change_turbo_text()
        self.game.options_menu._change_gfx_text()
        self.game.options_menu._change_window_size()

    def _create_game_states(self):
        """Creates instance variables necessary for the game states to function."""
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

    def _read_options_json(self):
        """Reads the settings.json file and loads data if found."""
        try: 
            with open('stats/settings.json') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return 0
        except json.decoder.JSONDecodeError:
            return 0
        except KeyError: 
            return 0

    def _read_music_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for playing music."""
        if self.options_data:
            music_option = self.options_data.get("play_music")
            if music_option is not None:
                return music_option
            else:
                return True


    def _read_sfx_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for playing SFX."""
        if self.options_data:
            sfx_option = self.options_data.get("play_sfx")
            if sfx_option is not None:
                return sfx_option
            else:
                return True

    def _read_vfx_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for cinematic bars."""
        if self.options_data:
            vfx_option = self.options_data.get("cinematic_mode")
            if vfx_option is not None:
                return vfx_option
            else:
                return True

    def _read_turbo_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for turbo mode."""
        if self.options_data:
            turbo_option = self.options_data.get("game_speed")
            if turbo_option is not None:
                return turbo_option
            else:
                return False

    def _read_controls_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for controls."""
        if self.options_data:
            control_option = self.options_data.get("control_scheme")
            if control_option is not None:
                return control_option
            else:
                return 1

    def _read_gfx_json(self):
        """Searches the dictionary created from the settings.json file 
        and sees if we already have an option for window size."""
        if self.options_data:
            gfx_option = self.options_data.get("window_mode")
            if gfx_option is not None:
                return gfx_option
            else:
                return False

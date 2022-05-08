import json, pygame

class GameStats:
    """Class to track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize stats."""
        self.game = ai_game
        self.settings = ai_game.settings
        self.reset_stats()
        self.options_data = self._read_options_json()
        self.high_score = self._read_stats_json()
        self._set_json_options_settings()
        self._update_menu_text_json()

    def reset_stats(self):
        """Initialize stats that can change during the game."""
        self.ships_remaining = self.settings.ship_limit
        self.charges_remaining = self.settings.beam_limit
        self.score = 0
        self.hidden_score = 0

    def _set_json_options_settings(self):
        """Sets current options preferences based on JSON file."""
        self.game.settings.music_volume = self._read_music_json()
        self.game.settings.sound_volume = self._read_sfx_json()
        self.game.settings.speed = self._read_turbo_json()
        self.game.keybinds.controls = self._read_keybinds_json()
        self.game.settings.gfx_mode = self._read_gfx_json()
        self.game.settings.HUD = self._read_HUD_json()
        self.game.settings.show_score = self._read_score_json()

    def _update_menu_text_json(self):
        """Updates menu text based on JSON file preferences."""
        self.game.options_menu._change_turbo_text()
        self.game.options_menu._change_music_text()
        self.game.options_menu._change_sound_text()
        self.game.options_menu._change_gfx_text()
        self.game.options_menu._change_window_size()
        self.game.options_menu._change_HUD_text()
        self.game.options_menu._change_score_text()

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
            return None
        except json.decoder.JSONDecodeError:
            return None
        except KeyError: 
            return None

    def _read_music_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for playing music."""
        if self.options_data:
            music_option = self.options_data.get("music_volume")
            if music_option is not None:
                return music_option
            else:
                return 1.0
        else:
            return 1.0

    def _read_keybinds_json(self):
        """Searches the dictionary creates from the settings.json file 
        and sees if we already have a control mapping enabled."""
        if self.options_data:
            controls_option = self.options_data.get("controls")
            if controls_option is not None: 
                return controls_option
            else:
                return {"MOVELEFT": pygame.K_LEFT, "MOVERIGHT": pygame.K_RIGHT,
                "MOVEUP": pygame.K_UP, "MOVEDOWN": pygame.K_DOWN, "MISSILEATTACK": pygame.K_x, 
                "BEAMATTACK": pygame.K_c, "FLIPSHIP": pygame.K_z}
        else:
            return {"MOVELEFT": pygame.K_LEFT, "MOVERIGHT": pygame.K_RIGHT,
            "MOVEUP": pygame.K_UP, "MOVEDOWN": pygame.K_DOWN, "MISSILEATTACK": pygame.K_x, 
            "BEAMATTACK": pygame.K_c, "FLIPSHIP": pygame.K_z}


    def _read_sfx_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for playing SFX."""
        if self.options_data:
            sfx_option = self.options_data.get("sound_volume")
            if sfx_option is not None:
                return sfx_option
            else:
                return 1.0
        else:
            return 1.0

    def _read_turbo_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for turbo mode."""
        if self.options_data:
            turbo_option = self.options_data.get("game_speed")
            if turbo_option is not None:
                return turbo_option
            else:
                return 3
        else:
            return 3

    def _read_gfx_json(self):
        """Searches the dictionary created from the settings.json file 
        and sees if we already have an option for window size."""
        if self.options_data:
            gfx_option = self.options_data.get("window_mode")
            if gfx_option is not None:
                return gfx_option
            else:
                return 1
        else:
            return 1

    def _read_HUD_json(self):
        """Searches the dictionary created from the settings.json file 
        and sees if we already have an option for HUD preset."""
        if self.options_data:
            HUD_option = self.options_data.get("HUD_preset")
            if HUD_option is not None:
                return HUD_option
            else:
                return 1
        else:
            return 1

    def _read_score_json(self):
        """Searches the dictionary created from the settings.json file 
        and sees if we already have an option for displaying score."""
        if self.options_data:
            score_option = self.options_data.get("display_score")
            if score_option is not None:
                return score_option
            else:
                return True
        else:
            return True

    def dump_stats_json(self):
        """Dumps score and key game settings to a JSON file."""
        with open("stats/score.json", 'w') as f:
            json.dump({"high_score" : self.game.stats.high_score}, f)
        with open("stats/settings.json", 'w') as f:
            json.dump({"game_speed" : self.settings.speed,"music_volume": self.settings.music_volume,
                "sound_volume": self.settings.sound_volume, "window_mode": self.settings.gfx_mode,
                "display_score": self.settings.show_score, "HUD_preset": self.settings.HUD,
                "controls": self.game.keybinds.controls}, f)


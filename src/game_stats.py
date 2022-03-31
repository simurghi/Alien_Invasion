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
        self.game.settings.play_music = self._read_music_json()
        self.game.settings.play_sfx = self._read_sfx_json()
        self.game.settings.speed = self._read_turbo_json()
        self.game.settings.cinematic_bars = self._read_vfx_json()
        self.game.keybinds.controls = self._read_keybinds_json()
        self.game.keybinds.use_mouse = self._read_mouse_json()
        self.game.settings.scaled_gfx = self._read_gfx_json()
        self.game.settings.high_FPS = self._read_fps_json()

    def _update_menu_text_json(self):
        """Updates menu text based on JSON file preferences."""
        self.game.options_menu._change_turbo_text()
        self.game.options_menu._change_music_text()
        self.game.options_menu._change_sound_text()
        self.game.options_menu._change_gfx_text()
        self.game.options_menu._change_movie_text()
        self.game.options_menu._change_fps()
        self.game.options_menu._change_window_size()
        self.game.controls_menu._change_mouse_text()

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
            music_option = self.options_data.get("play_music")
            if music_option is not None:
                return music_option
            else:
                return True
        else:
            return True

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


    def _read_mouse_json(self):
        """Searches the dictionary created from the settings.json file 
        and sees if we already have an option for enabling mouse control ingame."""
        if self.options_data:
            mouse_option = self.options_data.get("mouse_enabled")
            if mouse_option is not None: 
                return mouse_option
            else:
                return False
        else:
            return False

    def _read_sfx_json(self):
        """Searches the dictionary created from the settings.json file
        and sees if we already have an option for playing SFX."""
        if self.options_data:
            sfx_option = self.options_data.get("play_sfx")
            if sfx_option is not None:
                return sfx_option
            else:
                return True
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
                return False
        else:
            return False

    def _read_fps_json(self):
        """Searches the dictionary created from the settings.json file 
        and sees if we already have an option for high FPS."""
        if self.options_data:
            fps_option = self.options_data.get("high_FPS")
            if fps_option is not None:
                return fps_option
            else:
                return False
        else:
            return False

    def dump_stats_json(self):
        """Dumps score and key game settings to a JSON file."""
        with open("stats/score.json", 'w') as f:
            json.dump({"high_score" : self.game.stats.high_score}, f)
        with open("stats/settings.json", 'w') as f:
            json.dump({"game_speed" : self.settings.speed,"play_music": self.settings.play_music,
                "play_sfx": self.settings.play_sfx, "cinematic_mode": self.settings.cinematic_bars, "window_mode":
                self.settings.scaled_gfx, "controls": self.game.keybinds.controls, 
                "mouse_enabled": self.game.keybinds.use_mouse, "high_FPS": self.settings.high_FPS}, f)


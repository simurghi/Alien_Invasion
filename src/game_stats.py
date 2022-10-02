import json
import pygame


class GameStats:
    """Class to track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize stats."""
        self.game = ai_game
        self.keybinds = self.game.keybinds
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
        """Set current options preferences based on JSON file."""
        self.game.settings.music_volume = self._read_music_json()
        self.game.settings.sound_volume = self._read_sfx_json()
        self.game.settings.speed = self._read_turbo_json()
        self.game.settings.speed_counter = self._read_turbo_counter_json()
        self.game.keybinds.controls = self._read_keybinds_json()
        self.game.settings.gfx_mode = self._read_gfx_json()
        self.game.settings.gfx_counter = self._read_gfx_counter_json()
        self.game.settings.HUD = self._read_HUD_json()
        self.game.settings.HUD_counter = self._read_HUD_counter_json()
        self.game.settings.score_mode = self._read_score_json()
        self.game.settings.score_counter = self._read_score_counter_json()
        self.game.settings.arrow_mode = self._read_dirarrow_json()
        self.game.settings.arrow_counter = self._read_dirarrow_counter_json()

    def _update_menu_text_json(self):
        """Update menu text based on JSON file preferences."""
        self.game.options_menu._change_turbo_text()
        self.game.options_menu._change_music_text()
        self.game.options_menu._change_sound_text()
        self.game.options_menu._change_gfx_text()
        self.game.options_menu._change_window_size()
        self.game.options_menu._change_HUD_text()
        self.game.options_menu._change_score_text()
        self.game.options_menu._change_dirarrow_text()

    def _read_stats_json(self):
        """Read the score.json file and sees if we already have a high score."""
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
        """Read the settings.json file and loads data if found."""
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
        """Search the dictionary created from the settings.json file
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
        """Search the dictionary creates from the settings.json file
        and sees if we already have a control mapping enabled."""
        if self.options_data:
            controls_option = self.options_data.get("controls")
            if controls_option is not None:
                return controls_option
            else:
                return {
                    self.keybinds.MOVELEFT: pygame.K_a,
                    self.keybinds.MOVERIGHT: pygame.K_d,
                    self.keybinds.MOVEUP: pygame.K_w,
                    self.keybinds.MOVEDOWN: pygame.K_s,
                    self.keybinds.MISSILEATTACK: pygame.K_j,
                    self.keybinds.BEAMATTACK: pygame.K_l,
                    self.keybinds.FLIPSHIP: pygame.K_k,
                }
        else:
            return {
                self.keybinds.MOVELEFT: pygame.K_a,
                self.keybinds.MOVERIGHT: pygame.K_d,
                self.keybinds.MOVEUP: pygame.K_w,
                self.keybinds.MOVEDOWN: pygame.K_s,
                self.keybinds.MISSILEATTACK: pygame.K_j,
                self.keybinds.BEAMATTACK: pygame.K_l,
                self.keybinds.FLIPSHIP: pygame.K_k,
            }

    def _read_sfx_json(self):
        """Search the dictionary created from the settings.json file
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
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for turbo mode."""
        if self.options_data:
            turbo_option = self.options_data.get("game_speed")
            if turbo_option is not None:
                return turbo_option
            else:
                return self.game.settings.GAME_SPEEDS[1]
        else:
            return self.game.settings.GAME_SPEEDS[1]

    def _read_turbo_counter_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for turbo mode."""
        if self.options_data:
            turbo_count_option = self.options_data.get("speed_counter")
            if turbo_count_option is not None:
                return turbo_count_option
            else:
                return 1
        else:
            return 1

    def _read_gfx_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for window size."""
        if self.options_data:
            gfx_option = self.options_data.get("window_mode")
            if gfx_option is not None:
                return gfx_option
            else:
                return self.game.settings.GFX_SETTINGS[0]
        else:
            return self.game.settings.GFX_SETTINGS[0]

    def _read_gfx_counter_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for window size."""
        if self.options_data:
            gfx_count_option = self.options_data.get("gfx_counter")
            if gfx_count_option is not None:
                return gfx_count_option
            else:
                return 0
        else:
            return 0

    def _read_HUD_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for HUD preset."""
        if self.options_data:
            HUD_option = self.options_data.get("HUD_preset")
            if HUD_option is not None:
                return HUD_option
            else:
                return self.game.settings.HUD_SETTINGS[0]
        else:
            return self.game.settings.HUD_SETTINGS[0]

    def _read_HUD_counter_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for HUD preset."""
        if self.options_data:
            HUD_count_option = self.options_data.get("HUD_counter")
            if HUD_count_option is not None:
                return HUD_count_option
            else:
                return 0
        else:
            return 0

    def _read_score_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for displaying score."""
        if self.options_data:
            score_option = self.options_data.get("display_score")
            if score_option is not None:
                return score_option
            else:
                return self.game.settings.SCORE_SETTINGS[0]
        else:
            return self.game.settings.SCORE_SETTINGS[0]

    def _read_score_counter_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for displaying score."""
        if self.options_data:
            score_counter_option = self.options_data.get("score_counter")
            if score_counter_option is not None:
                return score_counter_option
            else:
                return 0
        else:
            return 0

    def _read_dirarrow_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for displaying the direction arrow."""
        if self.options_data:
            dirarrow_option = self.options_data.get("arrow_setting")
            if dirarrow_option is not None:
                return dirarrow_option
            else:
                return self.game.settings.ARROW_SETTINGS[0]
        else:
            return self.game.settings.ARROW_SETTINGS[0]

    def _read_dirarrow_counter_json(self):
        """Search the dictionary created from the settings.json file
        and sees if we already have an option for displaying the direction arrow."""
        if self.options_data:
            dirarrow_counter_option = self.options_data.get("arrow_counter")
            if dirarrow_counter_option is not None:
                return dirarrow_counter_option
            else:
                return 0
        else:
            return 0

    def dump_stats_json(self):
        """Dump score and key game settings to a JSON file."""
        with open("stats/score.json", 'w') as f:
            json.dump({"high_score": self.game.stats.high_score}, f)
        with open("stats/settings.json", 'w') as f:
            json.dump(
                {
                    "game_speed": self.settings.speed,
                    "music_volume": self.settings.music_volume,
                    "sound_volume": self.settings.sound_volume,
                    "window_mode": self.settings.gfx_mode,
                    "display_score": self.settings.score_mode,
                    "score_counter": self.settings.score_counter,
                    "HUD_preset": self.settings.HUD,
                    "arrow_setting": self.settings.arrow_mode,
                    "arrow_counter": self.settings.arrow_counter,
                    "controls": self.game.keybinds.controls,
                    "HUD_counter": self.settings.HUD_counter,
                    "gfx_counter": self.settings.gfx_counter,
                    "speed_counter": self.settings.speed_counter,
                },
                f,
            )

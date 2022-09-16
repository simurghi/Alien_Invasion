from menu import *


class OptionsMenu(Menu):
    """Class that holds state and behaviour for the options menu."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self.enter_pressed = False
        self.index = 0
        self._set_cursor()
        self._set_initial_text()
        self._create_options_buttons()

    def _set_cursor(self):
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_rect.midright = (70, 70)
        self.x = float(self.cursor_rect.x)
        self.y = float(self.cursor_rect.y)

    def _set_initial_text(self):
        self.speed_state = self.game.settings.GAME_SPEEDS[self.game.settings.speed_counter]
        self.gfx_state = self.game.settings.GFX_SETTINGS[self.game.settings.gfx_counter]
        self.sfx_state = f"Sound: {self.game.settings.sound_volume * 100:.0f}%"
        self.music_state = f"Music: {self.game.settings.music_volume * 100:.0f}%"
        self.HUD_state = self.game.settings.HUD_SETTINGS[self.game.settings.HUD_counter]
        self.score_state = "Score: ON"
        self.dirarrow_state = "Arrows: Player"

    def _create_options_buttons(self):
        """Creates buttons for the options menu."""
        self.turbo_button = Button(self, self.speed_state, 250, 250)
        self.mute_button = Button(self, self.music_state, 250, 175)
        self.sfx_button = Button(self, self.sfx_state, 250, 100)
        self.gfx_button = Button(self, self.gfx_state, 250, 25)
        self.score_button = Button(self, self.gfx_state, 250, -50)
        self.HUD_button = Button(self, self.HUD_state, 250, -125)
        self.dirarrow_button = Button(self, self.dirarrow_state, 250, -200)
        self.back_button = Button(self, "Back", 250, -275)
        self.buttons = (
            self.turbo_button,
            self.mute_button,
            self.sfx_button,
            self.gfx_button,
            self.score_button,
            self.HUD_button,
            self.dirarrow_button,
            self.back_button,
        )
        self.menu_event_dict = {
                self.turbo_button: self._change_difficulty,
                self.mute_button: self._change_music_volume,
                self.sfx_button: self._change_sound_volume,
                self.gfx_button: self._change_game_resolution,
                self.score_button: self._update_score_setting,
                self.HUD_button: self._change_game_HUD,
                self.dirarrow_button: self._change_game_arrow,
                self.back_button: self._change_back_state,
            }


    def _check_button(self, button):
        '''Responds to button press and performs an action based on collision type.'''
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            if button is not self.back_button:
                self.sound.play_sfx("options_menu")
            if (button.lmb_pressed and not button.rmb_pressed):
                direction = 1
            elif button.rmb_pressed and not button.lmb_pressed:
                direction = -1
            if direction:
                self.menu_event_dict.get(button)(direction)
            self.enter_pressed = False


    def _update_score_setting(self, direction):
        """Update score and its display text."""
        self._change_game_score(direction)
        self._change_score_text()

    def _change_back_state(self, direction): 
        self.game.state.state = self.game.state.MAINMENU
        self.sound.play_sfx("options_menu")


    def _change_difficulty(self, direction):
        """Helper method that changes the difficulty of the game when a button is clicked."""
        if self.game.settings.speed_counter < len(self.game.settings.GAME_SPEEDS) - 1 and direction > 0:
            self.game.settings.speed_counter += 1
        elif self.game.settings.speed_counter > 0 and direction < 0:
            self.game.settings.speed_counter -= 1
        else:
            if direction > 0:
                self.game.settings.speed_counter = 0
            elif direction < 0:
                self.game.settings.speed_counter = len(self.game.settings.GAME_SPEEDS) - 1
        self.game.settings.speed = self.game.settings.GAME_SPEEDS[self.game.settings.speed_counter]
        self._change_turbo_text()

    def _change_sound_volume(self, direction):
        """Helper method that changes the loudness of the game's sound when button is clicked."""
        if self.game.settings.sound_volume >= 0.9 and direction > 0:
            self.game.settings.sound_volume = 0.0
        elif self.game.settings.sound_volume < 0.9 and direction > 0:
            self.game.settings.sound_volume += 0.1
        elif self.game.settings.sound_volume > 0.1 and direction < 0:
            self.game.settings.sound_volume -= 0.1
        elif self.game.settings.sound_volume <= 0.1 and direction < 0:
            self.game.settings.sound_volume = 1.0
        self._change_sound_text()

    def _change_music_volume(self, direction):
        """Helper method that changes the loudness of the game's music when button is clicked."""
        if self.game.settings.music_volume >= 0.9 and direction > 0:
            self.game.settings.music_volume = 0.0
        elif self.game.settings.music_volume < 0.9 and direction > 0:
            self.game.settings.music_volume += 0.1
        elif self.game.settings.music_volume > 0.1 and direction < 0:
            self.game.settings.music_volume -= 0.1
        elif self.game.settings.music_volume <= 0.1 and direction < 0:
            self.game.settings.music_volume = 1.0
        self._change_music_text()

    def _change_game_resolution(self, direction):
        """Helper method that changes the game's resolution scale when button is clicked."""
        if self.game.settings.gfx_counter < len(self.game.settings.GFX_SETTINGS) - 1 and direction > 0:
            self.game.settings.gfx_counter += 1
        elif self.game.settings.gfx_counter > 0 and direction < 0:
            self.game.settings.gfx_counter -= 1
        else:
            if direction > 0:
                self.game.settings.gfx_counter = 0
            elif direction < 0:
                self.game.settings.gfx_counter = len(self.game.settings.GFX_SETTINGS) - 1
        self.game.settings.gfx_mode = self.game.settings.GFX_SETTINGS[self.game.settings.gfx_counter]
        self._change_gfx_text()
        self._change_window_size()

    def _change_game_HUD(self, direction):
        """Helper method that changes the in-game combat HUD when button is clicked."""
        if self.game.settings.HUD_counter < len(self.game.settings.HUD_SETTINGS) - 1 and direction > 0:
            self.game.settings.HUD_counter += 1
        elif self.game.settings.HUD_counter > 0 and direction < 0:
            self.game.settings.HUD_counter -= 1
        else:
            if direction > 0:
                self.game.settings.HUD_counter = 0
            elif direction < 0:
                self.game.settings.HUD_counter = len(self.game.settings.HUD_SETTINGS) - 1
        self.game.settings.HUD = self.game.settings.HUD_SETTINGS[self.game.settings.HUD_counter]
        self.game.scoreboard.update_prep()
        self._change_HUD_text()

    def _change_game_arrow(self, direction):
        """Helper method that changes the in-game arrow indicators when button is clicked."""
        if self.game.settings.arrow_counter < len(self.game.settings.ARROW_SETTINGS) - 1 and direction > 0:
            self.game.settings.arrow_counter += 1
        elif self.game.settings.arrow_counter > 0 and direction < 0:
            self.game.settings.arrow_counter -= 1
        else:
            if direction > 0:
                self.game.settings.arrow_counter = 0
            elif direction < 0:
                self.game.settings.arrow_counter = len(self.game.settings.ARROW_SETTINGS) - 1
        self.game.settings.arrow_mode = self.game.settings.ARROW_SETTINGS[self.game.settings.arrow_counter]
        self._change_dirarrow_text()

    def _change_game_score(self, direction):
        """Helper method that changes the in-game and menu score displays when button is clicked."""
        if self.game.settings.score_counter < len(self.game.settings.SCORE_SETTINGS) - 1 and direction > 0:
            self.game.settings.score_counter += 1
        elif self.game.settings.score_counter > 0 and direction < 0:
            self.game.settings.score_counter -= 1
        else:
            if direction > 0:
                self.game.settings.score_counter = 0
            elif direction < 0:
                self.game.settings.score_counter = len(self.game.settings.SCORE_SETTINGS) - 1
        self.game.settings.score_mode = self.game.settings.SCORE_SETTINGS[self.game.settings.score_counter]
        self.game.scoreboard.update_prep()
        self._change_HUD_text()

    def _change_music_text(self):
        """Helper method that changes what text is displayed on the music button."""
        self.music_state = f"Music: {self.game.settings.music_volume * 100:.0f}%"

    def _change_score_text(self):
        """Helper method that changes what text is displayed on the score button."""
        self.score_state = self.game.settings.SCORE_SETTINGS[self.game.settings.score_counter]

    def _change_dirarrow_text(self):
        """Helper method that changes what text is displayed on the direction arrow button."""
        self.dirarrow_state = self.game.settings.ARROW_SETTINGS[self.game.settings.arrow_counter]

    def _change_turbo_text(self):
        """Helper method that changes what text is displayed on the turbo button"""
        self.speed_state = self.game.settings.GAME_SPEEDS[self.game.settings.speed_counter]

    def _change_gfx_text(self):
        """Helper method that changes what text is displayed on the resolution button"""
        self.gfx_state = self.game.settings.GFX_SETTINGS[self.game.settings.gfx_counter]

    def _change_sound_text(self):
        """Helper method that changes what text is displayed on the sound button"""
        self.sfx_state = f"Sound: {self.game.settings.sound_volume * 100:.0f}%"

    def _change_HUD_text(self):
        """Helper method that changes what text is displayed on the HUD button"""
        self.HUD_state = self.game.settings.HUD_SETTINGS[self.game.settings.HUD_counter]

    def _change_window_size(self):
        """Changes the size of the game window based on user setting."""
        if self.game.settings.gfx_mode == self.game.settings.GFX_SETTINGS[0]:
            self.screen = pygame.display.set_mode((self.game.settings.screen_width, self.game.settings.screen_height))
        elif self.game.settings.gfx_mode == self.game.settings.GFX_SETTINGS[1]:
            self.screen = pygame.display.set_mode(
                (self.game.settings.screen_width, self.game.settings.screen_height), pygame.SCALED + pygame.RESIZABLE
            )
        elif self.game.settings.gfx_mode == self.game.settings.GFX_SETTINGS[2]:
            self.screen = pygame.display.set_mode(
                (self.game.settings.screen_width, self.game.settings.screen_height),
                pygame.SCALED + pygame.RESIZABLE + pygame.FULLSCREEN,
            )

    def draw_buttons(self):
        """Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0))
        self._highlight_colors()
        self.gfx_button._prep_msg(self.gfx_state)
        self.mute_button._prep_msg(self.music_state)
        self.sfx_button._prep_msg(self.sfx_state)
        self.score_button._prep_msg(self.score_state)
        self.HUD_button._prep_msg(self.HUD_state)
        self.turbo_button._prep_msg(self.speed_state)
        self.dirarrow_button._prep_msg(self.dirarrow_state)
        for button in self.buttons:
            button.draw_button()
        self.screen.blit(self.cursor_image, self.cursor_rect)


    def update_cursor(self, direction):
        """Moves the cursor up or down based on input"""
        if direction >= 0 and self.index > 0:
            self.index -= 1
            self.y -= 75
        elif direction < 0 and self.index < len(self.buttons)-1:
            self.index += 1
            self.y += 75
        self.cursor_rect.y = self.y

import pygame.font, sys, pygame
from button import Button


class Menu:
    """Parent class to hold generic menu functionality and state."""
    def __init__(self, ai_game):
        self.game = ai_game
        self.screen = ai_game.screen
        self.sound = ai_game.sound
        self.index = 0
        self.buttons = []

    def _highlight_colors(self):
        """ Toggles colors for buttons that are being selected."""
        for button in self.buttons:
            button.highlight_color(button.top_rect.collidepoint(pygame.mouse.get_pos()))

    def _toggle_colors(self):
        pass

    def check_menu_buttons(self):
        '''Loops through every button in the menu list and checks over it.'''
        for button in self.buttons:
            self._check_button(button)

    def _check_button(self, button):
        '''To be overriden by child.'''
        pass

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()

class MainMenu(Menu):
    """Class that holds the state and behavior for the main menu screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self._create_main_buttons(ai_game)

    def _create_main_buttons(self, ai_game):
        """Creates the buttons for the main menu."""
        self.play_button = Button(ai_game, "Start", 250, 150)
        self.options_button = Button(ai_game, "Options", 250, 75)
        self.controls_button = Button(self, "Controls", 250, 0)
        self.help_button = Button(ai_game, "Help", 250, -75)
        self.credits_button = Button(ai_game, "Credits", 250, -150)
        self.exit_button = Button(ai_game, "Quit", 250, -225)
        self.buttons = (self.play_button, self.options_button, 
                self.controls_button, self.help_button, self.credits_button,
                self.exit_button)

    def _check_button(self, button):
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.MAINMENU:
            if button.lmb_pressed:
                self.sound.play_sfx("options_menu")
                if button is self.play_button:
                    self.game._clear_state()
                    self.game.state.state = self.game.state.GAMEPLAY
                elif button is self.options_button:
                    self.game.state.state = self.game.state.OPTIONSMENU
                elif button is self.controls_button:
                    self.game.state.state = self.game.state.CONTROLSMENU
                elif button is self.help_button:
                    pass
                elif button is self.credits_button:
                    pass
                elif button is self.exit_button:
                    self.game.stats.dump_stats_json()
                    pygame.quit()
                    sys.exit()

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self.game.scoreboard.prep_high_score_main_menu()
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()

class OptionsMenu(Menu):
    """Class that holds state and behaviour for the options menu."""
    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self._set_initial_text()
        self._create_options_buttons()

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
        self.turbo_button = Button(self, self.speed_state, 0, 250)
        self.mute_button = Button(self, self.music_state, 0, 175)
        self.sfx_button = Button(self, self.sfx_state, 0, 100)
        self.gfx_button = Button(self, self.gfx_state, 0, 25)
        self.score_button = Button(self, self.gfx_state, 0, -50)
        self.HUD_button = Button(self, self.HUD_state, 0, -125)
        self.dirarrow_button = Button(self, self.dirarrow_state, 0, -200)
        self.back_button = Button(self, "Back", 0, -275)
        self.buttons = (self.turbo_button, self.mute_button, self.sfx_button, 
                self.gfx_button, self.score_button, self.HUD_button, self.dirarrow_button, 
                self.back_button)

    def _check_button(self, button):
        '''Responds to button press and performs an action based on collision type.'''
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            if button is not self.back_button:
                self.sound.play_sfx("options_menu")
            if button.lmb_pressed and not button.rmb_pressed:
                direction = 1
            elif button.rmb_pressed and not button.lmb_pressed:
                direction = -1
            if button is self.turbo_button:
                self._change_difficulty(direction)
            elif button is self.sfx_button:
                self._change_sound_volume(direction)
            elif button is self.mute_button:
                self._change_music_volume(direction)
            elif button is self.gfx_button:
                self._change_game_resolution(direction)
            elif button is self.dirarrow_button:
                self._change_game_arrow(direction)
            elif button is self.HUD_button:
                self._change_game_HUD(direction)
            elif button is self.back_button and direction > 0:
                self.game.state.state = self.game.state.MAINMENU
                self.sound.play_sfx("options_menu")
            elif button is self.score_button:
                self._change_game_score(direction)
                self._change_score_text()

    def _change_difficulty(self, direction):
        """Helper method that changes the difficulty of the game when a button is clicked."""
        if self.game.settings.speed_counter < len(self.game.settings.GAME_SPEEDS)-1 and direction > 0:
            self.game.settings.speed_counter += 1
        elif self.game.settings.speed_counter > 0 and direction < 0:
            self.game.settings.speed_counter -= 1
        else: 
            if direction > 0:
                self.game.settings.speed_counter = 0
            elif direction < 0:
                self.game.settings.speed_counter = len(self.game.settings.GAME_SPEEDS)-1
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
        elif self.game.settings.sound_volume < 0.1 and direction < 0:
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
        elif self.game.settings.music_volume < 0.1 and direction < 0:
            self.game.settings.sound_volume = 1.0
        self._change_music_text()

    def _change_game_resolution(self, direction):
        """Helper method that changes the game's resolution scale when button is clicked."""
        if self.game.settings.gfx_counter < len(self.game.settings.GFX_SETTINGS)-1 and direction > 0:
            self.game.settings.gfx_counter += 1 
        elif self.game.settings.gfx_counter > 0 and direction < 0:
            self.game.settings.gfx_counter -= 1
        else: 
            if direction > 0:
                self.game.settings.gfx_counter = 0
            elif direction < 0:
                self.game.settings.gfx_counter = len(self.game.settings.GFX_SETTINGS)-1
        self.game.settings.gfx_mode = self.game.settings.GFX_SETTINGS[self.game.settings.gfx_counter]
        self._change_gfx_text()
        self._change_window_size()

    def _change_game_HUD(self, direction):
        """Helper method that changes the in-game combat HUD when button is clicked."""
        if self.game.settings.HUD_counter < len(self.game.settings.HUD_SETTINGS)-1 and direction > 0:
            self.game.settings.HUD_counter += 1
        elif self.game.settings.HUD_counter > 0 and direction < 0:
            self.game.settings.HUD_counter -= 1
        else: 
            if direction > 0:
                self.game.settings.HUD_counter = 0
            elif direction < 0:
                self.game.settings.HUD_counter = len(self.game.settings.HUD_SETTINGS)-1
        self.game.settings.HUD = self.game.settings.HUD_SETTINGS[self.game.settings.HUD_counter]
        self.game.scoreboard.update_prep()
        self._change_HUD_text()

    def _change_game_arrow(self, direction):
        """Helper method that changes the in-game arrow indicators when button is clicked."""
        if self.game.settings.arrow_counter < len(self.game.settings.ARROW_SETTINGS)-1 and direction > 0:
            self.game.settings.arrow_counter += 1
        elif self.game.settings.arrow_counter > 0 and direction < 0: 
            self.game.settings.arrow_counter -= 1
        else: 
            if direction > 0:
                self.game.settings.arrow_counter = 0
            elif direction < 0:
                self.game.settings.arrow_counter = len(self.game.settings.ARROW_SETTINGS)-1
        self.game.settings.arrow_mode = self.game.settings.ARROW_SETTINGS[self.game.settings.arrow_counter]
        self._change_dirarrow_text()

    def _change_game_score(self, direction):
        """Helper method that changes the in-game and menu score displays when button is clicked."""
        if self.game.settings.score_counter < len(self.game.settings.SCORE_SETTINGS)-1 and direction > 0:
            self.game.settings.score_counter += 1
        elif self.game.settings.score_counter > 0 and direction < 0:
            self.game.settings.score_counter -= 1
        else: 
            if direction > 0:
                self.game.settings.score_counter = 0
            elif direction < 0:
                self.game.settings.score_counter = len(self.game.settings.SCORE_SETTINGS)-1
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
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height))
        elif self.game.settings.gfx_mode == self.game.settings.GFX_SETTINGS[1]:
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height), pygame.SCALED+pygame.RESIZABLE)
        elif self.game.settings.gfx_mode == self.game.settings.GFX_SETTINGS[2]:
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height), 
                    pygame.SCALED+pygame.RESIZABLE+pygame.FULLSCREEN)

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self._highlight_colors()
        self.gfx_button._prep_msg(self.gfx_state)
        self.mute_button._prep_msg(self.music_state)
        self.sfx_button._prep_msg(self.sfx_state)
        self.score_button._prep_msg(self.score_state)
        self.HUD_button._prep_msg(self.HUD_state)
        self.turbo_button._prep_msg(self.speed_state)
        self.dirarrow_button._prep_msg(self.dirarrow_state)
        self._toggle_colors()
        for button in self.buttons:
            button.draw_button()

class ControlsMenu(Menu):
    """Class the holds the state and behavior for the controls menu."""
    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self.screen_rect = self.screen.get_rect()
        self.keybinds = ai_game.keybinds
        self._create_controls_buttons()

    def _create_controls_buttons(self):
        """Creates buttons for the options menu."""
        self.left_button = Button(self, self.keybinds.move_left_text, -250, 280)
        self.right_button = Button(self, self.keybinds.move_right_text, -250, 210)
        self.up_button = Button(self, self.keybinds.move_up_text, -250, 140)
        self.down_button = Button(self, self.keybinds.move_down_text, -250, 70)
        self.beam_button = Button(self, self.keybinds.beam_text, -250, 00)
        self.flip_button = Button(self, self.keybinds.flip_text, -250, -70)
        self.missile_button = Button(self, self.keybinds.shoot_text, -250, -140) 
        self.reset_button = Button(self, "Reset Keys", -250, -210)
        self.back_button = Button(self, "Back", -250, -280)
        self.key_buttons = {self.left_button: "MOVELEFT", self.right_button: "MOVERIGHT",
                self.up_button: "MOVEUP", self.down_button: "MOVEDOWN", self.beam_button: "BEAMATTACK", 
                self.flip_button: "FLIPSHIP", self.missile_button: "MISSILEATTACK"}
        self.buttons = [self.reset_button, self.back_button]

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self._highlight_colors()
        self._toggle_colors()
        self._update_button_text()
        for keybind_button in self.key_buttons:
            keybind_button.draw_button()
        for button in self.buttons:
            button.draw_button()

    def check_controls_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        for keybind_button, mapping in self.key_buttons.items():
            self._check_keybind_button(mouse_pos, keybind_button, mapping) 
        self._check_reset_button()
        self._check_back_button()

    def _highlight_keybind_colors(self):
        """ Toggles colors for buttons that are being selected."""
        for button in self.key_buttons:
            button.highlight_color(button.top_rect.collidepoint(pygame.mouse.get_pos()))

    def _check_keybind_button(self, mouse_pos, button, mapping):
        button_clicked = button.top_rect.collidepoint(mouse_pos)
        done = False
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.sound.play_sfx("options_menu")
            button.set_color((192,81,0), "Press a key or hit ESC", 32)
            button.draw_button()
            pygame.display.update(button.top_rect)
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            done = True
                            pygame.quit()
                            sys.exit()
                        elif (event.key not in self.keybinds.controls.values()
                                and event.key not in self.keybinds.reserved_keys):
                            self.keybinds.controls[mapping] = event.key
                            done = True

    def clear_keybind_button(self, mouse_pos):
        """If right clicking a button, clear the input to free it for reassignment."""
        for button, mapping in self.key_buttons.items():
            if button.top_rect.collidepoint(mouse_pos):
                button_clicked = button.top_rect.collidepoint(mouse_pos)
                key_val = mapping
                break
        button_clicked = button.top_rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.sound.play_sfx("options_menu_unselect")
            self.keybinds.controls[key_val] = pygame.K_UNDERSCORE

    def _update_button_text(self):
        """Updates the keybinding based on the current value."""
        self.keybinds.init_menu_text()
        for button in enumerate(self.key_buttons):
            button[1]._prep_msg(self.keybinds.menu_text[button[0]])

    def _toggle_colors(self):
        """ Toggles colors for buttons that have on/off states."""
        for button, mapping in self.key_buttons.items():
            button.toggle_color(button.top_rect.collidepoint(pygame.mouse.get_pos()), 
                self._check_empty_key(mapping))

    def _check_empty_key(self, mapping):
        """ Checks if a key is empty or not."""
        if self.keybinds.controls.get(mapping) == pygame.K_UNDERSCORE:
            return False
        else: 
            return True

    def _check_back_button(self):
        """Enters the main menu from the options menu screen once clicked."""
        button_clicked = self.back_button.check_mouse_click()
        if (button_clicked and pygame.K_UNDERSCORE not in self.keybinds.controls.values() and
                self.game.state.state is self.game.state.CONTROLSMENU):
            self.game.state.state = self.game.state.MAINMENU
            self.sound.play_sfx("options_menu")

    def _check_reset_button(self):
        """Clears the custom keybinds and resets to initial options."""
        button_clicked = self.reset_button.check_mouse_click()
        if (button_clicked and self.game.state.state is self.game.state.CONTROLSMENU):
            self.keybinds.controls = {"MOVELEFT": pygame.K_a, "MOVERIGHT": pygame.K_d,
                    "MOVEUP": pygame.K_w, "MOVEDOWN": pygame.K_s, "MISSILEATTACK": pygame.K_j, 
                    "BEAMATTACK": pygame.K_l, "FLIPSHIP": pygame.K_k}
            self.sound.play_sfx("options_menu")

class GameOverMenu(Menu):
    """Class that holds the state and behavior for the game over screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self.screen_rect = self.screen.get_rect()
        self.menu_button = Button(self, "Menu", 150, -50)
        self.restart_button = Button(self, "Restart", -150,-50)
        self.buttons = [self.menu_button, self.restart_button]
        self._create_go_menu_properties()
        
    def _create_go_menu_properties(self):
        '''Crates the font and images necessary for the game over screen.'''
        self.game_over_font = pygame.font.Font("assets/fonts/m5x7.ttf", 128)
        self.game_over_image = self.game_over_font.render("GAME OVER", True,
                (255,255,255))
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 100)

    def _check_button(self, button):
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.GAMEOVER:
            if button.lmb_pressed:
                self.sound.play_sfx("game_over")
                if button is self.menu_button:
                    self.game._clear_state()
                    self.game.state.state = self.game.state.MAINMENU
                elif button is self.restart_button:
                    self.game._clear_state()
                    self.game.state.state = self.game.state.GAMEPLAY

    def render_game_over(self):
        """Renders and displays the game over message."""
        self.screen.fill(self.game.settings.bg_color)
        self.screen.blit(self.game_over_image, self.game_over_rect)

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.render_game_over()
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()

class PauseMenu:

    def __init__(self, ai_game):
        """Initialize Pause Menu attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.pause_font = pygame.font.Font("assets/fonts/m5x7.ttf", 128)
        self.pause_image = self.pause_font.render("PAUSED", True,
                (255,255,255))
        self.pause_rect = self.pause_image.get_rect()
        self.pause_rect.center = self.screen_rect.center
        self.state = ai_game.state

    def render_pause(self):
        """Renders and displays the pause message."""
        self.screen.blit(self.pause_image, self.pause_rect)

    def check_pause(self):
        """Checks to see if hitting ESC should pause or unpause the game."""
        self.state.pause_state +=1 
        if self.state.pause_state % 2 == 0 and self.state.state == self.state.PAUSE:
            self.state.state = self.state.GAMEPLAY
        elif self.state.pause_state % 2 and self.state.state == self.state.GAMEPLAY:
            self.state.state = self.state.PAUSE


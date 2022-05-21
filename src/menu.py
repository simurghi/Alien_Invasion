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
        self.exit_button = Button(ai_game, "Quit", 250, -150)
        self.buttons = (self.play_button, self.options_button, 
                self.controls_button, self.help_button, self.exit_button)

    def _check_button(self, button):
        button_clicked = button.check_left_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.MAINMENU:
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
            elif button is self.exit_button:
                self.game.stats.dump_stats_json()
                pygame.quit()
                sys.exit()

class OptionsMenu(Menu):
    """Class that holds state and behaviour for the options menu."""
    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self._set_initial_text()
        self._create_options_buttons()

    def _set_initial_text(self):
        self.speed_state = "SPD: Normal"
        self.gfx_state = "REZ: Scaled"
        self.sfx_state = f"Sound: {self.game.settings.sound_volume * 100:.0f}%"
        self.music_state = f"Music: {self.game.settings.music_volume * 100:.0f}%"
        self.HUD_state = f"HUD: Classic"
        self.score_state = "Score: ON"
        self.dirarrow_state = "Arrows: ON"

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

    def check_options_menu_buttons(self):
        """Check main menu buttons for clicks."""
        self._check_turbo_button()
        self._check_mute_button()
        self._check_sfx_button()
        self._check_gfx_button()
        self._check_score_button()
        self._check_HUD_button()
        self._check_dirarrow_button()
        self._check_back_button()

    def _check_button(self, button):
        '''Responds based on button press:
            Turbo Button - Game Speed / Difficulty
            SFX Button - Game Sound Volume 
            Mute Button - Game Music Volume
            GFX Button - Game Resolution / Window Size
            Dir Arrow - HUD Warning/Direction Arrows
            HUD Button - In-Game HUD presets
            Score Button - In-Game Score Display toggle
            Back Button - Returns to main menu.'''
        button_clicked = button.check_left_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.sound.play_sfx("options_menu")
            if button is self.turbo_button:
                if self.game.settings.speed is self.game.settings.NORMAL_SPEED:
                    self.game.settings.speed = self.game.settings.TURBO_SPEED
                elif self.game.settings.speed is self.game.settings.TURBO_SPEED:
                    self.game.settings.speed = self.game.settings.CHEETAH_SPEED
                elif self.game.settings.speed is self.game.settings.CHEETAH_SPEED:
                    self.game.settings.speed = self.game.settings.LUDICROUS_SPEED
                elif self.game.settings.speed is self.game.settings.LUDICROUS_SPEED:
                    self.game.settings.speed = self.game.settings.EASY_SPEED
                elif self.game.settings.speed is self.game.settings.EASY_SPEED:
                    self.game.settings.speed = self.game.settings.NORMAL_SPEED
                self._change_turbo_text()
            elif button is self.sfx_button:
                if self.game.settings.sound_volume >= 0.9:
                    self.game.settings.sound_volume = 0.0
                elif self.game.settings.sound_volume < 0.9:
                    self.game.settings.sound_volume += 0.1
                self._change_sound_text()
            elif button is self.mute_button:
                if self.game.settings.music_volume >= 0.9:
                    self.game.settings.music_volume = 0.0
                elif self.game.settings.music_volume < 0.9:
                    self.game.settings.music_volume += 0.1
                self._change_music_text()
            elif button is self.gfx_button:
                if self.game.settings.gfx_mode is self.game.settings.NATIVE_GFX:
                    self.game.settings.gfx_mode = self.game.settings.SCALED_GFX
                elif self.game.settings.gfx_mode is self.game.settings.SCALED_GFX:
                    self.game.settings.gfx_mode = self.game.settings.FULLSCREEN_GFX
                elif self.game.settings.gfx_mode is self.game.settings.FULLSCREEN_GFX:
                    self.game.settings.gfx_mode = self.game.settings.NATIVE_GFX
                self._change_gfx_text()
                self._change_window_size()
            elif button is self.dirarrow_button:
                self.game.settings.show_arrow = not self.game.settings.show_arrow
                self._change_dirarrow_text()
            elif button is self.HUD_button:
                if self.game.settings.HUD is self.game.settings.HUD_A:
                    self.game.settings.HUD = self.game.settings.HUD_A_SMOLL
                elif self.game.settings.HUD is self.game.settings.HUD_A_SMOLL:
                    self.game.settings.HUD = self.game.settings.HUD_B
                elif self.game.settings.HUD is self.game.settings.HUD_B:
                    self.game.settings.HUD = self.game.settings.HUD_B_SMOLL
                elif self.game.settings.HUD is self.game.settings.HUD_B_SMOLL:
                    self.game.settings.HUD = self.game.settings.HUD_A
                self.game.scoreboard.update_prep()
                self._change_HUD_text()
            elif button is self.back_button:
                self.game.state.state = self.game.state.MAINMENU
            elif button is self.score_button:
                self.game.settings.show_score = not self.game.settings.show_score
                self._change_score_text()

    def _change_music_text(self):
        """Helper method that changes what text is displayed on the music button."""
        self.music_state = f"Music: {self.game.settings.music_volume * 100:.0f}%"

    def _change_score_text(self):
        """Helper method that changes what text is displayed on the score button."""
        if self.game.settings.show_score:
            self.score_state =  "Score: ON"
        else:
            self.score_state =  "Score: OFF"

    def _change_dirarrow_text(self):
        """Helper method that changes what text is displayed on the direction arrow button."""
        if self.game.settings.show_arrow:
            self.dirarrow_state =  "Arrows: ON"
        else:
            self.dirarrow_state =  "Arrows: OFF"

    def _change_turbo_text(self):
        """Helper method that changes what text is displayed on the turbo button"""
        if self.game.settings.speed is self.game.settings.NORMAL_SPEED:
            self.speed_state = "SPD: Normal"
        elif self.game.settings.speed is self.game.settings.TURBO_SPEED:
            self.speed_state = "SPD: Fast"
        elif self.game.settings.speed is self.game.settings.EASY_SPEED:
            self.speed_state = "SPD: Slow"
        elif self.game.settings.speed is self.game.settings.CHEETAH_SPEED:
            self.speed_state = "SPD: Very Fast"
        elif self.game.settings.speed is self.game.settings.LUDICROUS_SPEED:
            self.speed_state = "SPD: Ludicrous"

    def _change_gfx_text(self):
        """Helper method that changes what text is displayed on the resolution button"""
        if self.game.settings.gfx_mode is self.game.settings.NATIVE_GFX:
            self.gfx_state = "REZ: Native"
        elif self.game.settings.gfx_mode is self.game.settings.SCALED_GFX:
            self.gfx_state = "REZ: Scaled"
        elif self.game.settings.gfx_mode is self.game.settings.FULLSCREEN_GFX:
            self.gfx_state = "REZ: Full Scaled"

    def _change_sound_text(self):
        """Helper method that changes what text is displayed on the sound button"""
        self.sfx_state = f"Sound: {self.game.settings.sound_volume * 100:.0f}%"

    def _change_window_size(self):
        """Changes the size of the game window based on user setting."""
        if self.game.settings.gfx_mode is self.game.settings.SCALED_GFX:
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height), pygame.SCALED+pygame.RESIZABLE)
        elif self.game.settings.gfx_mode is self.game.settings.NATIVE_GFX:
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height))
        elif self.game.settings.gfx_mode is self.game.settings.FULLSCREEN_GFX:
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height), 
                    pygame.SCALED+pygame.RESIZABLE+pygame.FULLSCREEN)

    def _change_HUD_text(self):
        """Helper method that changes what text is displayed on the HUD button"""
        if self.game.settings.HUD is self.game.settings.HUD_A:
            self.HUD_state = "HUD: Classic"
        elif self.game.settings.HUD is self.game.settings.HUD_A_SMOLL:
            self.HUD_state = "HUD: Compact"
        elif self.game.settings.HUD is self.game.settings.HUD_B:
            self.HUD_state = "HUD: Classic-2"
        elif self.game.settings.HUD is self.game.settings.HUD_B_SMOLL:
            self.HUD_state = "HUD: Compact-2"

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
        self._toggle_colors()
        self._update_button_text()
        self._highlight_colors()
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
            button.toggle_color(self._check_empty_key(mapping))

    def _check_empty_key(self, mapping):
        """ Checks if a key is empty or not."""
        if self.keybinds.controls.get(mapping) == pygame.K_UNDERSCORE:
            return False
        else: 
            return True

    def _check_back_button(self):
        """Enters the main menu from the options menu screen once clicked."""
        button_clicked = self.back_button.check_left_mouse_click()
        if (button_clicked and pygame.K_UNDERSCORE not in self.keybinds.controls.values() and
                self.game.state.state is self.game.state.CONTROLSMENU):
            self.game.state.state = self.game.state.MAINMENU
            self.sound.play_sfx("options_menu")

    def _check_reset_button(self):
        """Clears the custom keybinds and resets to initial options."""
        button_clicked = self.reset_button.check_left_mouse_click()
        if (button_clicked and self.game.state.state is self.game.state.CONTROLSMENU):
            self.keybinds.controls = {"MOVELEFT": pygame.K_LEFT, "MOVERIGHT": pygame.K_RIGHT,
                "MOVEUP": pygame.K_UP, "MOVEDOWN": pygame.K_DOWN, "MISSILEATTACK": pygame.K_x, 
                "BEAMATTACK": pygame.K_c, "FLIPSHIP": pygame.K_z}
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
        button_clicked = button.check_left_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.GAMEOVER:
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


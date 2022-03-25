import pygame.font, sys, pygame
from button import Button

class MainMenu:
    """Class that holds the state and behavior for the main menu screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.game = ai_game
        self.screen = ai_game.screen
        self.sound = ai_game.sound
        self._create_main_buttons(ai_game)

    def _create_main_buttons(self, ai_game):
        """Creates the buttons for the main menu."""
        self.play_button = Button(ai_game, "Start", 250, 150)
        self.options_button = Button(ai_game, "Options", 250, 75)
        self.exit_button = Button(ai_game, "Quit", 250, 0)
        self.buttons = [self.play_button,
                self.options_button, self.exit_button]

    def check_main_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        self._check_play_button(mouse_pos)
        self._check_options_button(mouse_pos)
        self._check_exit_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.MAINMENU:
            self.game._clear_state()
            self.game.state.state = self.game.state.GAMEPLAY
            self.sound.play_sfx("options_menu")

    def _check_options_button(self, mouse_pos):
        """Enters the options menu from the main menu screen once clicked."""
        button_clicked = self.options_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.MAINMENU:
            self.game.state.state = self.game.state.OPTIONSMENU
            self.sound.play_sfx("options_menu")

    def _check_exit_button(self, mouse_pos):
        """ Exits the game from the main menu once clicked."""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.MAINMENU:
            self.sound.play_sfx("options_menu")
            self.game.stats.dump_stats_json()
            pygame.quit()
            sys.exit()

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        for button in self.buttons:
            button.draw_button()

class OptionsMenu:
    """Class that holds state and behaviour for the options menu."""
    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.game = ai_game
        self.screen = ai_game.screen
        self.sound = ai_game.sound
        self._set_initial_text()
        self._create_options_buttons()

    def _set_initial_text(self):
        self.speed_state = "Normal Speed"
        self.gfx_state = "Scaled REZ"
        self.FPS_state = "60 FPS"
        self.sfx_state = "Sound ON"
        self.music_state = "Music ON"
        self.vfx_state = "Movie VFX ON"

    def _create_options_buttons(self):
        """Creates buttons for the options menu."""
        self.turbo_button = Button(self, self.speed_state, 0, 250)
        self.controls_button = Button(self, "Keybindings", 0, 175)
        self.mute_button = Button(self, self.music_state, 0, 100)
        self.sfx_button = Button(self, self.sfx_state, 0, 25)
        self.cinematic_button = Button(self, self.vfx_state, 0, -50)
        self.gfx_button = Button(self, self.gfx_state, 0, -125)
        self.fps_button = Button(self, self.FPS_state, 0, -200)
        self.back_button = Button(self, "Back", 0, -275)
        self.buttons = [self.turbo_button, self.controls_button,
                self.mute_button, self.sfx_button, self.cinematic_button,
                self.gfx_button, self.fps_button, self.back_button]

    def check_options_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        self._check_turbo_button(mouse_pos)
        self._check_controls_button(mouse_pos)
        self._check_mute_button(mouse_pos)
        self._check_sfx_button(mouse_pos)
        self._check_cinematic_button(mouse_pos)
        self._check_gfx_button(mouse_pos)
        self._check_fps_button(mouse_pos)
        self._check_back_button(mouse_pos)

    def _change_turbo_text(self):
        """Helper method that changes what text is displayed on the turbo button"""
        if not self.game.settings.turbo_speed:
            self.speed_state = "Normal Speed"
        else:
            self.speed_state = "Turbo Speed"

    def _change_gfx_text(self):
        """Helper method that changes what text is displayed on the resolution button"""
        if not self.game.settings.scaled_gfx:
            self.gfx_state = "Native REZ"
        else:
            self.gfx_state = "Scaled REZ"

    def _change_music_text(self):
        """Helper method that changes what text is displayed on the music button"""
        if not self.game.settings.play_music:
            self.music_state = "Music OFF"
        else:
            self.music_state = "Music ON"

    def _change_sound_text(self):
        """Helper method that changes what text is displayed on the sound button"""
        if not self.game.settings.play_sfx:
            self.sfx_state = "Sound OFF"
        else:
            self.sfx_state = "Sound ON"

    def _change_movie_text(self):
        """Helper method that changes what text is displayed on the VFX button"""
        if not self.game.settings.cinematic_bars:
            self.vfx_state = "Movie VFX OFF"
        else:
            self.vfx_state = "Movie VFX ON"

    def _change_fps(self):
        """Helper method that changes what the game's FPS is"""
        if not self.game.settings.high_FPS:
            self.FPS_state = "60 FPS"
        else:
            self.FPS_state = "120 FPS"

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self.gfx_button._prep_msg(self.gfx_state)
        self.fps_button._prep_msg(self.FPS_state)
        self._toggle_colors()
        for button in self.buttons:
            button.draw_button()

    def _toggle_colors(self):
        """ Toggles colors for buttons that have on/off states."""
        self.mute_button.toggle_color(self.game.settings.play_music, self.music_state)
        self.sfx_button.toggle_color(self.game.settings.play_sfx, self.sfx_state)
        self.cinematic_button.toggle_color(self.game.settings.cinematic_bars, self.vfx_state)
        self.turbo_button.toggle_color(not self.game.settings.turbo_speed, self.speed_state)

    def _check_mute_button(self, mouse_pos):
        """ Toggles music when the player clicks 'Music'"""
        button_clicked = self.mute_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.settings.play_music = not self.game.settings.play_music 
            self._change_music_text()
            self.sound.play_sfx("options_menu")

    def _check_sfx_button(self, mouse_pos):
        """ Toggles sound when the player clicks 'Sound'"""
        button_clicked = self.sfx_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.settings.play_sfx = not self.game.settings.play_sfx 
            self._change_sound_text()
            self.sound.play_sfx("options_menu")

    def _check_cinematic_button(self, mouse_pos):
        """ Toggles "cinematic" black bars when the player clicks 'Movie Mode'"""
        button_clicked = self.cinematic_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.settings.cinematic_bars = not self.game.settings.cinematic_bars
            self._change_movie_text()
            self.sound.play_sfx("options_menu")

    def _check_turbo_button(self, mouse_pos):
        """Increases the game speed by 1.5x if active."""
        button_clicked = self.turbo_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.settings.turbo_speed = not self.game.settings.turbo_speed
            self._change_turbo_text()
            self.sound.play_sfx("options_menu")

    def _check_controls_button(self, mouse_pos):
        """Changes the control scheme based on the current option."""
        button_clicked = self.controls_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.state.state = self.game.state.CONTROLSMENU
            self.sound.play_sfx("options_menu")

    def _check_gfx_button(self, mouse_pos):
        """Changes the window size based on the current option."""
        button_clicked = self.gfx_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.settings.scaled_gfx = not self.game.settings.scaled_gfx
            self._change_gfx_text()
            self._change_window_size()
            self.sound.play_sfx("options_menu")

    def _check_fps_button(self, mouse_pos):
        """Changes the game's framerate based on the current option."""
        button_clicked = self.fps_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.settings.high_FPS = not self.game.settings.high_FPS
            self.game.settings.toggle_fps()
            self._change_fps()
            self.sound.play_sfx("options_menu")

    def _check_back_button(self, mouse_pos):
        """Enters the main menu from the options menu screen once clicked."""
        button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.OPTIONSMENU:
            self.game.state.state = self.game.state.MAINMENU
            self.sound.play_sfx("options_menu")

    def _change_window_size(self):
        """Changes the size of the game window based on user setting."""
        if self.game.settings.scaled_gfx:
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height), pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode(
                    (self.game.settings.screen_width, self.game.settings.screen_height))

class ControlsMenu:
    """Class the holds the state and behavior for the controls menu."""
    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.keybinds = ai_game.keybinds
        self.sound = ai_game.sound
        self.selected = False
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
        self.mouse_button = Button(self, "MOUSE COMBAT", -250, -210)
        self.back_button = Button(self, "Back", -250, -280)
        self.buttons = {self.left_button: "MOVELEFT", self.right_button: "MOVERIGHT",
                self.up_button: "MOVEUP", self.down_button: "MOVEDOWN", self.beam_button: "BEAMATTACK", 
                self.flip_button: "FLIPSHIP", self.missile_button: "MISSILEATTACK"}

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self._toggle_colors()
        self._update_button_text()
        for button in self.buttons:
            button.draw_button()
        self.mouse_button.draw_button()
        self.back_button.draw_button()

    def check_controls_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        for button, mapping in self.buttons.items():
            self._check_keybind_button(mouse_pos, button, mapping) 
        self._check_back_button(mouse_pos)
        self._check_mouse_button(mouse_pos)

    def _check_keybind_button(self, mouse_pos, button, mapping):
        button_clicked = button.rect.collidepoint(mouse_pos)
        done = False
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.sound.play_sfx("options_menu")
            self.selected = True
            button.set_color((192,81,0), "Assign a key or hit ESC", 32)
            button.draw_button()
            pygame.display.update(button.rect)
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        self.selected = False
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True
                            self.selected = False
                        elif event.key == pygame.K_BACKSPACE:
                            done = True
                            self.selected = False
                            pygame.quit()
                            sys.exit()
                        elif event.key not in self.keybinds.controls.values():
                            self.keybinds.controls[mapping] = event.key
                            done = True
                            self.selected = False

    def clear_keybind_button(self, mouse_pos):
        """If right clicking a button, clear the input to free it for reassignment."""
        for button, mapping in self.buttons.items():
            if button.rect.collidepoint(mouse_pos):
                button_clicked = button.rect.collidepoint(mouse_pos)
                key_val = mapping
                break
        button_clicked = button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.sound.play_sfx("options_menu_unselect")
            self.keybinds.controls[key_val] = pygame.K_UNDERSCORE

    def _update_button_text(self):
        """Updates the keybinding based on the current value."""
        self.keybinds.init_menu_text()
        for button in enumerate(self.buttons):
            button[1]._prep_msg(self.keybinds.menu_text[button[0]])

    def _toggle_colors(self):
        """ Toggles colors for buttons that have on/off states."""
        for button, mapping in self.buttons.items():
            button.toggle_color(self._check_empty_key(mapping))
        self.mouse_button.toggle_color(self.game.keybinds.use_mouse)

    def _check_empty_key(self, mapping):
        """ Checks if a key is empty or not."""
        if self.keybinds.controls.get(mapping) == pygame.K_UNDERSCORE:
            return False
        else: 
            return True

    def _check_back_button(self, mouse_pos):
        """Enters the main menu from the options menu screen once clicked."""
        button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if (button_clicked and pygame.K_UNDERSCORE not in self.keybinds.controls.values() and
                self.game.state.state is self.game.state.CONTROLSMENU):
            self.game.state.state = self.game.state.OPTIONSMENU
            self.sound.play_sfx("options_menu")

    def _check_mouse_button(self, mouse_pos):
        """Enters the main menu from the options menu screen once clicked."""
        button_clicked = self.mouse_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.keybinds.use_mouse = not self.keybinds.use_mouse
            self.sound.play_sfx("options_menu")

class GameOverMenu:
    """Class that holds the state and behavior for the game over screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.sound = ai_game.sound
        self.menu_button = Button(self, "Menu", 150, -50)
        self.restart_button = Button(self, "Restart", -150,-50)
        self.game_over_font = pygame.font.Font("assets/fonts/m5x7.ttf", 128)
        self.game_over_image = self.game_over_font.render("GAME OVER", True,
                (255,255,255))
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 100)

    def check_game_over_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        self._check_menu_button(mouse_pos)
        self._check_restart_button(mouse_pos)

    def _check_restart_button(self, mouse_pos):
        """ Enters the game from the game over screen once clicked."""
        button_clicked = self.restart_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.GAMEOVER:
            self.sound.play_sfx("game_over")
            self.game._clear_state()
            self.game.state.state = self.game.state.GAMEPLAY

    def _check_menu_button(self, mouse_pos):
        """Enters the main menu from the game over screen once clicked."""
        button_clicked = self.menu_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.GAMEOVER:
            self.sound.play_sfx("game_over")
            self.game._clear_state()
            self.game.state.state = self.game.state.MAINMENU

    def render_game_over(self):
        """Renders and displays the game over message."""
        self.screen.fill(self.game.settings.bg_color)
        self.screen.blit(self.game_over_image, self.game_over_rect)

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.menu_button.draw_button()
        self.restart_button.draw_button()

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


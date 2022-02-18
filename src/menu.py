import pygame.font, sys, pygame

from button import Button

class MainMenu:
    """Class that holds the state and behavior for the main menu screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.game = ai_game
        self.screen = ai_game.screen
        self.play_button = Button(ai_game, "Start", 100, 150)
        self.options_button = Button(ai_game, "Options", 100, 50)
        self.exit_button = Button(ai_game, "Quit", 100, -50)


    def check_main_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        self._check_play_button(mouse_pos)
        self._check_options_button(mouse_pos)
        self._check_exit_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.MAINMENU:
            self.game._clear_state()
            self.game.stats.state = self.game.stats.GAMEPLAY
            if self.game.settings.play_sfx and self.game.stats.state is not self.game.stats.GAMEOVER:
                self.game.menu_sfx.play()

    def _check_options_button(self, mouse_pos):
        """Enters the options menu from the main menu screen once clicked."""
        button_clicked = self.options_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.MAINMENU:
            self.game.stats.state = self.game.stats.OPTIONSMENU
            if self.game.settings.play_sfx: 
                self.game.menu_sfx.play()
           

    def _check_exit_button(self, mouse_pos):
        """ Exits the game from the main menu once clicked."""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.MAINMENU:
            if self.game.settings.play_sfx and self.game.stats.state is not self.game.stats.GAMEOVER:
                self.game.menu_sfx.play()
            self.game.dump_stats_json()
            pygame.quit()
            sys.exit()


    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self.play_button.draw_button()
        self.options_button.draw_button()
        self.exit_button.draw_button()

class OptionsMenu:
    """Class that holds state and behaviour for the options menu."""
    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.game = ai_game
        self.screen = ai_game.screen
        self.speed_state = "Normal"
        self.control_state =  "ARROWS" 
        self.turbo_button = Button(self, self.speed_state, 100, 250)
        self.controls_button = Button(self, self.control_state, 100, 150)
        self.mute_button = Button(self, "Music", 100, 50)
        self.sfx_button = Button(self, "Sound", 100, -50)
        self.cinematic_button = Button(self, "Movie VFX", 100, -150)
        self.back_button = Button(self, "Back", 100, -250)


    def check_options_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        self._check_turbo_button(mouse_pos)
        self._check_controls_button(mouse_pos)
        self._check_mute_button(mouse_pos)
        self._check_sfx_button(mouse_pos)
        self._check_cinematic_button(mouse_pos)
        self._check_back_button(mouse_pos)

    def _change_turbo_text(self):
        """Helper method that changes what text is displayed on the turbo button"""
        if not self.game.settings.turbo_speed:
            self.speed_state = "Normal"
        else:
            self.speed_state = "Turbo"

    def _change_controls_text(self):
        """Helper method that changes what text is displayed on the control button"""
        if self.game.keybinds.current_scheme is self.game.keybinds.ARROWS:
            self.control_state = "ARROWS" 
        elif self.game.keybinds.current_scheme is self.game.keybinds.WASD:
            self.control_state = "WASD"
        elif self.game.keybinds.current_scheme is self.game.keybinds.ESDF:
            self.control_state = "ESDF"
        elif self.game.keybinds.current_scheme is self.game.keybinds.VIM:
            self.control_state = "VIMLIKE"

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self.mute_button.toggle_color(self.game.settings.play_music)
        self.sfx_button.toggle_color(self.game.settings.play_sfx)
        self.cinematic_button.toggle_color(self.game.settings.cinematic_bars)
        self.turbo_button.toggle_color(not self.game.settings.turbo_speed, self.speed_state)
        self.controls_button._prep_msg(self.control_state)
        self.mute_button.draw_button()
        self.sfx_button.draw_button()
        self.cinematic_button.draw_button()
        self.controls_button.draw_button()
        self.turbo_button.draw_button()
        self.back_button.draw_button()

    def _check_mute_button(self, mouse_pos):
        """ Toggles music when the player clicks 'Music'"""
        button_clicked = self.mute_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.OPTIONSMENU:
            self.game.settings.play_music = not self.game.settings.play_music 
            if self.game.settings.play_sfx and self.game.stats.state is not self.game.stats.GAMEOVER:
                self.game.menu_sfx.play()

    def _check_sfx_button(self, mouse_pos):
        """ Toggles sound when the player clicks 'Sound'"""
        button_clicked = self.sfx_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.OPTIONSMENU:
            self.game.settings.play_sfx = not self.game.settings.play_sfx 
            if self.game.settings.play_sfx and self.game.stats.state is not self.game.stats.GAMEOVER:
                self.game.menu_sfx.play()

    def _check_cinematic_button(self, mouse_pos):
        """ Toggles "cinematic" black bars when the player clicks 'Movie Mode'"""
        button_clicked = self.cinematic_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.OPTIONSMENU:
            self.game.settings.cinematic_bars = not self.game.settings.cinematic_bars
            if self.game.settings.play_sfx and self.game.stats.state is not self.game.stats.GAMEOVER:
                self.game.menu_sfx.play()

    def _check_turbo_button(self, mouse_pos):
        """Increases the game speed by 1.5x if active."""
        button_clicked = self.turbo_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.OPTIONSMENU:
            self.game.settings.turbo_speed = not self.game.settings.turbo_speed
            self._change_turbo_text()
            if self.game.settings.play_sfx and self.game.stats.state is not self.game.stats.GAMEOVER:
                self.game.menu_sfx.play()

    def _check_controls_button(self, mouse_pos):
        """Changes the control scheme based on the current option."""
        button_clicked = self.controls_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.OPTIONSMENU:
            if self.game.keybinds.current_scheme is self.game.keybinds.ARROWS:
                self.game.keybinds.current_scheme = self.game.keybinds.VIM
            elif self.game.keybinds.current_scheme is self.game.keybinds.VIM:
                self.game.keybinds.current_scheme = self.game.keybinds.WASD
            elif self.game.keybinds.current_scheme is self.game.keybinds.WASD:
                self.game.keybinds.current_scheme = self.game.keybinds.ESDF
            elif self.game.keybinds.current_scheme is self.game.keybinds.ESDF:
                self.game.keybinds.current_scheme = self.game.keybinds.ARROWS
            self._change_controls_text()
            self.game.keybinds.set_movement_scheme()
            self.game.keybinds.set_combat_scheme()
            if self.game.settings.play_sfx and self.game.stats.state is not self.game.stats.GAMEOVER:
                self.game.menu_sfx.play()

    def _check_back_button(self, mouse_pos):
        """Enters the main menu from the options menu screen once clicked."""
        button_clicked = self.back_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.OPTIONSMENU:
            self.game.stats.state = self.game.stats.MAINMENU
            if self.game.settings.play_sfx: 
                self.game.menu_sfx.play()

class GameOverMenu:
    """Class that holds the state and behavior for the game over screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        self.game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.menu_button = Button(self, "Menu", 150, -50)
        self.restart_button = Button(self, "Restart", -150,-50)

    def check_game_over_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        self._check_menu_button(mouse_pos)
        self._check_restart_button(mouse_pos)

    def _check_restart_button(self, mouse_pos):
        """ Enters the game from the game over screen once clicked."""
        button_clicked = self.restart_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.GAMEOVER:
            if self.game.settings.play_sfx:
                self.game.menu_sfx.play()
            self.game._clear_state()
            self.game.stats.state = self.game.stats.GAMEPLAY

    def _check_menu_button(self, mouse_pos):
        """Enters the main menu from the game over screen once clicked."""
        button_clicked = self.menu_button.rect.collidepoint(mouse_pos)
        if button_clicked and self.game.stats.state is self.game.stats.GAMEOVER:
            if self.game.settings.play_sfx: 
                self.game.menu_sfx.play()
            self.game._clear_state()
            self.game.stats.state = self.game.stats.MAINMENU

    def render_game_over(self):
        """Renders and displays the game over message."""
        self.screen.fill(self.game.settings.bg_color)
        game_over_font = pygame.font.Font("assets/fonts/m5x7.ttf", 128)
        game_over_image = game_over_font.render("GAME OVER", True,
                (255,255,255))
        # Display the message at the center of the screen.
        game_over_rect = game_over_image.get_rect()
        game_over_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 100)
        self.screen.blit(game_over_image, game_over_rect)


    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.menu_button.draw_button()
        self.restart_button.draw_button()



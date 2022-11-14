import pygame
from button import Button
from menu import Menu


class GameOverMenu(Menu):
    """Class that holds the state and behavior for the game over screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self.screen_rect = self.screen.get_rect()
        self.menu_button = Button(self, "Menu", 150, -50)
        self.restart_button = Button(self, "Restart", -150, -50)
        self.buttons = [self.menu_button, self.restart_button]
        self.menu_event_dict = {self.menu_button: self._check_main_menu_button,
                                self.restart_button: self._check_restart_button}
        self._create_go_menu_properties()
        self._set_cursor()

    def _set_cursor(self):
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_rect.midright = (195, 370)
        self.x = float(self.cursor_rect.x)
        self.y = float(self.cursor_rect.y)

    def _create_go_menu_properties(self):
        """Crates the font and images necessary for the game over screen."""
        self.game_over_font = pygame.font.Font("assets/fonts/m5x7.ttf", 128)
        self.game_over_image = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = (self.screen_rect.centerx, self.screen_rect.centery - 100)

    def _check_button(self, button):
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.GAMEOVER:
            if button.lmb_pressed:
                self.sound.play_sfx("game_over")
                if button is self.menu_button:
                    self._check_main_menu_button()
                elif button is self.restart_button:
                    self._check_restart_button()

    def _check_main_menu_button(self):
        """Helper method that returns to the main menu from the GO screen."""
        self.game._clear_state()
        self.game.state.state = self.game.state.MAINMENU

    def _check_restart_button(self):
        """Help method that restarts the game from GO screen."""
        self.game._clear_state()
        self.game.state.state = self.game.state.GAMEPLAY

    def render_game_over(self):
        """Render and displays the game over message."""
        self.screen.fill(self.game.settings.bg_color)
        self.screen.blit(self.game_over_image, self.game_over_rect)

    def draw_buttons(self):
        """Draws buttons to the screen."""
        self.render_game_over()
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()
        self.screen.blit(self.cursor_image, self.cursor_rect)

    def update_cursor(self, direction):
        """Move the cursor left or right based on input."""
        if direction >= 0 and self.index > 0:
            self.index -= 1
            self.x = 165
        elif direction < 0 and self.index < len(self.buttons) - 1:
            self.index += 1
            self.x = 465
        elif direction >= 0 and self.index == 0:
            self.index = len(self.buttons) - 1
            self.x = 465
        elif direction < 0 and self.index == len(self.buttons) - 1:
            self.index = 0
            self.x = 165
        self.cursor_rect.x = self.x

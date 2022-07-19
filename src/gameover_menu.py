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
        self._create_go_menu_properties()

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
                    self.game._clear_state()
                    self.game.state.state = self.game.state.MAINMENU
                elif button is self.restart_button:
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

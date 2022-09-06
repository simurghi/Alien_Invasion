import pygame.font, sys, pygame
from button import Button

class Menu:
    """Parent class to hold generic menu functionality and state."""

    def __init__(self, ai_game):
        self.game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.sound = ai_game.sound
        self.cursor_image = pygame.image.load('assets/images/menu_arrow.png').convert_alpha()
        self._set_cursor()
        self.index = 0
        self.buttons = []

    def _set_cursor(self):
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_rect.midright = (70, 170)
        self.x = float(self.cursor_rect.x)
        self.y = float(self.cursor_rect.y)

    def _highlight_colors(self):
        """Toggles colors for buttons that are being selected."""
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
        """Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0))
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()
        self.screen.blit(self.cursor_image, self.cursor_rect)

    def update_cursor(self, direction=1):
        """To be overriden by child"""
        if direction >= 0:
            pass
        elif direction < 0:
            pass

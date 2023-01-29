import pygame.font
import sys
import pygame
from button import Button
from menu import Menu


class MainMenu(Menu):
    """Class that holds the state and behavior for the main menu screen."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self.enter_pressed = False
        self.index = 0
        self.font = pygame.font.Font("assets/fonts/m5x7.ttf", 48)
        self._create_main_buttons(ai_game)
        self.prep_name()

    def _create_main_buttons(self, ai_game):
        """Create the buttons for the main menu."""
        self.play_button = Button(ai_game, "Start", 250, 150)
        self.options_button = Button(ai_game, "Options", 250, 75)
        self.controls_button = Button(self, "Controls", 250, 0)
        self.help_button = Button(ai_game, "Help", 250, -75)
        self.credits_button = Button(ai_game, "Credits", 250, -150)
        self.exit_button = Button(ai_game, "Quit", 250, -225)
        self.buttons = (
            self.play_button,
            self.options_button,
            self.controls_button,
            self.help_button,
            self.credits_button,
            self.exit_button,
        )
        self.menu_event_dict = {
            self.play_button: self._play_action,
            self.options_button: self._option_action,
            self.controls_button: self._control_action,
            self.help_button: self._help_action,
            self.credits_button: self._credit_action,
            self.exit_button: self._exit_action,
        }

    def _check_button(self, button):
        """Respond to mouse clicks on buttons."""
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.MAINMENU:
            if button.lmb_pressed or button.enter_pressed:
                self.sound.play_sfx("options_menu")
                self.menu_event_dict.get(button)()
                self.enter_pressed = False

    def _play_action(self):
        self.game._clear_state()
        self.game.state.state = self.game.state.GAMEPLAY

    def _option_action(self):
        self.game.state.state = self.game.state.OPTIONSMENU

    def _control_action(self):
        self.game.state.state = self.game.state.CONTROLSMENU

    def _help_action(self):
        self.game.state.state = self.game.state.HELPMENU

    def _credit_action(self):
        self.game.state.state = self.game.state.CREDITSMENU

    def _exit_action(self):
        self.game.stats.dump_stats_json()
        pygame.quit()
        sys.exit()

    def draw_buttons(self):
        """Draw buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0))
        self.game.scoreboard.prep_high_score_main_menu()
        self.screen.blit(self.name_image, self.name_rect)
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()
        self.screen.blit(self.cursor_image, self.cursor_rect)

    def prep_name(self):
        """Displays the author's name on the bottom right of the main menu."""
        name_str = "a game by Mike Mooc"
        self.name_image = self.font.render(name_str, True, (255,255,255))
        self.name_rect = self.name_image.get_rect()
        self.name_rect.x = self.screen_rect.right / 1.75
        self.name_rect.y = self.screen_rect.bottom - 50

    def update_cursor(self, direction):
        """Move the cursor up or down based on input."""
        if direction >= 0 and self.index > 0:
            self.index -= 1
            self.y -= 75
        elif direction < 0 and self.index < len(self.buttons) - 1:
            self.index += 1
            self.y += 75
        elif direction >= 0 and self.index == 0:
            self.index = len(self.buttons) - 1
            self.y = 530
        elif direction < 0 and self.index == len(self.buttons) - 1:
            self.index = 0
            self.y = 155
        self.cursor_rect.y = self.y

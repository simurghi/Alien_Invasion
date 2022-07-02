from menu import *


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
        self.buttons = (
            self.play_button,
            self.options_button,
            self.controls_button,
            self.help_button,
            self.credits_button,
            self.exit_button,
        )

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
                    self.game.state.state = self.game.state.HELPMENU
                elif button is self.credits_button:
                    self.game.state.state = self.game.state.CREDITSMENU
                elif button is self.exit_button:
                    self.game.stats.dump_stats_json()
                    pygame.quit()
                    sys.exit()

    def draw_buttons(self):
        """Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0))
        self.game.scoreboard.prep_high_score_main_menu()
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()
        self.screen.blit(self.cursor_image, self.cursor_rect)

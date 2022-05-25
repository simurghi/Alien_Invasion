from menu import *

class HelpMenu(Menu):
    """Class to hold helpful tutorial information."""
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self._create_help_buttons(ai_game)

    def _create_help_buttons(self, ai_game):
        """Creates the buttons for the main menu."""
        self.basic_controls_button = Button(ai_game, "Basic Controls", 250, 150)
        self.basic_score_button = Button(ai_game, "Basic Scoring", 250, 75)
        self.basic_enemies_button = Button(ai_game, "Basic Enemies", 250, 0)
        self.adv_enemies_button = Button(ai_game, "ADV Enemies", 250, -75)
        self.adv_score_button = Button(self, "ADV Scoring", 250, -150)
        self.back_button = Button(ai_game, "Back", 250, -225)
        self.buttons = (self.basic_controls_button, self.basic_score_button, 
                self.basic_enemies_button, self.adv_enemies_button, self.adv_score_button,
                self.back_button)

    def _check_button(self, button):
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.HELPMENU:
            if button.lmb_pressed:
                self.sound.play_sfx("options_menu")
                if button is self.back_button:
                    self.game.state.state = self.game.state.MAINMENU
                else:
                    pass

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()


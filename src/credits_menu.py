from button import Button
from menu import Menu


class CreditsMenu(Menu):
    """Class to credit contributors information."""

    def __init__(self, ai_game):
        """Initialize the credits menu."""
        super().__init__(ai_game)
        self._credit_contributors()
        self._create_credits_buttons(ai_game)

    def _credit_contributors(self):
        """Strings to display credits."""
        self.art_credit_text0 = "ART"
        self.art_credit_text1 = "Ansimuz | Matt Walkden | Daniel Linssen"
        self.art_credit_text2 = "GameSupplyGuy | GooseNinja | StudioMeowMeow"
        self.code_credit_text0 = "CODE"
        self.code_credit_text1 = "Eric Matthes | DaFluffyPotato| ScriptLineStudios"
        self.code_credit_text2 = "u/iminurnamez | KidsCanCode | CodeSurgeon | skrx"
        self.code_credit_text3 = "CDCodes | u/metulburr | ClearCode | code.Pylet"

    def _create_credits_buttons(self, ai_game):
        """Create the buttons for the main menu."""
        self.art_button0 = Button(ai_game, self.art_credit_text0, 275, 250, 200, 50, 16)
        self.art_button1 = Button(ai_game, self.art_credit_text1, -25, 175, 800, 50, 16)
        self.art_button2 = Button(ai_game, self.art_credit_text2, -25, 100, 800, 50, 16)
        self.art_button_credits = (self.art_button1, self.art_button2)
        self.code_button0 = Button(ai_game, self.code_credit_text0, 275, 25, 200, 50, 16)
        self.code_button1 = Button(ai_game, self.code_credit_text1, -25, -50, 800, 50, 16)
        self.code_button2 = Button(ai_game, self.code_credit_text2, -25, -125, 800, 50, 16)
        self.code_button3 = Button(ai_game, self.code_credit_text3, -25, -200, 800, 50, 16)
        self.code_button_credits = (self.code_button1, self.code_button2, self.code_button3)
        self.back_button = Button(ai_game, "Back", 250, -275)
        self.buttons = (
            self.art_button0,
            self.art_button1,
            self.art_button2,
            self.code_button0,
            self.code_button1,
            self.code_button2,
            self.code_button3,
            self.back_button,
        )

    def _check_button(self, button):
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.CREDITSMENU:
            if button.lmb_pressed:
                if button is self.back_button:
                    for button in self.buttons:
                        button.display_main = True
                    self.game.state.state = self.game.state.MAINMENU
                    self.sound.play_sfx("options_menu")
                elif button is self.art_button0:
                    self.sound.play_sfx("options_menu")
                    for button in self.art_button_credits:
                        button.display_main = not button.display_main
                elif button is self.code_button0:
                    self.sound.play_sfx("options_menu")
                    for button in self.code_button_credits:
                        button.display_main = not button.display_main
                else:
                    pass

    def draw_buttons(self):
        """Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0))
        self._highlight_colors()
        for button in self.buttons:
            if button.display_main:
                button.draw_button()

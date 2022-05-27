from menu import *

class HelpMenu(Menu):
    """Class to hold helpful tutorial information."""
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self._create_help_buttons(ai_game)
        self._create_help_descriptions()
        self._create_help_windows(ai_game)

    def _create_help_descriptions(self):
        self.basic_control_desc0 = "Move with WASD or Left Analogue Stick/D-PAD on a gamepad"
        self.basic_control_desc1 = "Fire a missile with LMB, J or the A button on a gamepad"
        self.basic_control_desc2 = "Fire a beam with MMB, L, or the X button on a gamepad"
        self.basic_control_desc3 = "Flip the ship with RMB, K, or the B button on a gamepad."
        self.basic_control_desc4 = "Pause the game with ESC or the Start button on a gamepad"
        self.basic_score_desc0 = "Mobs and Mines give 50 and 75 points when killed, respectively."
        self.basic_score_desc1 = "Gunners give 300 points when killed."
        self.basic_score_desc2 = "Killing enemies up close has a 4x score multiplier."
        self.basic_score_desc3 = "Backstabbing enemies has a 4x score multiplier."
        self.basic_score_desc4 = "If both multipliers are on, you get a 10x bonus instead." 

    def _create_help_windows(self, ai_game):
        """Creates the buttons for the main menu."""
        self._create_control_windows(ai_game)
        self._create_score_windows(ai_game)
        self.display_buttons = (self.basic_control_windows, self.basic_score_windows)
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

    def _create_control_windows(self, ai_game):
        self.basic_control_window0 = Button(ai_game, self.basic_control_desc0, -150, 170, 520, 35,
                font_size=32, small_font = True)
        self.basic_control_window1 = Button(ai_game, self.basic_control_desc1, -150, 130, 520, 35,
                font_size=32, small_font = True)
        self.basic_control_window2 = Button(ai_game, self.basic_control_desc2, -150, 90, 520, 35,
                font_size=32, small_font = True)
        self.basic_control_window3 = Button(ai_game, self.basic_control_desc3, -150, 50, 520, 35,
                font_size=32, small_font = True)
        self.basic_control_window4 = Button(ai_game, self.basic_control_desc4, -150, 10, 520, 35,
                font_size=32, small_font = True)
        self.basic_control_windows = (self.basic_control_window0, self.basic_control_window1,
                self.basic_control_window2, self.basic_control_window3, self.basic_control_window4)

    def _create_score_windows(self,ai_game):
        self.basic_score_window0 = Button(ai_game, self.basic_score_desc0, -150, 170, 520, 35,
                font_size=32, small_font = True)
        self.basic_score_window1 = Button(ai_game, self.basic_score_desc1, -150, 130, 520, 35,
                font_size=32, small_font = True)
        self.basic_score_window2 = Button(ai_game, self.basic_score_desc2, -150, 90, 520, 35,
                font_size=32, small_font = True)
        self.basic_score_window3 = Button(ai_game, self.basic_score_desc3, -150, 50, 520, 35,
                font_size=32, small_font = True)
        self.basic_score_window4 = Button(ai_game, self.basic_score_desc4, -150, 10, 520, 35,
                font_size=32, small_font = True)
        self.basic_score_windows = (self.basic_score_window0, self.basic_score_window1,
                self.basic_score_window2, self.basic_score_window3, self.basic_score_window4)

    def _check_button(self, button):
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.HELPMENU:
            if button.lmb_pressed:
                self.sound.play_sfx("options_menu")
                if button is self.basic_controls_button:
                    for button in self.basic_control_windows:
                        button.display = not button.display
                    for button_list in self.display_buttons:
                        if button_list is self.basic_control_windows:
                            pass
                        else:
                            for button in button_list:
                                button.display = False
                elif button is self.basic_score_button:
                    for button in self.basic_score_windows:
                        button.display = not button.display
                    for button_list in self.display_buttons:
                        if button_list is self.basic_score_windows:
                            pass
                        else:
                            for button in button_list:
                                button.display = False
                elif button is self.back_button:
                    for button_list in self.display_buttons:
                            for button in button_list:
                                button.display = False
                    self.game.state.state = self.game.state.MAINMENU

    def _highlight_colors(self):
        """ Toggles colors for buttons that are being selected."""
        for button_list in self.display_buttons:
            for button in button_list:
                if button.display:
                    button.highlight_color(button.top_rect.collidepoint(pygame.mouse.get_pos()), 
                            msg_size=32, small_font = True)
        for button in self.buttons:
            button.highlight_color(button.top_rect.collidepoint(pygame.mouse.get_pos()))

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()
        for button_list in self.display_buttons:
            for button in button_list:
                if button.display:
                    button.draw_button()


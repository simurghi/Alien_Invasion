from menu import *

class HelpMenu(Menu):
    """Class to hold helpful tutorial information."""
    def __init__(self, ai_game):
        super().__init__(ai_game)
        self.game = ai_game
        self._create_help_buttons(ai_game)
        self._create_help_descriptions(ai_game)
        self._create_help_windows(ai_game)

    def _create_help_descriptions(self, ai_game):
        self.basic_control_desc0 = "Move with WASD or Left Analogue Stick/D-PAD on a gamepad"
        self.basic_control_desc1 = "Fire a missile with LMB, J or the A button on a gamepad"
        self.basic_control_desc2 = "Fire a beam with MMB, L, or the X button on a gamepad"
        self.basic_control_desc3 = "Flip the ship with RMB, K, or the B button on a gamepad"
        self.basic_control_desc4 = "Pause the game with ESC or the Start button on a gamepad"
        self.basic_misc_desc0 = "You begin each run with only 3 non-replenishable lives"
        self.basic_misc_desc1 = "You can only have 5 missiles on screen at once"
        self.basic_misc_desc2 = "Missiles immediately regen if they hit an enemy or go offscreen"
        self.basic_misc_desc3 = "You start off with 3 beam charges which are consumable"
        self.basic_misc_desc4 = "Beams are larger than missiles, move faster, and pierce enemies"
        self.basic_misc_desc5 = "You and your missiles move faster while your ship is flipped." 
        self.basic_score_desc0 = "Mobs and Mines give 50 and 75 points when killed, respectively"
        self.basic_score_desc1 = "Gunners give 300 points when killed"
        self.basic_score_desc2 = "Killing enemies up close has a 4x score multiplier"
        self.basic_score_desc3 = "Backstabbing enemies has a 4x score multiplier"
        self.basic_score_desc4 = "If both multipliers are on, you get a 10x bonus instead" 
        self.basic_score_desc5 = "The game becomes harder over time, but you get more score"
        self.basic_score_desc6 = "Every 5000 points earns 1 beam charge or 500 points if full"
        self.basic_enemy_desc0 = "Mobs will spawn from the right of the screen and move left"
        self.basic_enemy_desc1 = "Mines spawn from the non-right edges of the screen and chase you"
        self.basic_enemy_desc2 = "Mines will move and blink faster if near a player and play a sound" 
        self.basic_enemy_desc3 = "Gunners will spawn from the right center and follow your ship's y-pos"
        self.basic_enemy_desc4 = "Gunners will fire a missile at your current y-pos on cooldown" 
        self.basic_enemy_desc5 = "If there are no mobs on the screen, the game will spawn a new wave"
        self.adv_enemy_desc0 = "Mobs and Mines have circular hitboxes, so you can slightly hit them"
        self.adv_enemy_desc1 = "Gunners and their missiles have pixel perfect hitboxes. Watch out!"
        self.adv_enemy_desc2 = "Mobs will spawn and despawn offscreen to give you reaction time"
        self.adv_enemy_desc3 = "Mines will move slower when offscreen and never spawn in the center"
        self.adv_enemy_desc4 = "Mine arrows indicate where they spawn, not their current position"
        self.adv_enemy_desc5 = "Gunners have 10 HP and take 1 DMG from missiles and 5 from beams"
        self.adv_enemy_desc6 = "When under 50% HP, Gunners will move and shoot faster"
        self.adv_enemy_desc7 = "There can only be one Gunner, a new wave will spawn if it is alive"
        self.adv_enemy_desc8 = "Beams will only pierce Gunners on killing blows"

    def _create_help_windows(self, ai_game):
        """Creates the buttons for the main menu."""
        self._create_control_windows(ai_game)
        self._create_misc_windows(ai_game)
        self._create_score_windows(ai_game)
        self._create_enemy_windows(ai_game)
        self._create_adv_enemy_windows(ai_game)
        self.display_buttons = (self.basic_control_windows, self.basic_misc_windows,
                self.basic_score_windows, self.basic_enemy_windows, self.adv_enemy_windows)

    def _create_help_buttons(self, ai_game):
        """Creates the buttons for the main menu."""
        self.basic_controls_button = Button(ai_game, "Basic Controls", 250, 150)
        self.basic_misc_button = Button(ai_game, "Basic Gameplay", 250, 75)
        self.basic_score_button = Button(ai_game, "Basic Scoring", 250, 0)
        self.basic_enemies_button = Button(ai_game, "Basic Enemies", 250, -75)
        self.adv_enemies_button = Button(ai_game, "ADV Enemies", 250, -150)
        self.back_button = Button(ai_game, "Back", 250, -225)
        self.buttons = (self.basic_controls_button, self.basic_score_button, self.basic_misc_button,
                self.basic_enemies_button, self.adv_enemies_button, self.back_button)

    def _create_control_windows(self, ai_game):
        """Creates the tutorial buttons for the game's basic controls. TODO: add fstrings for 
        current key mappings, not just defaults."""
        self.basic_control_window0 = Button(ai_game, self.basic_control_desc0, -175, 240, 580, 35,
                font_size=32, small_font = True)
        self.basic_control_window1 = Button(ai_game, self.basic_control_desc1, -175, 200, 580, 35,
                font_size=32, small_font = True)
        self.basic_control_window2 = Button(ai_game, self.basic_control_desc2, -175, 160, 580, 35,
                font_size=32, small_font = True)
        self.basic_control_window3 = Button(ai_game, self.basic_control_desc3, -175, 120, 580, 35,
                font_size=32, small_font = True)
        self.basic_control_window4 = Button(ai_game, self.basic_control_desc4, -175, 80, 580, 35,
                font_size=32, small_font = True)
        self.basic_control_windows = (self.basic_control_window0, self.basic_control_window1,
                self.basic_control_window2, self.basic_control_window3, self.basic_control_window4)

    def _create_score_windows(self,ai_game):
        """Creates tutorial buttons for the game's basic score tutorial."""
        self.basic_score_window0 = Button(ai_game, self.basic_score_desc0, -175, 200, 580, 35,
                font_size=32, small_font = True)
        self.basic_score_window1 = Button(ai_game, self.basic_score_desc1, -175, 160, 580, 35,
                font_size=32, small_font = True)
        self.basic_score_window2 = Button(ai_game, self.basic_score_desc2, -175, 120, 580, 35,
                font_size=32, small_font = True)
        self.basic_score_window3 = Button(ai_game, self.basic_score_desc3, -175, 80, 580, 35,
                font_size=32, small_font = True)
        self.basic_score_window4 = Button(ai_game, self.basic_score_desc4, -175, 40, 580, 35,
                font_size=32, small_font = True)
        self.basic_score_window5 = Button(ai_game, self.basic_score_desc5, -175, 00, 580, 35,
                font_size=32, small_font = True)
        self.basic_score_window6 = Button(ai_game, self.basic_score_desc6, -175, -40, 580, 35,
                font_size=32, small_font = True)
        self.basic_score_windows = (self.basic_score_window0, self.basic_score_window1,
                self.basic_score_window2, self.basic_score_window3, self.basic_score_window4,
                self.basic_score_window5, self.basic_score_window6)

    def _create_misc_windows(self,ai_game):
        """Creates tutorial buttons for the game's basic mechanics tutorials."""
        self.basic_misc_window0 = Button(ai_game, self.basic_misc_desc0, -175, 220, 580, 35,
                font_size=32, small_font = True)
        self.basic_misc_window1 = Button(ai_game, self.basic_misc_desc1, -175, 180, 580, 35,
                font_size=32, small_font = True)
        self.basic_misc_window2 = Button(ai_game, self.basic_misc_desc2, -175, 140, 580, 35,
                font_size=32, small_font = True)
        self.basic_misc_window3 = Button(ai_game, self.basic_misc_desc3, -175, 100, 580, 35,
                font_size=32, small_font = True)
        self.basic_misc_window4 = Button(ai_game, self.basic_misc_desc4, -175, 60, 580, 35,
                font_size=32, small_font = True)
        self.basic_misc_window5 = Button(ai_game, self.basic_misc_desc5, -175, 20, 580, 35,
                font_size=32, small_font = True)
        self.basic_misc_windows = (self.basic_misc_window0, self.basic_misc_window1,
                self.basic_misc_window2, self.basic_misc_window3, self.basic_misc_window4,
                self.basic_misc_window5)

    def _create_enemy_windows(self,ai_game):
        """Creates basic tutorial buttons for the game's basic enemies tutorial."""
        self.basic_enemy_window0 = Button(ai_game, self.basic_enemy_desc0, -175, 180, 580, 35,
                font_size=32, small_font = True)
        self.basic_enemy_window1 = Button(ai_game, self.basic_enemy_desc1, -175, 140, 580, 35,
                font_size=32, small_font = True)
        self.basic_enemy_window2 = Button(ai_game, self.basic_enemy_desc2, -175, 100, 580, 35,
                font_size=32, small_font = True)
        self.basic_enemy_window3 = Button(ai_game, self.basic_enemy_desc3, -175, 60, 580, 35,
                font_size=32, small_font = True)
        self.basic_enemy_window4 = Button(ai_game, self.basic_enemy_desc4, -175, 20, 580, 35,
                font_size=32, small_font = True)
        self.basic_enemy_window5 = Button(ai_game, self.basic_enemy_desc5, -175, -20, 580, 35,
                font_size=32, small_font = True)
        self.basic_enemy_windows = (self.basic_enemy_window0, self.basic_enemy_window1,
                self.basic_enemy_window2, self.basic_enemy_window3, self.basic_enemy_window4,
                self.basic_enemy_window5) 

    def _create_adv_enemy_windows(self,ai_game):
        """Creates advanced tutorial buttons for the game's advanced enemies tutorial."""
        self.adv_enemy_window0 = Button(ai_game, self.adv_enemy_desc0, -175, 160, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window1 = Button(ai_game, self.adv_enemy_desc1, -175, 120, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window2 = Button(ai_game, self.adv_enemy_desc2, -175, 80, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window3 = Button(ai_game, self.adv_enemy_desc3, -175, 40, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window4 = Button(ai_game, self.adv_enemy_desc4, -175, 0, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window5 = Button(ai_game, self.adv_enemy_desc5, -175, -40, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window6 = Button(ai_game, self.adv_enemy_desc6, -175, -80, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window7 = Button(ai_game, self.adv_enemy_desc7, -175, -120, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_window8 = Button(ai_game, self.adv_enemy_desc8, -175, -160, 580, 35,
                font_size=32, small_font = True)
        self.adv_enemy_windows = (self.adv_enemy_window0, self.adv_enemy_window1,
                self.adv_enemy_window2, self.adv_enemy_window3, self.adv_enemy_window4,
                self.adv_enemy_window5, self.adv_enemy_window6, self.adv_enemy_window7,
                self.adv_enemy_window8)

    def _check_button(self, button):
        """Processes user clicks and displays the appropriate tutorials for the appropriate button"""
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.HELPMENU:
            if button.lmb_pressed:
                self.sound.play_sfx("options_menu")
                if button is self.basic_controls_button:
                    self._check_controls_button()
                elif button is self.basic_misc_button:
                    self._check_misc_button()
                elif button is self.basic_score_button:
                    self._check_score_button()
                elif button is self.basic_enemies_button:
                    self._check_basic_enemies_button()
                elif button is self.adv_enemies_button:
                    self._check_adv_enemies_button()
                elif button is self.back_button:
                    self._check_back_button()

    def _check_controls_button(self):
        """displays only the controls tutorial when clicked."""
        for button in self.basic_control_windows:
            button.display = not button.display
        for button_list in self.display_buttons:
            if button_list is self.basic_control_windows:
                pass
            else:
                for button in button_list:
                    button.display = False

    def _check_misc_button(self):
        """Displays only the basic gameplay tutorial when clicked."""
        for button in self.basic_misc_windows:
            button.display = not button.display
        for button_list in self.display_buttons:
            if button_list is self.basic_misc_windows:
                pass
            else:
                for button in button_list:
                    button.display = False

    def _check_score_button(self):
        """Displays only the basic score tutorial when clicked."""
        for button in self.basic_score_windows:
            button.display = not button.display
        for button_list in self.display_buttons:
            if button_list is self.basic_score_windows:
                pass
            else:
                for button in button_list:
                    button.display = False

    def _check_basic_enemies_button(self):
        """Displays only the basic enemies tutorial when clicked."""
        for button in self.basic_enemy_windows:
            button.display = not button.display
        for button_list in self.display_buttons:
            if button_list is self.basic_enemy_windows:
                pass
            else:
                for button in button_list:
                    button.display = False

    def _check_adv_enemies_button(self):
        """Displays only the advanced enemies tutorial when clicked."""
        for button in self.adv_enemy_windows:
            button.display = not button.display
        for button_list in self.display_buttons:
            if button_list is self.adv_enemy_windows:
                pass
            else:
                for button in button_list:
                    button.display = False

    def _check_back_button(self):
        """Hides all tutorial prompts and returns to the main menu when clicked."""
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
        self.game.keybinds.init_menu_text()
        self._highlight_colors()
        for button in self.buttons:
            button.draw_button()
        for button_list in self.display_buttons:
            for button in button_list:
                if button.display:
                    button.draw_button()


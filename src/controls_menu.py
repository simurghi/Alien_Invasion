from menu import * 

class ControlsMenu(Menu):
    """Class the holds the state and behavior for the controls menu."""
    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self.screen_rect = self.screen.get_rect()
        self.keybinds = ai_game.keybinds
        self._create_controls_buttons()

    def _create_controls_buttons(self):
        """Creates buttons for the options menu."""
        self.left_button = Button(self, self.keybinds.move_left_text, 0, 280)
        self.right_button = Button(self, self.keybinds.move_right_text, 0, 210)
        self.up_button = Button(self, self.keybinds.move_up_text, 0, 140)
        self.down_button = Button(self, self.keybinds.move_down_text, 0, 70)
        self.beam_button = Button(self, self.keybinds.beam_text, 0, 00)
        self.flip_button = Button(self, self.keybinds.flip_text, 0, -70)
        self.missile_button = Button(self, self.keybinds.shoot_text, 0, -140) 
        self.reset_button = Button(self, "Reset Keys", 0, -210)
        self.back_button = Button(self, "Back", 0, -280)
        self.key_buttons = {self.left_button: "MOVELEFT", self.right_button: "MOVERIGHT",
                self.up_button: "MOVEUP", self.down_button: "MOVEDOWN", self.beam_button: "BEAMATTACK", 
                self.flip_button: "FLIPSHIP", self.missile_button: "MISSILEATTACK"}
        self.buttons = [self.reset_button, self.back_button]
        self._append_keybinds_to_buttons()

    def _append_keybinds_to_buttons(self):
        """Appends the keybinds (buttons only) to the buttons list."""
        for key in tuple(self.key_buttons):
            self.buttons.append(key)

    def draw_buttons(self):
        """ Draws buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0)) 
        self._highlight_colors()
        self._toggle_colors()
        self._update_button_text()
        for button in self.buttons:
            button.draw_button()

    def check_controls_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        for keybind_button, mapping in self.key_buttons.items():
            self._check_keybind_button(mouse_pos, keybind_button, mapping) 
        self._check_reset_button()
        self._check_back_button()

    def _highlight_keybind_colors(self):
        """ Toggles colors for buttons that are being selected."""
        for button in self.key_buttons:
            button.highlight_color(button.top_rect.collidepoint(pygame.mouse.get_pos()))

    def _check_keybind_button(self, mouse_pos, button, mapping):
        button_clicked = button.top_rect.collidepoint(mouse_pos)
        done = False
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.sound.play_sfx("options_menu")
            button.set_color((192,81,0), "Press a key or hit ESC", 32)
            button.draw_button()
            pygame.display.update(button.top_rect)
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            done = True
                            pygame.quit()
                            sys.exit()
                        elif (event.key not in self.keybinds.controls.values()
                                and event.key not in self.keybinds.reserved_keys):
                            self.keybinds.controls[mapping] = event.key
                            done = True

    def clear_keybind_button(self, mouse_pos):
        """If right clicking a button, clear the input to free it for reassignment."""
        for button, mapping in self.key_buttons.items():
            if button.top_rect.collidepoint(mouse_pos):
                button_clicked = button.top_rect.collidepoint(mouse_pos)
                key_val = mapping
                break
        button_clicked = button.top_rect.collidepoint(mouse_pos)
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.sound.play_sfx("options_menu_unselect")
            self.keybinds.controls[key_val] = pygame.K_UNDERSCORE

    def _update_button_text(self):
        """Updates the keybinding based on the current value."""
        self.keybinds.init_menu_text()
        for button in enumerate(self.key_buttons):
            button[1]._prep_msg(self.keybinds.menu_text[button[0]])

    def _toggle_colors(self):
        """ Toggles colors for buttons that have on/off states."""
        for button, mapping in self.key_buttons.items():
            button.toggle_color(button.top_rect.collidepoint(pygame.mouse.get_pos()), 
                self._check_empty_key(mapping))

    def _check_empty_key(self, mapping):
        """ Checks if a key is empty or not."""
        if self.keybinds.controls.get(mapping) == pygame.K_UNDERSCORE:
            return False
        else: 
            return True

    def _check_back_button(self):
        """Enters the main menu from the options menu screen once clicked."""
        button_clicked = self.back_button.check_mouse_click()
        if (button_clicked and pygame.K_UNDERSCORE not in self.keybinds.controls.values() and
                self.game.state.state is self.game.state.CONTROLSMENU):
            self.game.state.state = self.game.state.MAINMENU
            self.sound.play_sfx("options_menu")

    def _check_reset_button(self):
        """Clears the custom keybinds and resets to initial options."""
        button_clicked = self.reset_button.check_mouse_click()
        if (button_clicked and self.game.state.state is self.game.state.CONTROLSMENU):
            self.keybinds.controls = {"MOVELEFT": pygame.K_a, "MOVERIGHT": pygame.K_d,
                    "MOVEUP": pygame.K_w, "MOVEDOWN": pygame.K_s, "MISSILEATTACK": pygame.K_j, 
                    "BEAMATTACK": pygame.K_l, "FLIPSHIP": pygame.K_k}
            self.sound.play_sfx("options_menu")


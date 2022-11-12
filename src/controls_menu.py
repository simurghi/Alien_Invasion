import pygame.font
import sys
import pygame
from button import Button
from menu import Menu


class ControlsMenu(Menu):
    """Class the holds the state and behavior for the controls menu."""

    def __init__(self, ai_game):
        """Initialize button attributes."""
        super().__init__(ai_game)
        self.screen_rect = self.screen.get_rect()
        self.keybinds = ai_game.keybinds
        self._create_controls_buttons()
        self.enter_pressed = False
        self._set_cursor()

    def _set_cursor(self):
        self.cursor_rect = self.cursor_image.get_rect()
        self.cursor_rect.midright = (70, 40)
        self.x = float(self.cursor_rect.x)
        self.y = float(self.cursor_rect.y)

    def _create_controls_buttons(self):
        """Create buttons for the options menu."""
        self.left_button = Button(self, self.keybinds.move_left_text, 250, 280)
        self.right_button = Button(self, self.keybinds.move_right_text, 250, 210)
        self.up_button = Button(self, self.keybinds.move_up_text, 250, 140)
        self.down_button = Button(self, self.keybinds.move_down_text, 250, 70)
        self.beam_button = Button(self, self.keybinds.beam_text, 250, 0)
        self.flip_button = Button(self, self.keybinds.flip_text, 250, -70)
        self.missile_button = Button(self, self.keybinds.shoot_text, 250, -140)
        self.reset_button = Button(self, "Reset Keys", 250, -210)
        self.back_button = Button(self, "Back", 250, -280)
        self.key_buttons = {
            self.left_button: self.keybinds.MOVELEFT,
            self.right_button: self.keybinds.MOVERIGHT,
            self.up_button: self.keybinds.MOVEUP,
            self.down_button: self.keybinds.MOVEDOWN,
            self.beam_button: self.keybinds.BEAMATTACK,
            self.flip_button: self.keybinds.FLIPSHIP,
            self.missile_button: self.keybinds.MISSILEATTACK,
        }
        self.buttons = [self.reset_button, self.back_button]
        self._append_keybinds_to_buttons()
        self.menu_event_dict = {
                self.left_button: self._check_keybind_button,
                self.right_button: self._check_keybind_button,
                self.up_button: self._check_keybind_button,
                self.down_button: self._check_keybind_button,
                self.beam_button: self._check_keybind_button,
                self.flip_button: self._check_keybind_button,
                self.missile_button: self._check_keybind_button,
                self.reset_button: self._check_reset_button,
                self.back_button: self._check_back_button,
                }

    def _append_keybinds_to_buttons(self):
        """Append the keybinds (buttons only) to the buttons list."""
        for key in tuple(self.key_buttons):
            self.buttons.append(key)

    def draw_buttons(self):
        """Draw buttons to the screen."""
        self.screen.blit(self.game.menu_image, (0, 0))
        self._highlight_colors()
        self._toggle_colors()
        self._update_button_text()
        for button in self.buttons:
            button.draw_button()
        self.screen.blit(self.cursor_image, self.cursor_rect)

    def _check_button(self, mouse_pos, button):
        """Respond to a button press and performans an action based on collision type."""
        button_clicked = button.check_mouse_click()
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            if button.lmb_pressed or button.enter_pressed:
                self.sound.play_sfx("options_menu")
                if button in self.key_buttons:
                    self.menu_event_dict.get(button)(mouse_pos, button, self.key_buttons.get(button))
                else:
                    self.menu_event_dict.get(button)()
                self.enter_pressed = False

    def check_controls_menu_buttons(self, mouse_pos):
        """Check main menu buttons for clicks."""
        for button in self.buttons: 
            self._check_button(mouse_pos, button)

    def _highlight_keybind_colors(self):
        """Toggle colors for buttons that are being selected."""
        for button in self.key_buttons:
            button.highlight_color(button.top_rect.collidepoint(pygame.mouse.get_pos()))

    def _check_keybind_button(self, mouse_pos, button, mapping):
        """Check button for user input and dynamically reassign the value."""
        button_clicked = button.top_rect.collidepoint(mouse_pos)
        done = False
        if button_clicked and self.game.state.state is self.game.state.CONTROLSMENU:
            self.sound.play_sfx("options_menu")
            button.set_color((192, 81, 0), "Press a key or hit ESC", 32)
            button.draw_button()
            pygame.display.update(button.top_rect)
            while not done:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                            done = True
                        elif event.key == pygame.K_DELETE:
                            done = True
                            pygame.quit()
                            sys.exit()
                        elif (
                                event.key not in self.keybinds.controls.values() and
                                event.key not in self.keybinds.reserved_keys
                             ):
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
        """Update the keybinding based on the current value."""
        self.keybinds.init_menu_text()
        for button in enumerate(self.key_buttons):
            button[1]._prep_msg(self.keybinds.menu_text[button[0]])

    def _toggle_colors(self):
        """Toggle colors for buttons that have on/off states."""
        for button, mapping in self.key_buttons.items():
            button.toggle_color(button.top_rect.collidepoint(pygame.mouse.get_pos()), self._check_empty_key(mapping))

    def _check_empty_key(self, mapping):
        """Check if a key is empty or not."""
        if self.keybinds.controls.get(mapping) == pygame.K_UNDERSCORE:
            return False
        else:
            return True

    def _check_back_button(self):
        """Enter the main menu from the options menu screen once clicked."""
        if ( pygame.K_UNDERSCORE not in self.keybinds.controls.values() and
            self.game.state.state is self.game.state.CONTROLSMENU):
                self.game.state.state = self.game.state.MAINMENU

    def _check_reset_button(self):
        """Clear the custom keybinds and resets to initial options."""
        if self.game.state.state is self.game.state.CONTROLSMENU:
            self.keybinds.controls = {
                self.keybinds.MOVELEFT: pygame.K_a,
                self.keybinds.MOVERIGHT: pygame.K_d,
                self.keybinds.MOVEUP: pygame.K_w,
                self.keybinds.MOVEDOWN: pygame.K_s,
                self.keybinds.MISSILEATTACK: pygame.K_j,
                self.keybinds.BEAMATTACK: pygame.K_l,
                self.keybinds.FLIPSHIP: pygame.K_k,
            }

    def update_cursor(self, direction):
        """Move the cursor up or down based on input."""
        if direction >= 0 and self.index > 0:
            self.index -= 1
            self.y -= 70
        elif direction < 0 and self.index < len(self.buttons) - 1:
            self.index += 1
            self.y += 70
        elif direction >= 0 and self.index == 0:
            self.index = len(self.buttons) - 1
            self.y = 590
        elif direction < 0 and self.index == len(self.buttons) - 1:
            self.index = 0
            self.y = 25
        self.cursor_rect.y = self.y

    def pass_function(self):
        pass

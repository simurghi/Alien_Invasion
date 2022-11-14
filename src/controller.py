import pygame


class Controller:
    """Class to track and manage the gamepad."""

    def __init__(self, ai_game):
        """Initialize basic controller buttons and properties."""
        pygame.joystick.init()
        self._check_gamepad()
        self._set_button_names()
        self._create_objects(ai_game)
        self.analog_motion = [0, 0]

    def _check_gamepad(self):
        """Check if a gamepad is connected and assigns it to the first one if it is."""
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)

    def _set_button_names(self):
        """Create constants to assign to button numbers to correspond to Xbox controller."""
        self.BTN_A = 0
        self.BTN_B = 1
        self.BTN_X = 2
        self.BTN_Y = 3
        self.BTN_LB = 4
        self.BTN_RB = 5
        self.BTN_SELECT = 6
        self.BTN_START = 7

    def _create_objects(self, ai_game):
        """Create objects necessary for the gamepad to work."""
        self.state = ai_game.state
        self.sound = ai_game.sound
        self.game = ai_game
        self.main_menu = self.game.main_menu
        self.options_menu = self.game.options_menu
        self.help_menu = self.game.help_menu
        self.credits_menu = self.game.credits_menu
        self.go_menu = self.game.go_menu
        self.settings = ai_game.settings
        self.options_menu = ai_game.options_menu
        self.ship = ai_game.ship

    def check_joybuttondown_events(self, event):
        """Respond to gamepad face button presses."""
        self._check_combat_controls(event)
        self._check_menu_controls_buttons(event)

    def check_joybuttonup_events(self, event):
        """Respond to gamepad face button releases."""
        self._check_combat_controls(event)

    def _check_combat_controls(self, event):
        """Handle input while in combat."""
        if self.state.state is self.state.GAMEPLAY:
            if event.button == self.BTN_A and event.type == pygame.JOYBUTTONDOWN:
                self.ship.is_firing = True
            if event.button == self.BTN_A and event.type == pygame.JOYBUTTONUP:
                self.ship.is_firing = False
            if event.button == self.BTN_B and event.type == pygame.JOYBUTTONDOWN:
                self.ship.flip_ship()
            if event.button == self.BTN_X and event.type == pygame.JOYBUTTONDOWN:
                self.ship.fire_beam()
        if (
            event.button == self.BTN_START and
            event.type == pygame.JOYBUTTONDOWN and
            (self.state.state is self.state.GAMEPLAY or self.state.state is self.state.PAUSE)
        ):
            self.sound.play_sfx("options_menu")
            self.game.pause.check_pause()

    def _check_menu_controls_buttons(self, event):
        """Handle button input while in any menu."""
        if self.state.state is self.state.MAINMENU:
            if event.button == self.BTN_A:
                if self.main_menu.buttons[self.main_menu.index].msg == "Controls":
                    self.sound.play_sfx("options_menu_denied")
                else:
                    self.sound.play_sfx("options_menu")
                    self.main_menu.enter_pressed = True
                    self.main_menu.menu_event_dict.get(self.main_menu.buttons[self.main_menu.index])()
        elif self.state.state == self.state.OPTIONSMENU:
            if event.button == self.BTN_A:
                self.sound.play_sfx("options_menu")
                self.options_menu.enter_pressed = True
                (self.options_menu.menu_event_dict.get(self.options_menu.buttons[self.options_menu.index])
                 (direction=1))
        elif self.state.state == self.state.HELPMENU:
            if event.button == self.BTN_A:
                self.sound.play_sfx("options_menu")
                self.help_menu.enter_pressed = True
                self.help_menu.menu_event_dict.get(self.help_menu.buttons[self.help_menu.index])()
        elif self.state.state == self.state.CREDITSMENU:
            if event.button == self.BTN_A:
                self.sound.play_sfx("options_menu")
                self.credits_menu.enter_pressed = True
                self.credits_menu.menu_event_dict.get(self.credits_menu.func_buttons[self.credits_menu.index])()
        elif self.state.state == self.state.GAMEOVER:
            if event.button == self.BTN_A:
                self.sound.play_sfx("options_menu")
                self.go_menu.enter_pressed = True
                self.go_menu.menu_event_dict.get(self.go_menu.buttons[self.go_menu.index])()
        if event.button == self.BTN_B and self.state.state is not (self.state.GAMEPLAY or self.state.PAUSE):
            self.game._check_exit()

    def _check_menu_controls_dpad(self, event):
        """Handle DPAD input while in any menu."""
        if self.state.state == self.state.MAINMENU:
            if event.value[1] == 1:
                self.main_menu.update_cursor(direction=1)
            elif event.value[1] == -1:
                self.main_menu.update_cursor(direction=-1)
        elif self.state.state == self.state.OPTIONSMENU:
            if event.value[1] == 1:
                self.options_menu.update_cursor(direction=1)
            elif event.value[1] == -1:
                self.options_menu.update_cursor(direction=-1)
        elif self.state.state == self.state.HELPMENU:
            if event.value[1] == 1:
                self.help_menu.update_cursor(direction=1)
            elif event.value[1] == -1:
                self.help_menu.update_cursor(direction=-1)
        elif self.state.state == self.state.CREDITSMENU:
            if event.value[1] == 1:
                self.credits_menu.update_cursor(direction=1)
            elif event.value[1] == -1:
                self.credits_menu.update_cursor(direction=-1)
        elif self.state.state == self.state.GAMEOVER:
            if event.value[0] == -1:
                self.go_menu.update_cursor(direction=1)
            elif event.value[0] == 1:
                self.go_menu.update_cursor(direction=-1)

    def check_joyaxismotion_events(self, event):
        """Respond to analogue stick input."""
        if event.axis < 2:
            self.analog_motion[event.axis] = event.value
            if abs(self.analog_motion[0]) < 0.1:
                self.analog_motion[0] = 0
            else:
                if self.analog_motion[0] < -0.4:
                    self.ship.moving_left = True
                else:
                    self.ship.moving_left = False
                if self.analog_motion[0] > 0.4:
                    self.ship.moving_right = True
                else:
                    self.ship.moving_right = False
            if abs(self.analog_motion[1]) < 0.1:
                self.analog_motion[1] = 0
            else:
                if self.analog_motion[1] < -0.4:
                    self.ship.moving_up = True
                else:
                    self.ship.moving_up = False
                if self.analog_motion[1] > 0.4:
                    self.ship.moving_down = True
                else:
                    self.ship.moving_down = False

    def check_joyhatmotion_events(self, event):
        """Respond to dpad presses on the gamepad."""
        if self.state.state is self.state.GAMEPLAY:
            if event.value[0] == 1:
                self.ship.moving_right = True
            elif event.value[0] == -1:
                self.ship.moving_left = True
            elif event.value[0] == 0:
                self.ship.moving_left = False
                self.ship.moving_right = False
            if event.value[1] == 1:
                self.ship.moving_up = True
            elif event.value[1] == -1:
                self.ship.moving_down = True
            elif event.value[1] == 0:
                self.ship.moving_up = False
                self.ship.moving_down = False
        else:
            self._check_menu_controls_dpad(event)

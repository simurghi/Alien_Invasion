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
        self.settings = ai_game.settings
        self.options_menu = ai_game.options_menu
        self.ship = ai_game.ship

    def check_joybuttondown_events(self, event):
        """Respond to gamepad face button presses."""
        self._check_combat_controls(event)
        self._check_menu_controls(event)
        self._check_game_over_controls(event)

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

    def _check_menu_controls(self, event):
        """Handle input while in the main menu."""
        if self.state.state is self.state.MAINMENU:
            if event.button == self.BTN_A:
                self.game._clear_state()
                self.sound.play_sfx("options_menu")
                self.state.state = self.state.GAMEPLAY
            elif event.button == self.BTN_B:
                self.sound.play_sfx("options_menu")
                self.game._check_exit()
            elif event.button == self.BTN_X:
                self.sound.play_sfx("options_menu")
                self.state.state = self.state.OPTIONSMENU

    def _check_game_over_controls(self, event):
        """Handle input while in the game over screen."""
        if self.state.state is self.state.GAMEOVER:
            if event.button == self.BTN_B:
                self.game._clear_state()
                self.sound.play_sfx("game_over")
                self.state.state = self.state.MAINMENU
            elif event.button == self.BTN_A:
                self.game._clear_state()
                self.sound.play_sfx("game_over")
                self.state.state = self.state.GAMEPLAY

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

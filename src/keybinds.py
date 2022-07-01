import pygame

class Keybinds:
    """A class to manage keybindings"""
    def __init__(self):
        self._make_control_constants()
        self.controls = {self.MOVELEFT: pygame.K_a, self.MOVERIGHT: pygame.K_d,
                self.MOVEUP: pygame.K_w, self.MOVEDOWN: pygame.K_s, self.MISSILEATTACK: pygame.K_j, 
                self.BEAMATTACK: pygame.K_l, self.FLIPSHIP: pygame.K_k}
        self.reserved_keys = (pygame.K_UNDERSCORE, pygame.K_ESCAPE, 
                pygame.K_BACKSPACE, pygame.K_BACKQUOTE, pygame.K_RETURN)
        self.init_menu_text()

    def init_menu_text(self):
        """Sets the menu text to display in the keybindings menu."""
        self.move_left_text = "LEFT - " + pygame.key.name(self.controls.get(self.MOVELEFT))
        self.move_right_text = "RIGHT - " + pygame.key.name(self.controls.get(self.MOVERIGHT))
        self.move_up_text = "UP - " + pygame.key.name(self.controls.get(self.MOVEUP))
        self.move_down_text = "DOWN - " + pygame.key.name(self.controls.get(self.MOVEDOWN))
        self.move_left_text_smoll = pygame.key.name(self.controls.get(self.MOVELEFT))
        self.move_right_text_smoll = pygame.key.name(self.controls.get(self.MOVERIGHT))
        self.move_up_text_smoll = pygame.key.name(self.controls.get(self.MOVEUP))
        self.move_down_text_smoll = pygame.key.name(self.controls.get(self.MOVEDOWN))
        self.beam_text = "BEAM - " + pygame.key.name(self.controls.get(self.BEAMATTACK))
        self.flip_text = "FLIP - " + pygame.key.name(self.controls.get(self.FLIPSHIP))
        self.shoot_text = "SHOOT - " + pygame.key.name(self.controls.get(self.MISSILEATTACK))
        self.menu_text = [self.move_left_text, self.move_right_text, self.move_up_text,
                self.move_down_text, self.beam_text, self.flip_text, self.shoot_text]

    def _make_control_constants(self):
        """Makes constants for key binding assignments"""
        self.MOVELEFT = "MOVELEFT"
        self.MOVERIGHT = "MOVERIGHT"
        self.MOVEUP = "MOVEUP"
        self.MOVEDOWN = "MOVEDOWN"
        self.MISSILEATTACK = "MISSILEATTACK"
        self.BEAMATTACK = "BEAMATTACK"
        self.FLIPSHIP = "FLIPSHIP"

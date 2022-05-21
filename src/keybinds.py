import pygame

class Keybinds:
    """A class to manage keybindings"""
    def __init__(self):
        self.controls = {"MOVELEFT": pygame.K_a, "MOVERIGHT": pygame.K_d,
                "MOVEUP": pygame.K_w, "MOVEDOWN": pygame.K_s, "MISSILEATTACK": pygame.K_j, 
                "BEAMATTACK": pygame.K_l, "FLIPSHIP": pygame.K_k}
        self.reserved_keys = (pygame.K_UNDERSCORE, pygame.K_ESCAPE, 
                pygame.K_BACKSPACE, pygame.K_BACKQUOTE, pygame.K_RETURN)
        self.init_menu_text()

    def init_menu_text(self):
        """Sets the menu text to display in the keybindings menu."""
        self.move_left_text = f"LEFT - {pygame.key.name(self.controls.get('MOVELEFT'))}"
        self.move_right_text = f"RIGHT - {pygame.key.name(self.controls.get('MOVERIGHT'))}"
        self.move_up_text = f"UP - {pygame.key.name(self.controls.get('MOVEUP'))}"
        self.move_down_text = f"DOWN - {pygame.key.name(self.controls.get('MOVEDOWN'))}"
        self.beam_text = f"BEAM - {pygame.key.name(self.controls.get('BEAMATTACK'))}"
        self.flip_text = f"FLIP - {pygame.key.name(self.controls.get('FLIPSHIP'))}"
        self.shoot_text = f"SHOOT - {pygame.key.name(self.controls.get('MISSILEATTACK'))}"
        self.menu_text = [self.move_left_text, self.move_right_text, self.move_up_text,
                self.move_down_text, self.beam_text, self.flip_text, self.shoot_text]

    



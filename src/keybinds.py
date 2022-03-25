import pygame

class Keybinds:
    """A class to manage keybindings"""
    def __init__(self):
        self.controls = {"MOVELEFT": pygame.K_LEFT, "MOVERIGHT": pygame.K_RIGHT,
                "MOVEUP": pygame.K_UP, "MOVEDOWN": pygame.K_DOWN, "MISSILEATTACK": pygame.K_x, 
                "BEAMATTACK": pygame.K_c, "FLIPSHIP": pygame.K_z}
        self.use_mouse = False
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

    



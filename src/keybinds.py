import pygame

class Keybinds:
    """A class to manage keybindings"""
    def __init__(self):
        self.controls = {"MOVELEFT": pygame.K_LEFT, "MOVERIGHT": pygame.K_RIGHT,
                "MOVEUP": pygame.K_UP, "MOVEDOWN": pygame.K_DOWN, "MISSILEATTACK": pygame.K_x, 
                "BEAMATTACK": pygame.K_c, "FLIPSHIP": pygame.K_z}
        self.use_mouse = False
        self.ARROWS = 1
        self.current_scheme = self.ARROWS
        self.set_movement_scheme()
        self.set_combat_scheme()

    def set_movement_scheme(self):
        """Sets the movment keys based on the current scheme"""
        if self.current_scheme is self.ARROWS:
            self.MOVEUP = pygame.K_UP
            self.MOVEDOWN = pygame.K_DOWN
            self.MOVELEFT = pygame.K_LEFT
            self.MOVERIGHT = pygame.K_RIGHT

    def set_combat_scheme(self):
        if self.current_scheme is self.ARROWS:
            self.MISSILEATTACK = pygame.K_x
            self.BEAMATTACK = pygame.K_c
            self.FLIPSHIP = pygame.K_z
            self.use_mouse = False


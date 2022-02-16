import pygame


class Keybinds:
    """A class to manage keybindings"""
    def __init__(self):
        self.WASD = 1
        self.ARROWS = 2
        self.current_scheme = 2
        self.set_movement_scheme()
        self.set_combat_scheme()

    def set_movement_scheme(self):
        """Sets the movment keys based on the current scheme"""
        if self.current_scheme is self.ARROWS:
            self.MOVEUP = pygame.K_UP
            self.MOVEDOWN = pygame.K_DOWN
            self.MOVELEFT = pygame.K_LEFT
            self.MOVERIGHT = pygame.K_RIGHT
        else:
            self.MOVEUP = pygame.K_w
            self.MOVEDOWN = pygame.K_s
            self.MOVELEFT = pygame.K_a
            self.MOVERIGHT = pygame.K_d


    def set_combat_scheme(self):
        if self.current_scheme is self.ARROWS:
            self.MISSILEATTACK = pygame.K_x
            self.BEAMATTACK = pygame.K_c
            self.FLIPSHIP = pygame.K_z
            self.use_mouse = False
        else:
            self.use_mouse = True

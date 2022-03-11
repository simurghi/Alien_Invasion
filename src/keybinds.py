import pygame

class Keybinds:
    """A class to manage keybindings"""
    def __init__(self):
        self._initialize_control_schemes()
        self.current_scheme = 1
        self.set_movement_scheme()
        self.set_combat_scheme()

    def _initialize_control_schemes(self):
        """Sets the possible control schemes for the game."""
        self.ARROWS = 1
        self.ARROWS2 = 2
        self.VIM = 3
        self.SPACE = 4
        self.SPACE2 = 5
        self.QWOP = 6
        self.WASD = 7
        self.ESDF = 8 

    def set_movement_scheme(self):
        """Sets the movment keys based on the current scheme"""
        if (self.current_scheme is self.ARROWS or self.current_scheme is self.ARROWS2 
                or self.current_scheme is self.SPACE or self.current_scheme is self.SPACE2):
            self.MOVEUP = pygame.K_UP
            self.MOVEDOWN = pygame.K_DOWN
            self.MOVELEFT = pygame.K_LEFT
            self.MOVERIGHT = pygame.K_RIGHT
        elif self.current_scheme is self.ESDF:
            self.MOVEUP = pygame.K_e
            self.MOVEDOWN = pygame.K_d
            self.MOVELEFT = pygame.K_s
            self.MOVERIGHT = pygame.K_f
        elif self.current_scheme is self.WASD:
            self.MOVEUP = pygame.K_w
            self.MOVEDOWN = pygame.K_s
            self.MOVELEFT = pygame.K_a
            self.MOVERIGHT = pygame.K_d
        elif self.current_scheme is self.VIM: 
            self.MOVEUP = pygame.K_l
            self.MOVEDOWN = pygame.K_k
            self.MOVELEFT = pygame.K_j
            self.MOVERIGHT = pygame.K_SEMICOLON
        elif self.current_scheme is self.QWOP: 
            self.MOVEUP = pygame.K_o
            self.MOVEDOWN = pygame.K_p
            self.MOVELEFT = pygame.K_q
            self.MOVERIGHT = pygame.K_w

    def set_combat_scheme(self):
        if self.current_scheme is self.ARROWS:
            self.MISSILEATTACK = pygame.K_x
            self.BEAMATTACK = pygame.K_c
            self.FLIPSHIP = pygame.K_z
            self.use_mouse = False
        elif self.current_scheme is self.ARROWS2:
            self.MISSILEATTACK = pygame.K_s
            self.BEAMATTACK = pygame.K_d
            self.FLIPSHIP = pygame.K_a
            self.use_mouse = False
        elif self.current_scheme is self.SPACE:
            self.MISSILEATTACK = pygame.K_SPACE
            self.BEAMATTACK = pygame.K_LCTRL 
            self.FLIPSHIP = pygame.K_LSHIFT
            self.use_mouse = False
        elif self.current_scheme is self.SPACE2:
            self.MISSILEATTACK = pygame.K_SPACE
            self.BEAMATTACK = pygame.K_LSHIFT
            self.FLIPSHIP = pygame.K_x
            self.use_mouse = False
        elif (self.current_scheme is self.ESDF 
                or self.current_scheme is self.WASD):
            self.use_mouse = True
        elif self.current_scheme is self.VIM:
            self.MISSILEATTACK = pygame.K_d
            self.BEAMATTACK = pygame.K_f
            self.FLIPSHIP = pygame.K_s
            self.use_mouse = False
        elif self.current_scheme is self.QWOP:
            self.MISSILEATTACK = pygame.K_SPACE
            self.BEAMATTACK = pygame.K_k
            self.FLIPSHIP = pygame.K_f
            self.use_mouse = False

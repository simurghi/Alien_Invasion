import pygame.font 

class Button:

    def __init__(self, ai_game, msg, x_offset = 0, y_offset = 0, width = 250, height = 50):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self._set_button_properties(width, height)
        self.msg = msg
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.centerx - x_offset, self.screen_rect.centery - y_offset
        self._prep_msg(msg)

    def _set_button_properties(self, width, height):
        """Sets the size, color, and font of the button."""
        self.width, self.height = width, height
        self.button_color = (34, 139, 34)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('assets/fonts/m5x7.ttf', 48)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, 
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """ Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def toggle_color(self, color_switch, msg='', msg_size=48):
        """Receives a boolean and adjusts the color of the button based on the values."""
        if color_switch:
            self.button_color = (34, 139, 34)
            self.font = pygame.font.Font('assets/fonts/m5x7.ttf', msg_size)
            if msg =='':
                self._prep_msg(self.msg)
            else:
                self._prep_msg(msg)
        elif not color_switch:
            self.button_color = (178, 34, 34)
            self.font = pygame.font.Font('assets/fonts/m5x7.ttf', msg_size)
            if msg =='':
                self._prep_msg(self.msg)
            else:
                self._prep_msg(msg)

    def set_color(self, button_color, msg='', msg_size=48):
        """Receives a color value and adjusts the color of the button based on the values."""
        self.button_color = button_color
        self.font = pygame.font.Font('assets/fonts/m5x7.ttf', msg_size)
        if msg =='':
            self._prep_msg(self.msg)
        else:
            self._prep_msg(msg)


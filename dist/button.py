import pygame.font 

class Button:

    def __init__(self, ai_game, msg, x_offset = 0, y_offset = 0):
        """Initialize button attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = 200, 50
        self.button_color = (34, 139, 34)
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font('fonts/m5x7.ttf', 48)
        self.msg = msg


        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.center = self.screen_rect.centerx - x_offset, self.screen_rect.centery - y_offset

        self._prep_msg(msg)

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

    def toggle_color(self, color_switch):
        """Receives a boolean and adjusts the color of the button based on the values."""
        if color_switch:
            self.button_color = (34, 139, 34)
            self._prep_msg(self.msg)
        elif not color_switch:
            self.button_color = (178, 34, 34)
            self._prep_msg(self.msg)




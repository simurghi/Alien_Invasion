from menu import *

class PauseMenu:

    def __init__(self, ai_game):
        """Initialize Pause Menu attributes."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.pause_font = pygame.font.Font("assets/fonts/m5x7.ttf", 128)
        self.pause_image = self.pause_font.render("PAUSED", True,
                (255,255,255))
        self.pause_rect = self.pause_image.get_rect()
        self.pause_rect.center = self.screen_rect.center
        self.state = ai_game.state

    def render_pause(self):
        """Renders and displays the pause message."""
        self.screen.blit(self.pause_image, self.pause_rect)

    def check_pause(self):
        """Checks to see if hitting ESC should pause or unpause the game."""
        self.state.pause_state +=1 
        if self.state.pause_state % 2 == 0 and self.state.state == self.state.PAUSE:
            self.state.state = self.state.GAMEPLAY
        elif self.state.pause_state % 2 and self.state.state == self.state.GAMEPLAY:
            self.state.state = self.state.PAUSE


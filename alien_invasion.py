import sys, pygame 

from settings import Settings
from ship import Ship 
from bullet import Bullet 

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self): 
        """Initialize the game and create game resources."""
        pygame.init()
        
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.background_image = pygame.image.load("images/parallax_scrolling_background.png").convert()
        self.background_x = 0
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        

    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

       
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event) 
                
    def _update_bullets(self):
        """Update position of the bullets and get rid of the old bullets."""
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width: 
                self.bullets.remove(bullet)


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        self._scroll_background()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        pygame.display.flip()

    
    def _scroll_background(self):
        """Smoothly scrolls the background image on the screen to give illusion of movement."""
        self.rel_background_x = self.background_x % self.background_image.get_rect().width
        self.screen.blit(self.background_image, (
            self.rel_background_x - self.background_image.get_rect().width, 0))
        if self.rel_background_x < self.settings.screen_width:
            self.screen.blit(self.background_image, (self.rel_background_x, 0))
        self.background_x -=0.75


    def _check_keydown_events(self, event):
        """Respond to keypresses.""" 
        if event.key == pygame.K_UP:
            self.ship.moving_up = True 
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True 
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE: 
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed: 
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


if __name__ == '__main__':
    # make a game instance and run the game. 
    ai = AlienInvasion()
    ai.run_game()

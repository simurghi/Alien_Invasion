import pygame 
from pygame.sprite import Sprite
from bullet import Bullet
from beam import Beam

class Ship(Sprite):
    """A class to manage the ship."""

    def __init__(self, ai_game):
        """Initialize the ship and set its starting position."""
        super().__init__()
        self._create_objects(ai_game)
        self.rect = self.image.get_rect()
        self.rect.midleft = self.screen_rect.midleft
        self.radius = 10
        self.fire_delay = 150
        self.last_shot = pygame.time.get_ticks()
        self.is_firing = False
        self.is_flipped = False
        self.y = float(self.rect.y) 
        self.x = float(self.rect.x) 
        self._create_movement_flags()

    def _create_objects(self, ai_game):
        """Creates the objects necessary for the ship class to work."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.state = ai_game.state
        self.stats = ai_game.stats
        self.game = ai_game
        self.sound = ai_game.sound
        self.image = pygame.image.load('assets/images/ship.bmp')


    def _create_movement_flags(self):
        """Creates the movement flags for the ship for smooth movement."""
        self.moving_up = False
        self.moving_down = False 
        self.moving_left = False
        self.moving_right = False 

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect) 

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_up and self.rect.top > 60: 
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom - 60:
            self.y += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed 
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.is_firing:
            self._fire_bullet()
        self.rect.y = self.y 
        self.rect.x = self.x 

    def position_ship(self):
        """Position the ship on the midleft portion of the screen."""
        self.rect.midleft = self.screen_rect.midleft
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)

    def flip_ship(self):
        """Flips the ship and firing pattens of the bullet."""
        if self.state.state == self.state.GAMEPLAY:
            self._rotate_ship()
            self._adjust_bullet_flipped()
            self.sound.play_sfx("flip")

    def _rotate_ship(self):
        """Flips the ship across the y-axis."""
        self.image = pygame.transform.flip(self.image, True, False)
        self.is_flipped = not self.is_flipped

    def _adjust_bullet_flipped(self):
        """Adjusts the speed and direction of flipped bullets."""
        if self.is_flipped:
            self.settings.bullet_speed *= 2.00
            self.settings.ship_speed *= 1.25
        else: 
            self.settings.bullet_speed *= 0.50
            self.settings.ship_speed *= 0.80

    def reset_ship_flip(self):
        """Resets the orientation of the ship on each new game."""
        self.image = pygame.image.load('assets/images/ship.bmp')
        self.is_flipped = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if self.state.state == self.state.GAMEPLAY:
            now = pygame.time.get_ticks()
            if (len(self.game.bullets) < self.settings.bullets_allowed and
                    now - self.last_shot > self.fire_delay): 
                self.last_shot = now
                new_bullet = Bullet(self.game, self)
                if self.is_flipped:
                    new_bullet.rotate_bullet()
                self.game.bullets.add(new_bullet)
                self.sound.play_sfx("bullet")

    def fire_beam(self):
        """Create a new beam and add it to the bullets group."""
        if self.state.state == self.state.GAMEPLAY:
            if len(self.game.beams) < self.stats.charges_remaining: 
                new_beam = Beam(self.game, self)
                if self.is_flipped:
                    new_beam.rotate_beam()
                self.game.beams.add(new_beam)
                self.stats.charges_remaining -= 1
                self.game.scoreboard.prep_beams()
                self.sound.play_sfx("beam")



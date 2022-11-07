import pygame.font
from pygame.sprite import Group
from ship import Ship
from beam import Beam
from bullet import Bullet


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("assets/fonts/m5x7.ttf", 48)
        self._initialize_prep()

    def _initialize_prep(self):
        """Prepare the initial score images."""
        self.prep_high_score()
        self.prep_score()
        self.prep_ships()
        self.prep_beams()
        self.prep_missiles()

    def create_countdown(self, text, x_offset=0, y_offset=0):
        """Create countdown text for the game."""
        self.countdown_image = self.font.render(text, True, self.text_color)
        self.screen.blit(
            self.countdown_image, (self.screen_rect.centerx + x_offset, self.screen_rect.centery + y_offset)
        )

    def update_prep(self):
        """Update the HUD element positions."""
        self._prep_high_score_position()
        self._prep_score_position()
        self.prep_ships()
        self.prep_beams()
        self.prep_missiles()

    def prep_score(self):
        """Turn the score into a rendered image at the top right of the screen."""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color)
        self._prep_score_position()

    def _prep_score_position(self):
        """Get the rect and positions of the score."""
        self.score_rect = self.score_image.get_rect()
        if self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[0]:
            self.score_rect.x, y = self.high_score_rect.left - self.high_score_rect.left / 6, self.screen_rect.top
        elif self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[1]:
            self.score_rect.x, self.score_rect.y = (
                self.high_score_rect.left - self.high_score_rect.left / 6,
                self.high_score_rect.y,
            )
        else:
            self.score_rect.x, y = self.high_score_rect.left - self.high_score_rect.left / 6, self.screen_rect.top

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        self.high_score_image = self.font.render(str(self.stats.high_score), True, self.text_color)
        self._prep_high_score_position()

    def _prep_high_score_position(self):
        self.high_score_rect = self.high_score_image.get_rect()
        if self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[0]:
            self.high_score_rect.topright = self.screen_rect.topright
        elif self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[1]:
            self.high_score_rect.bottomright = self.screen_rect.bottomright
        else:
            self.high_score_rect.topright = self.screen_rect.topright

    def show_score(self):
        """Draw score and lives to the screen."""
        if (
            self.ai_game.settings.score_mode == self.ai_game.settings.SCORE_SETTINGS[0]
            or self.ai_game.settings.score_mode == self.ai_game.settings.SCORE_SETTINGS[1]
        ):
            self.screen.blit(self.score_image, self.score_rect)
            self.screen.blit(self.high_score_image, self.high_score_rect)
        if self.ai_game.settings.HUD != self.ai_game.settings.HUD_SETTINGS[2]:
            self.ships.draw(self.screen)
            self.beams.draw(self.screen)
            self.bullets.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_ships(self):
        """Show how many lives the player has left."""
        self.ships = Group()
        for life in range(self.stats.ships_remaining):
            ship = Ship(self.ai_game)
            if self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[0]:
                ship.rect.x = 10 + life * ship.rect.width
                ship.rect.y = 10
            elif self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[1]:
                ship.rect.x = 10 + life * ship.rect.width
                ship.rect.y = self.screen_rect.bottom - ship.rect.height - 10
            else:
                ship.rect.x = 10 + life * ship.rect.width
                ship.rect.y = self.screen_rect.bottom - ship.rect.height - 10
            self.ships.add(ship)

    def prep_beams(self):
        """Show how many beams the player has left."""
        self.beams = Group()
        for charge in range(self.stats.charges_remaining):
            beam = Beam(self.ai_game, self.ai_game.ship)
            if self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[0]:
                beam.rect.x = (320) - charge * beam.rect.width
                beam.rect.y = 10
            elif self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[1]:
                beam.rect.x = (320) - charge * beam.rect.width
                beam.rect.y = self.screen_rect.bottom - 10 - beam.rect.height
            else:
                beam.rect.x = (320) - charge * beam.rect.width
                beam.rect.y = self.screen_rect.bottom - 10 - beam.rect.height
            self.beams.add(beam)

    def prep_missiles(self):
        """Show how many missiles the player has left."""
        self.bullets = Group()
        for missile in range(self.ai_game.settings.bullets_allowed - len(self.ai_game.bullets)):
            bullet = Bullet(self.ai_game, self.ai_game.ship, hud_scale=True)
            if self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[0]:
                bullet.rect.x = 180 - missile * bullet.rect.width
                bullet.rect.y = 15
            elif self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[1]:
                bullet.rect.x = 180 - missile * bullet.rect.width
                bullet.rect.y = self.screen_rect.bottom - 15 - bullet.rect.height
            else:
                bullet.rect.x = 180 - missile * bullet.rect.width
                bullet.rect.y = self.screen_rect.bottom - 15 - bullet.rect.height
            self.bullets.add(bullet)

    def prep_high_score_main_menu(self):
        """For the game over screen, turn the high score into a rendered image."""
        end_font = pygame.font.Font("assets/fonts/m5x7.ttf", 48)
        max_score = str(self.stats.high_score)
        self.high_score_image_mm = end_font.render(f"HIGH SCORE: {max_score}", True, self.text_color)
        self.high_score_rect_mm = self.high_score_image_mm.get_rect()
        self.high_score_rect_mm.x = self.screen_rect.centerx / 6
        self.high_score_rect_mm.y = self.screen_rect.bottom - 50

    def prep_high_score_game_over(self):
        """For the game over screen, turn the high score into a rendered image."""
        end_font = pygame.font.Font("assets/fonts/m5x7.ttf", 64)
        max_score = str(self.stats.high_score)
        self.high_score_image_go = end_font.render(f"BEST: {max_score}", True, self.text_color)
        self.high_score_rect_go = self.high_score_image_go.get_rect()
        self.high_score_rect_go.centerx = self.screen_rect.centerx
        self.high_score_rect_go.bottom = self.screen_rect.bottom - 50

    def prep_score_game_over(self):
        """For the game over screen, turn the current run's score into a rendered image."""
        end_font = pygame.font.Font("assets/fonts/m5x7.ttf", 64)
        max_score = str(self.stats.score)
        self.score_image_go = end_font.render(f"CURRENT: {max_score}", True, self.text_color)
        self.score_rect_go = self.score_image_go.get_rect()
        self.score_rect_go.centerx = self.screen_rect.centerx
        self.score_rect_go.bottom = self.screen_rect.bottom - 100

    def show_scores_go(self):
        """Draw current and high scores on the screen in a game over."""
        self.screen.blit(self.score_image_go, self.score_rect_go)
        self.screen.blit(self.high_score_image_go, self.high_score_rect_go)

    def show_scores_mm(self):
        """Draws high score on the screen in the main menu."""
        if (
            self.ai_game.settings.score_mode == self.ai_game.settings.SCORE_SETTINGS[0]
            or self.ai_game.settings.score_mode == self.ai_game.settings.SCORE_SETTINGS[2]
        ):
            self.screen.blit(self.high_score_image_mm, self.high_score_rect_mm)

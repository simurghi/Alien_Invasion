import pygame.font

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        self.text_color = (255, 255, 255)
        self.font = pygame.font.Font("assets/fonts/m5x7.ttf", 48)
        self.ship_image = ai_game.ship.image
        self.beam_image = pygame.image.load("assets/images/bolt1.png").convert_alpha()
        self.bullet_image = pygame.image.load("assets/images/missile_hud.bmp").convert_alpha()
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
            self.countdown_image,
            (self.screen_rect.centerx + x_offset, self.screen_rect.centery + y_offset),
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
            self.score_rect.x, self.score_rect.y = (
                self.high_score_rect.left - self.high_score_rect.left / 6,
                self.screen_rect.top,
            )
        elif self.ai_game.settings.HUD == self.ai_game.settings.HUD_SETTINGS[1]:
            self.score_rect.x, self.score_rect.y = (
                self.high_score_rect.left - self.high_score_rect.left / 6,
                self.high_score_rect.y,
            )
        else:
            self.score_rect.x, self.score_rect.y = (
                self.high_score_rect.left - self.high_score_rect.left / 6,
                self.screen_rect.top,
            )

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
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)

        # ships
        for x, y in self.ship_icons:
            self.screen.blit(self.ship_image, (x, y))

        # beams
        for x, y in self.beam_icons:
            self.screen.blit(self.beam_image, (x, y))

        # bullets
        for x, y in self.bullet_icons:
            self.screen.blit(self.bullet_image, (x, y))

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_ships(self):
        """Show how many lives the player has left."""
        self.ship_icons = []
        for i in range(self.stats.ships_remaining):
            x = 10 + i * self.ship_image.get_width()

            if self.settings.HUD == self.settings.HUD_SETTINGS[0]:
                y = 10
            else:
                y = self.screen_rect.bottom - 40

            self.ship_icons.append((x, y))

    def prep_beams(self):
        """Show how many beams the player has left."""
        self.beam_icons = []
        for i in range(self.stats.charges_remaining):
            x = 300 - i * self.beam_image.get_width()

            if self.settings.HUD == self.settings.HUD_SETTINGS[0]:
                y = 10
            else:
                y = self.screen_rect.bottom - 40

            self.beam_icons.append((x, y))

    def prep_missiles(self):
        """Show how many missiles the player has left."""
        self.bullet_icons = []

        remaining = self.settings.bullets_allowed - len(self.ai_game.bullets)

        for i in range(remaining):
            x = 174 - i * self.bullet_image.get_width()

            if self.settings.HUD == self.settings.HUD_SETTINGS[0]:
                y = 10
            else:
                y = self.screen_rect.bottom - 40

            self.bullet_icons.append((x, y))

    def prep_high_score_main_menu(self):
        """For the game over screen, turn the high score into a rendered image."""
        end_font = pygame.font.Font("assets/fonts/m5x7.ttf", 48)
        max_score = str(self.stats.high_score)
        self.high_score_image_mm = end_font.render(
            f"HIGH SCORE: {max_score}", True, self.text_color
        )
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

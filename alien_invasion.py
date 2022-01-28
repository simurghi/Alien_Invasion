import sys, pygame

from time import sleep
from settings import Settings
from ship import Ship 
from bullet import Bullet 
from alien import Alien
from button import Button
from game_stats import GameStats

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self): 
        """Initialize the game and create game resources."""
        pygame.init()
        pygame.joystick.init()
        pygame.display.set_caption("Alien Invasion")
        self._check_gamepad()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
        self.menu_image = pygame.image.load("images/background.png").convert()
        self.background_image = pygame.image.load("images/parallax_scrolling_background.png").convert()
        self.background_x = 0
        self.clock = pygame.time.Clock()
        self.difficulty_timer = 0
        self.difficulty_increase = 60000
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.combat_music = False
        self.menu_music = False
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "Start", 100, 50)
        self.mute_button = Button(self, "Music", 100, -50)
        self.exit_button = Button(self, "Quit", 100, -150)

    
    def _check_gamepad(self):
        """Checks if a gamepad is connected and assigns it to the first one if it is."""
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)
        else: 
            print("No gamepad detected.")

    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            self._check_events()
            self._play_menu_music()
            if self.stats.game_active: 
                delta_time = self.clock.tick()
                self._play_combat_music()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._adjust_difficulty(delta_time)
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses, gamepad actions, and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event) 
            elif event.type == pygame.JOYBUTTONDOWN:
                self._check_joybuttondown_events(event)
            elif event.type == pygame.JOYHATMOTION:
                self._check_joyhatmotion_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_mute_button(mouse_pos)
                self._check_exit_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._clear_state()
            self.stats.game_active = True

    def _check_mute_button(self, mouse_pos):
        """ Toggles music when the player clicks 'Toggle Music'"""
        button_clicked = self.mute_button.rect.collidepoint(mouse_pos)
        if button_clicked: 
            self.settings.play_music = not self.settings.play_music 

    def _check_exit_button(self, mouse_pos):
        """ Exits the game from the main menu once clicked."""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked: 
            sys.exit()


    def _clear_state(self):
        """ Resets the stats for the game on play/restart."""
        self.stats.reset_stats()
        self.aliens.empty()
        self.bullets.empty()
        pygame.mouse.set_visible(False)
        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.position_ship()

    def _play_menu_music(self):
        if not self.menu_music and not self.combat_music and self.settings.play_music:
            pygame.mixer.music.load("audio/menu.wav")
            pygame.mixer.music.play(-1)
            self.menu_music = True
        elif not self.settings.play_music:
            pygame.mixer.music.stop()
            self.menu_music = False
        else: 
            pass

    def _play_combat_music(self):
        """If the game is running, plays battle music."""
        if not self.combat_music and self.settings.play_music:
            pygame.mixer.music.load("audio/battle.wav")
            pygame.mixer.music.play(-1)
            self.combat_music = True
            self.menu_music = False
        elif not self.settings.play_music:
            pygame.mixer.music.stop()
            self.combat_music = False
        else:
            pass


    def _update_bullets(self):
        """Update position of the bullets and get rid of the old bullets."""
        # Update bullet positions
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width: 
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        #Remove and bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Destroy existing bullets and make a new fleet. 
            self.bullets.empty()
            self._create_fleet()



    def _update_aliens(self):
        self._check_alien_collision()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        for alien in self.aliens.copy():
            if alien.rect.left < -70: 
                self.aliens.remove(alien)
        


    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #self.screen.fill(self.settings.bg_color)
        self._scroll_background()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Draw the start button if the game is inactive.
        if not self.stats.game_active:
            self.screen.blit(self.menu_image, (0, 0)) 
            self.play_button.draw_button()
            self.mute_button.toggle_color(self.settings.play_music)
            self.mute_button.draw_button()
            self.exit_button.draw_button()
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
        """respond to keypresses.""" 
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
        """respond to key releases."""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

    def _check_joybuttondown_events(self, event):
        """respond to gamepad face button presses.""" 
        # 0 Corresponds to the "A" Button on an Xbox Controller
        if event.button == 0: 
            self._fire_bullet()
        # 6 Corresponds to the 'Back/Select" Button on an Xbox Controller
        elif event.button == 6: 
            sys.exit()
        # 4 Corresponds to the "LB" Button (Left Bumper) on an Xbox Controller 
        elif event.button == 4 and not self.stats.game_active: 
            self.settings.play_music = not self.settings.play_music 
        # 7 Corresponds to the "Start" Button on an Xbox Controller 
        elif event.button == 7 and not self.stats.game_active: 
            self._clear_state()
            self.stats.game_active = True

    def _check_joyhatmotion_events(self, event):
        """respond to dpad presses on the gamepad.""" 
        if event.value[0] == 1:
            self.ship.moving_right = True
        elif event.value[0] == -1:
            self.ship.moving_left = True
        elif event.value[0] == 0:
            self.ship.moving_left = False
            self.ship.moving_right = False
        if event.value[1] == 1:
            self.ship.moving_up = True
        elif event.value[1] == -1:
            self.ship.moving_down = True
        elif event.value[1] == 0:
            self.ship.moving_up = False
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed: 
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Make an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien height
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.settings.screen_height - (1.50 * alien_height)
        number_aliens_y = int(available_space_y // (1.50 * alien_height))

        # Determine the number of columns of aliens that fit on the screen.
        ship_width = self.ship.rect.width
        available_space_x = (self.settings.screen_height - 
                (3 * alien_width) - ship_width)
        number_cols = available_space_x // (2 * alien_width)

        # Create the first column of aliens.
        for col_number in range(number_cols):
            for alien_number in range(number_aliens_y):
                self._create_alien(alien_number, col_number)

    def _create_alien(self, alien_number, col_number):
        """Create an alien and place it in a column."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.y = alien_height + (1.5 * alien_height * alien_number) + alien.random_y
        alien.rect.y = alien.y
        alien.rect.x = (self.settings.screen_width / 2) + alien_width + 2 * alien.rect.width * col_number
        self.aliens.add(alien)


    def _check_alien_collision(self):
        """Checks to see if alien sprites are overlapping."""
        for alien in self.aliens:
            for other_alien in self.aliens:
                if pygame.sprite.collide_rect(other_alien, alien) and other_alien != alien:
                    other_alien.is_colliding = True
                else:
                    other_alien.is_colliding = False


    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement lives
        if self.stats.ships_remaining > 0:
            self.stats.ships_remaining -= 1

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and reposition the ship.
            self._create_fleet()
            self.ship.position_ship()

            # Pause.
            sleep(0.25)
        else: 
            self.stats.game_active = False
            pygame.mixer.music.fadeout(500)
            self.combat_music = False
            pygame.mouse.set_visible(True)



    def _adjust_difficulty(self, delta_time):
        """Gradually increases the game speed as time elapses."""
        self.difficulty_timer += delta_time
        if self.difficulty_timer > self.difficulty_increase:
            self.settings.increase_speed()
            self.difficulty_timer -= self.difficulty_increase
            print(f"""Difficulty increased! 
            Ship speed: {self.settings.ship_speed} 
            Bullet Speed: {self.settings.bullet_speed} 
            Alien Speed: {self.settings.alien_speed}
            """)

if __name__ == '__main__':
    # make a game instance and run the game. 
    ai = AlienInvasion()
    ai.run_game()

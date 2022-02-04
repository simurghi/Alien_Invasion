import sys, pygame, math, time, json

from settings import Settings
from ship import Ship 
from bullet import Bullet 
from alien import Alien
from button import Button
from aspect_ratio import AspectRatio
from game_stats import GameStats
from scoreboard import Scoreboard 
from explosion import Explosion

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
        self.FPS = 60
        self.time = time.time()
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.combat_music = False
        self.menu_music = False
        self.bullet_sfx = pygame.mixer.Sound("audio/MissileFire.wav")
        self.bullet_sfx.set_volume(0.40)
        self.explosion_sfx = pygame.mixer.Sound("audio/DestroyMonster2.wav")
        self.explosion_sfx.set_volume(0.40)
        self.menu_sfx = pygame.mixer.Sound("audio/OptionSelect.wav")
        self.menu_sfx.set_volume(0.40)
        self.flip_sfx = pygame.mixer.Sound("audio/UnitFlip.wav")
        self.flip_sfx.set_volume(0.25)
        self.bullets = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.bullet_direction = 1
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.difficulty_counter = 0
        self.speed_state = "Normal"
        self.play_button = Button(self, "Start", 100, 250)
        self.turbo_button = Button(self, self.speed_state, 100, 150)
        self.mute_button = Button(self, "Music", 100, 50)
        self.sfx_button = Button(self, "Sound", 100, -50)
        self.cinematic_button = Button(self, "Movie FX", 100, -150)
        self.exit_button = Button(self, "Quit", 100, -250)
        self.top_bar = AspectRatio(self)
        self.bot_bar = AspectRatio(self, self.settings.screen_height - 50)
        self.scoreboard = Scoreboard(self)

    def _check_gamepad(self):
        """Checks if a gamepad is connected and assigns it to the first one if it is."""
        if pygame.joystick.get_count() > 0:
            self.gamepad = pygame.joystick.Joystick(0)

    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            self._check_events()
            self._play_menu_music()
            if self.stats.game_active: 
                self._play_combat_music()
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self.explosions.update()
                self._adjust_difficulty()
            self._update_screen()
            self._adjust_fps_cap()

    def _check_events(self):
        """Respond to keypresses, gamepad actions, and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.dump_stats_json()
                pygame.quit()
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
                self._check_turbo_button(mouse_pos)
                self._check_mute_button(mouse_pos)
                self._check_sfx_button(mouse_pos)
                self._check_cinematic_button(mouse_pos)
                self._check_exit_button(mouse_pos)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        #self.screen.fill(self.settings.bg_color)
        self._scroll_background()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.explosions.draw(self.screen)
        self.aliens.draw(self.screen)
        self._make_game_cinematic()
        self.scoreboard.show_score()
        # Draw the start button if the game is inactive.
        if not self.stats.game_active:
            self.screen.blit(self.menu_image, (0, 0)) 
            self.play_button.draw_button()
            self.mute_button.toggle_color(self.settings.play_music)
            self.sfx_button.toggle_color(self.settings.play_sfx)
            self.cinematic_button.toggle_color(self.settings.cinematic_bars)
            self.turbo_button.toggle_color(not self.settings.turbo_speed, self.speed_state)
            self.mute_button.draw_button()
            self.sfx_button.draw_button()
            self.cinematic_button.draw_button()
            self.turbo_button.draw_button()
            self.exit_button.draw_button()
        pygame.display.flip()

    def _adjust_fps_cap(self):
        """Sets the internal FPS cap for the game."""
        #Current time after all other events in the while loop have elapsed.
        current_time = time.time() 
        #How long our frame took to process, substracting from the init 
        time_diff = current_time - self.time 
        # delay the game based on the target FPS if we finish early, otherwise don't delay
        delay = max(1.0/self.FPS - time_diff, 0)
        time.sleep(delay)
        self.time = current_time

    def _check_play_button(self, mouse_pos):
        """ Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._clear_state()
            self.stats.game_active = True
            if self.settings.play_sfx:
                self.menu_sfx.play()


    def _check_mute_button(self, mouse_pos):
        """ Toggles music when the player clicks 'Music'"""
        button_clicked = self.mute_button.rect.collidepoint(mouse_pos)
        if button_clicked: 
            self.settings.play_music = not self.settings.play_music 
            if self.settings.play_sfx:
                self.menu_sfx.play()


    def _check_sfx_button(self, mouse_pos):
        """ Toggles sound when the player clicks 'Sound'"""
        button_clicked = self.sfx_button.rect.collidepoint(mouse_pos)
        if button_clicked: 
            self.settings.play_sfx = not self.settings.play_sfx 
            if self.settings.play_sfx:
                self.menu_sfx.play()


    def _check_cinematic_button(self, mouse_pos):
        """ Toggles "cinematic" black bars when the player clicks 'Movie Mode'"""
        button_clicked = self.cinematic_button.rect.collidepoint(mouse_pos)
        if button_clicked: 
            self.settings.cinematic_bars = not self.settings.cinematic_bars
            if self.settings.play_sfx:
                self.menu_sfx.play()


    def _check_exit_button(self, mouse_pos):
        """ Exits the game from the main menu once clicked."""
        button_clicked = self.exit_button.rect.collidepoint(mouse_pos)
        if button_clicked: 
            if self.settings.play_sfx:
                self.menu_sfx.play()
            self.dump_stats_json()
            pygame.quit()
            sys.exit()


    def _check_turbo_button(self, mouse_pos):
        """Increases the game speed by 1.5x if active."""
        button_clicked = self.turbo_button.rect.collidepoint(mouse_pos)
        if button_clicked: 
            self.settings.turbo_speed = not self.settings.turbo_speed
            self._change_turbo_text()
            if self.settings.play_sfx:
                self.menu_sfx.play()

    def _change_turbo_text(self):
        """Helper method that changes what text is displayed on the turbo button"""
        if not self.settings.turbo_speed:
            self.speed_state = "Normal"
        else:
            self.speed_state = "Turbo"


    def _clear_state(self):
        """ Resets the stats for the game on play/restart."""
        self.scoreboard.prep_score()
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.scoreboard.prep_ships()
        self.explosions.empty()
        self.aliens.empty()
        self.bullets.empty()
        pygame.mouse.set_visible(False)
        # Create a new fleet and center the ship
        self._create_fleet()
        self.ship.position_ship()

    def _play_menu_music(self):
        """Plays menu music if not in game."""
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
            if bullet.rect.right > self.settings.screen_width or bullet.rect.right < 0: 
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        #Remove and bullets and aliens that have collided.
        collisions = pygame.sprite.groupcollide(self.aliens,
                self.bullets, False, True)
        if collisions:
            for alien in collisions:
                cqc_mult = self._check_cqc_distance(alien)
                self.stats.score += self.settings.alien_points * cqc_mult
                explosion = Explosion(alien.rect.center)
                self.explosions.add(explosion)
                if self.settings.play_sfx and self.stats.game_active:
                    self.explosion_sfx.play()
                alien.kill()


            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()
        if not self.aliens:
            # Destroy existing bullets and make a new fleet. 
            self.bullets.empty()
            self.explosions.empty()
            self._create_fleet()

    def _check_cqc_distance(self, alien):
        """Checks to see if the distance between the ship and alien is eligible for a score bonus."""
        if math.sqrt((self.ship.rect.x - alien.rect.x)**2 + 
                (self.ship.rect.x - alien.rect.x)**2) < 101:
            return 2
        else:
            return 1

    def _update_aliens(self):
        """Checks if any bullets are colliding with aliens, 
        then deletes aliens if they go offscreen.""" 
        self.aliens.update()
        if pygame.sprite.spritecollide(self.ship, self.aliens, False, pygame.sprite.collide_circle):
            self._ship_hit()
        for alien in self.aliens.copy():
            if alien.rect.left < -100: 
                self.aliens.remove(alien)
        

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
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = True 
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = True
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = True 
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_SPACE or event.key == pygame.K_x:
            self._fire_bullet()
        elif (event.key == pygame.K_z or event.key == pygame.K_LSHIFT) and self.stats.game_active:
            self._flip_ship()
        elif event.key == pygame.K_ESCAPE: 
            self.dump_stats_json()
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event):
        """respond to key releases."""
        if event.key == pygame.K_UP or event.key == pygame.K_w:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
            self.ship.moving_down = False
        if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            self.ship.moving_left = False
        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            self.ship.moving_right = False

    def _check_joybuttondown_events(self, event):
        """respond to gamepad face button presses.""" 
        # 0 Corresponds to the "A" Button on an Xbox Controller
        if event.button == 0: 
            self._fire_bullet()
        # 1 Corresponds to the "B" Button on an Xbox Controller
        if event.button == 1: 
            self._flip_ship()
        # 2 Corresponds to the "Y" Button on an Xbox Controller
        elif event.button == 2:
            self.settings.turbo_speed = not self.settings.turbo_speed
            self._change_turbo_text()
            if self.settings.play_sfx:
                self.menu_sfx.play()
        # 3 Corresponds to the "Y" Button on an Xbox Controller
        elif event.button == 3:
            self.settings.cinematic_bars = not self.settings.cinematic_bars
            if self.settings.play_sfx:
                self.menu_sfx.play()
        # 6 Corresponds to the 'Back/Select" Button on an Xbox Controller
        elif event.button == 6: 
            if self.settings.play_sfx:
                self.menu_sfx.play()
            self.dump_stats_json()
            pygame.quit()
            sys.exit()
        # 4 Corresponds to the "LB" Button (Left Bumper) on an Xbox Controller 
        elif event.button == 4 and not self.stats.game_active: 
            self.settings.play_music = not self.settings.play_music 
            if self.settings.play_sfx:
                self.menu_sfx.play()
        # 4 Corresponds to the "LB" Button (Left Bumper) on an Xbox Controller 
        elif event.button == 5 and not self.stats.game_active: 
            self.settings.play_sfx = not self.settings.play_sfx
            if self.settings.play_sfx:
                self.menu_sfx.play()
        # 7 Corresponds to the "Start" Button on an Xbox Controller 
        elif event.button == 7 and not self.stats.game_active: 
            self._clear_state()
            if self.settings.play_sfx:
                self.menu_sfx.play()
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
            if self.settings.play_sfx and self.stats.game_active:
                self.bullet_sfx.play()

    def _flip_ship(self):
        """Flips the ship and firing pattens of the bullet."""
        self.ship.rotate_ship()
        self._adjust_bullet_flipped()
        if self.settings.play_sfx and self.stats.game_active:
            self.flip_sfx.play()

    def _adjust_bullet_flipped(self):
        """Adjusts the speed and direction of flipped bullets."""
        if self.ship.is_flipped:
            self.settings.bullet_speed *= 2.50
        else: 
            self.settings.bullet_speed *= 0.4
        self.bullet_direction *= -1

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
        alien.rect.y = alien_height + (1.65 * alien_height * alien_number) +  alien.random_y
        #alien.rect.y = alien.y
        alien.rect.x = (self.settings.screen_width ) + alien_width + (2 * alien_width * col_number)
        self.aliens.add(alien)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        # Decrement lives
        if self.stats.ships_remaining > 0:
            self.stats.ships_remaining -= 1
            self.scoreboard.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Play an explosion at the ship's position
            explosion = Explosion(self.ship.rect.center)
            self.explosions.add(explosion)
            if self.settings.play_sfx and self.stats.game_active:
                self.explosion_sfx.play()


            # Create a new fleet and reposition the ship.
            self._create_fleet()
            self.ship.position_ship()

            # Pause.
            time.sleep(0.10)

        else: 
            self.stats.game_active = False
            pygame.mixer.music.fadeout(500)
            self.combat_music = False
            pygame.mouse.set_visible(True)

    def _adjust_difficulty(self):
        """Gradually increases the game speed as time elapses."""
        self.difficulty_counter+=1 
        if self.difficulty_counter % 5400 == 0:
            self.settings.increase_speed()
            print("difficulty up!")

    def _make_game_cinematic(self):
        """Draws cinematic black bars around the top and bottom of the screen, forcing a 16:9 aspect ratio."""
        if self.settings.cinematic_bars:
            self.top_bar.draw_bar()
            self.bot_bar.draw_bar()

    def dump_stats_json(self):
        """Dumps score and key game settings to a JSON file."""
        with open("stats/score.json", 'w') as f:
            json.dump({"high score" : self.stats.high_score}, f)

if __name__ == '__main__':
    # make a game instance and run the game. 
    ai = AlienInvasion()
    ai.run_game()

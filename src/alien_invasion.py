import pygame, sys, time

from alien import Alien
from aspect_ratio import AspectRatio
from beam import Beam
from bullet import Bullet 
from controller import Controller
from explosion import Explosion
from game_stats import GameStats
from gunner import Gunner
from keybinds import Keybinds
from math import sqrt
from mine import Mine
from menu import MainMenu, OptionsMenu, GameOverMenu, PauseMenu
from music import Music
from random import randint
from scoreboard import Scoreboard 
from ship import Ship 
from settings import Settings
from sound import Sound
from states import GameState

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self): 
        """Initialize the game and create game resources."""
        pygame.init()
        pygame.display.set_caption("Alien Invasion")
        self._make_game_objects()
        self._load_images()
        self._create_sprite_groups()
        self._create_fleet()

    def _load_images(self):
        """Loads menu and game background images."""
        self.menu_image = pygame.image.load("assets/images/background.png").convert()
        self.background_image = pygame.image.load("assets/images/parallax_scrolling_background.png").convert()

    def _make_game_objects(self):
        """Creates all of the necessary game objects for the game to run."""
        self.settings = Settings()
        self._set_screen_attributes()
        self.time_game = time.time()
        self.keybinds = Keybinds()
        self.state = GameState()
        self.ship = Ship(self)
        self.music = Music(self)
        self.sound = Sound(self)
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.go_menu = GameOverMenu(self)
        self.pause = PauseMenu(self)
        self.controller = Controller(self)
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)
        self.top_bar = AspectRatio(self)
        self.bot_bar = AspectRatio(self, self.settings.screen_height - 50)

    def _set_screen_attributes(self):
        """Sets the screen's dimensions and creates its rect."""
        self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height), pygame.SCALED)
        self.screen_rect = self.screen.get_rect()

    def _create_sprite_groups(self):
        """Creates sprite group containers for objects."""
        self.bullets = pygame.sprite.Group()
        self.beams = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.mines = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.gunners = pygame.sprite.GroupSingle()

    def run_game(self):
        """Start the main loop for the game."""
        while True: 
            self._check_events()
            self._check_mouse_visible()
            self.music.play_music()
            if self.state.state is self.state.GAMEPLAY: 
                self.ship.update()
                self._update_bullets()
                self._update_beams()
                self._update_aliens()
                self.explosions.update()
                self._adjust_difficulty()
            self._update_screen()
            self._adjust_fps_cap()

    def _check_events(self):
        """Respond to keypresses, gamepad actions, and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.dump_stats_json()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event) 
            elif event.type == pygame.JOYBUTTONDOWN:
                self.controller.check_joybuttondown_events(event)
            elif event.type == pygame.JOYHATMOTION:
                self.controller.check_joyhatmotion_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.options_menu.check_options_menu_buttons(mouse_pos)
                self.main_menu.check_main_menu_buttons(mouse_pos)
                self.go_menu.check_game_over_buttons(mouse_pos)
                self._check_mousedown_events()

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        if self.state.state is self.state.GAMEPLAY:
            self._scroll_background()
            self.ship.blitme()
            self.bullets.draw(self.screen)
            self.beams.draw(self.screen)
            self.aliens.draw(self.screen)
            self.mines.draw(self.screen)
            self.gunners.draw(self.screen)
            if self.gunners and self.gunners.sprite.gunner_bullets:
                self.gunners.sprite.gunner_bullets.draw(self.screen)
            self.explosions.draw(self.screen)
            self._make_game_cinematic()
            self.scoreboard.show_score()
        elif self.state.state is self.state.PAUSE:
            self.pause.render_pause()
        elif self.state.state is self.state.GAMEOVER:
            self.go_menu.render_game_over()
            self.go_menu.draw_buttons()
            self.scoreboard.show_scores_go()
        elif self.state.state is self.state.MAINMENU:
            self.main_menu.draw_buttons()
        elif self.state.state is self.state.OPTIONSMENU:
            self.options_menu.draw_buttons()
        pygame.display.flip()

    def _adjust_fps_cap(self):
        """Sets the internal FPS cap for the game.
        Current time is calculated after all other events in the game loop have elapsed
        The time different is how long our frame took to process
        The game will be delayed based on the game's FPS if we finish the loop early"""
        current_time = time.time() 
        time_diff = current_time - self.time_game 
        delay = max(1.0/self.settings.FPS - time_diff, 0)
        time.sleep(delay)
        self.time_game = current_time

    def _clear_state(self):
        """ Resets the stats for the game on play/restart."""
        self.settings._initialize_dynamic_settings()
        self.stats.reset_stats()
        self.scoreboard.prep_score()
        self.scoreboard.prep_ships()
        self.scoreboard.prep_beams()
        self.explosions.empty()
        self.mines.empty()
        self.gunners.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.beams.empty()
        if self.gunners and self.gunners.sprite.gunner_bullets:
            self.gunners.sprite.gunner_bullets.empty()
        self.settings.difficulty_counter = 0
        self._create_fleet()
        self.ship.position_ship()
        self.ship.reset_ship_flip()

    def _update_bullets(self):
        """Update position of the bullets and get rid of the old bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width or bullet.rect.right < 0: 
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision()
        self._check_bullet_mine_collision()
        self._check_bullet_gunner_collision()
        
    def _update_beams(self):
        """Update position of the beams and get rid of the old beams."""
        self.beams.update()
        for beam in self.beams.copy():
            if beam.rect.right > self.settings.screen_width or beam.rect.right < 0: 
                self.beams.remove(beam)
        self._check_bullet_alien_collision()
        self._check_bullet_mine_collision()

    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.aliens,
                self.bullets, False, False)
        collisions_beam = pygame.sprite.groupcollide(self.aliens,
                self.beams, False, False)
        if collisions:
            for alien_index, bullet_indexes in collisions.items():
                self._calculate_score(alien_index, bullet_indexes, 0.5)
                self._play_explosion(alien_index)
                self.bullets.remove(bullet_indexes)
                self._collision_cleanup_and_score(alien_index)
        if collisions_beam:
            for alien_index, beam_indexes in collisions_beam.items():
                self._calculate_score(alien_index, beam_indexes, 0.5)
                self._play_explosion(alien_index)
                self._collision_cleanup_and_score(alien_index)
        if not self.aliens: 
            self._create_fleet()
    
    def _check_bullet_mine_collision(self):
        """Respond to bullet-mines collisions."""
        collisions = pygame.sprite.groupcollide(self.mines,
                self.bullets, False, False)
        collisions_beam = pygame.sprite.groupcollide(self.mines,
                self.beams, False, False)
        if collisions:
            for mine_index, bullet_indexes in collisions.items():
                self._calculate_score(mine_index, bullet_indexes, 1)
                self._play_explosion(mine_index)
                self.bullets.remove(bullet_indexes)
                self._collision_cleanup_and_score(mine_index)
        if collisions_beam:
            for mine_index, beam_indexes in collisions_beam.items():
                self._calculate_score(mine_index, beam_indexes, 1)
                self._play_explosion(mine_index)
                self._collision_cleanup_and_score(mine_index)
        if not self.aliens:
            self._create_fleet()

    def _check_bullet_gunner_collision(self):
        """Respond to bullet-mines collisions."""
        collisions = pygame.sprite.groupcollide(self.gunners,
                self.bullets, False, False)
        collisions_beam = pygame.sprite.groupcollide(self.gunners,
                self.beams, False, False)
        if collisions:
            for gun_index, bullet_indexes in collisions.items():
                if self.gunners and self.gunners.sprite.hitpoints > 0:
                    self.gunners.sprite.hitpoints -= 1
                    self._play_impact(gun_index)
                    self.bullets.remove(bullet_indexes)
                else: 
                    self._calculate_score(gun_index, bullet_indexes, 2.5)
                    self._play_explosion(gun_index, is_gunner = True)
                    self._collision_cleanup_and_score_gunner(gun_index)
       
        if collisions_beam:
            for gun_index, beam_indexes in collisions_beam.items():
                if self.gunners and self.gunners.sprite.hitpoints > 0:
                    self.gunners.sprite.hitpoints -= 5
                    self._play_impact(gun_index, beam_impact = True)
                    if self.gunners.sprite.hitpoints > 0:
                        self.beams.remove(beam_indexes)
                else: 
                    self._calculate_score(gun_index, beam_indexes, 2.5)
                    self._play_explosion(gun_index, is_gunner = True)
                    self._collision_cleanup_and_score_gunner(gun_index)
        if not self.aliens:
            self._create_fleet()

    def _collision_cleanup_and_score_gunner(self,alien_index):
        """Removes collided gunners and bullets and adjusts score."""
        if self.gunners and self.gunners.sprite.gunner_bullets:
            self._explode_missiles()
        alien_index.kill()
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

    def _collision_cleanup_and_score(self,alien_index):
        """Removes collided aliens and adjusts score."""
        alien_index.kill()
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

    def _explode_missiles(self):
        """Plays impact and sounds if enabled."""
        for chonkymissile in self.gunners.sprite.gunner_bullets:
            explosion = Explosion(chonkymissile.rect.center, 2)
            self.explosions.add(explosion)
        
    def _calculate_score(self, alien_index, projectile_index, enemy_mult = 1):
        """Calculates score multipliers for killed enemies."""
        cqc_mult = self._check_cqc_distance(alien_index)
        backstab_mult = self._check_backstab(projectile_index)
        bonus_mult = 1.25 if (cqc_mult > 1 and backstab_mult > 1) else 1
        self.stats.score += round(self.settings.alien_points * 
                (cqc_mult + backstab_mult) * bonus_mult * enemy_mult)
        self.stats.hidden_score += round(self.settings.alien_points * 
                (cqc_mult + backstab_mult) * bonus_mult * enemy_mult)
        self._calculate_beam_addition()

    def _calculate_beam_addition(self):
        """Calculates if the player should received an additional beam charge or 1000 points
        If they hit the score threshold."""
        if self.stats.hidden_score / 5000 >= 1 and not self.settings.adjust_beams:
            if self.stats.charges_remaining < self.settings.beam_limit:
                self.stats.charges_remaining += 1
                self.scoreboard.prep_beams()
            elif self.stats.charges_remaining == self.settings.beam_limit:
                self.stats.score += 500
            self.stats.hidden_score -= 5000
            self.settings.adjust_beams = True
        else:
            self.settings.adjust_beams = False

    def _play_explosion(self, alien_index, is_gunner = False):
        """Plays explosions and sounds if enabled."""
        if not is_gunner:
            explosion = Explosion(alien_index.rect.center)
        else:
            explosion = Explosion(alien_index.rect.center, 3)
        self.explosions.add(explosion)
        self.sound.play_sfx("explosion")

    def _play_impact(self, alien_index, beam_impact= False):
        """Plays impact and sounds if enabled."""
        explosion = Explosion(alien_index.rect.center, 2)
        self.explosions.add(explosion)
        self.sound.play_impact_sfx(beam_impact)

    def _check_cqc_distance(self, alien):
        """Checks to see if the distance between the ship and alien is eligible for a score bonus."""
        formula = sqrt((self.ship.rect.centerx - alien.rect.centerx)**2 + 
                (self.ship.rect.centerx - alien.rect.centerx)**2)
        if formula < 201:
            return 4
        else:
            return 1

    def _check_backstab(self, bullet_indexes):
        """Checks to see if the bullet hit the alien from behind for a score bonus."""
        multiplier = 0
        for bullet_index in bullet_indexes:
            if bullet_index.direction < 0: 
                multiplier += 4
            else:
                multiplier += 1 if not multiplier else 0
        return multiplier

    def _update_aliens(self):
        """Checks if the player ship collides with aliens, 
        then deletes chaff aliens if they go offscreen.""" 
        self.aliens.update()
        self.mines.update()
        self.gunners.update()
        if pygame.sprite.spritecollide(self.ship, self.aliens, False, pygame.sprite.collide_circle):
            self._ship_hit()
        if pygame.sprite.spritecollide(self.ship, self.mines, False, pygame.sprite.collide_circle):
            self._ship_hit()
        if pygame.sprite.spritecollide(self.ship, self.gunners, False, pygame.sprite.collide_mask):
            self._ship_hit()
        if (self.gunners and self.gunners.sprite.gunner_bullets and 
                pygame.sprite.spritecollide(self.ship, self.gunners.sprite.gunner_bullets, 
                    False, pygame.sprite.collide_mask)):
                    self._ship_hit()
        for alien in self.aliens.copy():
            if alien.rect.left < -100: 
                self.aliens.remove(alien)

    def _scroll_background(self):
        """Smoothly scrolls the background image on the screen to give illusion of movement."""
        self.rel_background_x = self.settings.background_x % self.background_image.get_rect().width
        self.screen.blit(self.background_image, (
            self.rel_background_x - self.background_image.get_rect().width, 0))
        if self.rel_background_x < self.settings.screen_width:
            self.screen.blit(self.background_image, (self.rel_background_x, 0))
        self.settings.background_x += self.settings.scroll_speed
    
    def _check_keydown_events(self, event):
        """respond to keypresses.""" 
        if event.key == self.keybinds.MOVEUP:
            self.ship.moving_up = True 
        elif event.key == self.keybinds.MOVEDOWN:
            self.ship.moving_down = True
        if event.key == self.keybinds.MOVELEFT:
            self.ship.moving_left = True 
        elif event.key == self.keybinds.MOVERIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_ESCAPE:
            self._check_pause()
            self._check_exit()
        if (self.keybinds.current_scheme is self.keybinds.ARROWS 
                or self.keybinds.current_scheme is self.keybinds.ARROWS2 
                or self.keybinds.current_scheme is self.keybinds.VIM
                or self.keybinds.current_scheme is self.keybinds.SPACE
                or self.keybinds.current_scheme is self.keybinds.SPACE2
                or self.keybinds.current_scheme is self.keybinds.QWOP):
            if event.key == self.keybinds.MISSILEATTACK and not self.keybinds.use_mouse:
                self._fire_bullet()
            if event.key == self.keybinds.BEAMATTACK and not self.keybinds.use_mouse:
                self._fire_beam()
            if event.key == self.keybinds.FLIPSHIP and not self.keybinds.use_mouse:
                self._flip_ship()

    def _check_mousedown_events(self):
        """respond to keypresses.""" 
        if (self.keybinds.current_scheme is self.keybinds.WASD 
                or self.keybinds.current_scheme is self.keybinds.ESDF):
            mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
            if mouse_buttons[0]:
                self._fire_bullet()
            if mouse_buttons[1]:
                self._fire_beam()
            if mouse_buttons[2]:
                self._flip_ship()

    def _check_keyup_events(self, event):
        """respond to key releases."""
        if event.key == self.keybinds.MOVEUP:
            self.ship.moving_up = False
        elif event.key == self.keybinds.MOVEDOWN:
            self.ship.moving_down = False
        if event.key == self.keybinds.MOVELEFT:
            self.ship.moving_left = False
        elif event.key == self.keybinds.MOVERIGHT:
            self.ship.moving_right = False

    def _check_pause(self):
        """Checks to see if hitting ESC should pause or unpause the game."""
        self.state.pause_state +=1 
        if self.state.pause_state % 2 == 0 and self.state.state == self.state.PAUSE:
            self.state.state = self.state.GAMEPLAY
        elif self.state.pause_state % 2 and self.state.state == self.state.GAMEPLAY:
            self.state.state = self.state.PAUSE

    def _check_exit(self):
        """Checks to see if hitting ESC should exit the game."""
        if self.state.state == self.state.OPTIONSMENU:
            self.state.state = self.state.MAINMENU
        elif self.state.state == self.state.MAINMENU or self.state.state == self.state.GAMEOVER:
            self.stats.dump_stats_json()
            pygame.quit()
            sys.exit()

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if self.state.state == self.state.GAMEPLAY:
            if len(self.bullets) < self.settings.bullets_allowed: 
                new_bullet = Bullet(self)
                if self.ship.is_flipped:
                    new_bullet.rotate_bullet()
                self.bullets.add(new_bullet)
                self.sound.play_sfx("bullet")

    def _fire_beam(self):
        """Create a new beam and add it to the bullets group."""
        if self.state.state == self.state.GAMEPLAY:
            if len(self.beams) < self.stats.charges_remaining: 
                new_beam = Beam(self)
                if self.ship.is_flipped:
                    new_beam.rotate_beam()
                self.beams.add(new_beam)
                self.stats.charges_remaining -= 1
                self.scoreboard.prep_beams()
                self.sound.play_sfx("beam")

    def _flip_ship(self):
        """Flips the ship and firing pattens of the bullet."""
        if self.state.state == self.state.GAMEPLAY:
            self.ship.rotate_ship()
            self._adjust_bullet_flipped()
            self.sound.play_sfx("flip")

    def _adjust_bullet_flipped(self):
        """Adjusts the speed and direction of flipped bullets."""
        if self.ship.is_flipped:
            self.settings.bullet_speed *= 2.50
            self.settings.ship_speed *= 1.25
        else: 
            self.settings.bullet_speed *= 0.4
            self.settings.ship_speed *= 0.80

    def _create_fleet(self):
        """Create the fleet of aliens and find out 
        how many can be populated in each fleet."""
        alien = Alien(self)
        wave_spawn = randint(1,8)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.settings.screen_height - (1.50 * alien_height)
        number_aliens_y = int(available_space_y // (1.50 * alien_height)) 
        ship_width = self.ship.rect.width
        available_space_x = (self.settings.screen_height - 
                (3 * alien_width) - ship_width)
        number_cols = (available_space_x // (2 * alien_width)) 
        self._select_spawn_pattern(wave_spawn, number_cols, number_aliens_y)

    def _create_mine(self, spawn_number = 1):
        """Create an alien and place it in a column."""
        position_list = []
        if len(self.mines) < 20:
            for j in range(0,spawn_number):
                mine = Mine(self)
                self._check_unique_spawn(mine, position_list)
                self.mines.add(mine)

    def _check_unique_spawn(self, mine, position_list):
        """Shuffles the mines' starting positions randomly
        to help prevent them from clumping up on spawn."""
        if not position_list:
            position_list.append(mine.random_pos)
        while mine.random_pos in position_list:
            mine.random_pos = randint(1,10)
            mine.set_random_position()

    def _select_spawn_pattern(self, wave_number, number_cols, number_aliens_y):
        """Selects a wave spawn pattern based on a random number."""
        if wave_number == 1: 
            self._create_mine(5)
            self._create_trash_mobs(number_cols, number_aliens_y)
        elif wave_number == 2:
            self._create_mine(4)
            self._create_trash_mobs(number_cols+1, number_aliens_y)
        elif wave_number == 3:
            self._create_mine(3)
            self._create_trash_mobs(number_cols+2, number_aliens_y)
        elif wave_number == 4:
            self._create_mine(9)
            self._create_trash_mobs(1,3)
        elif wave_number == 5:
            if not self.gunners:
                gunner = Gunner(self)
                self.gunners.add(gunner)
                self._create_mine(4)
                self._create_trash_mobs(1,3)
            else: 
                self._create_mine(9)
                self._create_trash_mobs(1,4)
        elif wave_number == 6:
            if not self.gunners:
                self._create_mine(2)
                self._create_trash_mobs(number_cols, number_aliens_y)
                gunner = Gunner(self)
                self.gunners.add(gunner)
            else: 
                self._create_mine(3)
                self._create_trash_mobs(number_cols+2, number_aliens_y)
        elif wave_number == 7:
            if not self.gunners:
                gunner = Gunner(self)
                self.gunners.add(gunner)
                self._create_mine(2)
                self._create_trash_mobs(number_cols+1, number_aliens_y)
        elif wave_number == 8:
            self._create_trash_mobs(number_cols+3, number_aliens_y)
            self._create_mine(2)

    def _create_trash_mobs(self, number_cols, number_aliens_y):
        """Spawns waves of trash mobs based on wave pattern."""
        for col_number in range(number_cols):
            for alien_number in range(number_aliens_y):
                self._create_alien(alien_number, col_number)

    def _create_alien(self, alien_number, col_number):
        """Create an alien and place it in a column."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.rect.y = alien_height + (1.65 * alien_height * alien_number) +  alien.random_y
        alien.rect.x = (self.settings.screen_width ) + alien_width + int((2.25 * alien_width * col_number))
        alien.x = float(alien.rect.x) 
        alien.y = float(alien.rect.y)
        self.aliens.add(alien)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien. Delete any non-gunner aliens
        and all bullets, play explosions at the player's location, create a new fleet,
        reposition the player ship, and do a brief pause. End the game if no lives left"""
        if self.stats.ships_remaining > 1:
            self.stats.ships_remaining -= 1
            self.scoreboard.prep_ships()
            self._empty_enemies_on_death()
            self._play_explosion_on_death()
            self._create_fleet()
            self.ship.position_ship()
            time.sleep(0.10)
        else: 
            self.enter_game_over()
            self.scoreboard.prep_score_game_over()
            self.scoreboard.prep_high_score_game_over()

    def _empty_enemies_on_death(self):
        """If the player dies, clear all enemies and projectiles
        on the screen except for the gunner."""
        self.aliens.empty()
        self.mines.empty()
        self.bullets.empty()
        if self.gunners and self.gunners.sprite.gunner_bullets:
                self.gunners.sprite.gunner_bullets.empty()

    def _play_explosion_on_death(self):
        """Plays an explosion at the position where the player died."""
        explosion = Explosion(self.ship.rect.center)
        self.explosions.add(explosion)
        self.sound.play_sfx("explosion")

    def _adjust_difficulty(self):
        """Gradually increases the game speed as time elapses."""
        self.settings.difficulty_counter+=1 
        if self.settings.difficulty_counter % (self.settings.FPS * 90) == 0:
            self.settings.increase_speed()

    def _make_game_cinematic(self):
        """Draws cinematic black bars around the top and bottom of the screen, forcing a 16:9 aspect ratio."""
        if self.settings.cinematic_bars:
            self.top_bar.draw_bar()
            self.bot_bar.draw_bar()

    def enter_game_over(self):
        """Game Over Screen that plays when the player dies."""
        self.state.state = self.state.GAMEOVER
        pygame.mixer.music.fadeout(500)

    def _check_mouse_visible(self):
        """Checks if the game is in a state where the mouse is visible."""
        if self.state.state is self.state.GAMEPLAY:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

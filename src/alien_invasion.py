import pygame
import sys
import time
import logging

from alien import Alien
from aspect_ratio import AspectRatio
# from beam import Beam
# from bullet import Bullet
from controller import Controller
from controls_menu import ControlsMenu
from credits_menu import CreditsMenu
from explosion import Explosion
from game_stats import GameStats
from gunner import Gunner
from help_menu import HelpMenu
from keybinds import Keybinds
from math import sqrt, floor
from mine import Mine
from gameover_menu import GameOverMenu
from main_menu import MainMenu
from music import Music
from options_menu import OptionsMenu
from pause_menu import PauseMenu
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
        self.countdown = 3
        self.last_count = pygame.time.get_ticks()
        self._create_sprite_groups()
        self._make_game_objects()
        self._make_logic_dictionaries()
        self._load_images()

    def _load_images(self):
        """Load menu and game background images."""
        self.menu_image = pygame.image.load("assets/images/background.png").convert()
        self.background_image = pygame.image.load("assets/images/parallax_scrolling_background.png").convert()

    def _make_game_objects(self):
        """Create all of the necessary game objects for the game to run."""
        self.previous_time = time.time()
        self.time_game = time.time()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height), pygame.SCALED)
        self.screen_rect = self.screen.get_rect()
        self.keybinds = Keybinds()
        self.state = GameState()
        self.music = Music(self)
        self.sound = Sound(self)
        self.main_menu = MainMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.options_menu = OptionsMenu(self)
        self.controls_menu = ControlsMenu(self)
        self.help_menu = HelpMenu(self)
        self.go_menu = GameOverMenu(self)
        self.pause = PauseMenu(self)
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.controller = Controller(self)
        self.scoreboard = Scoreboard(self)
        self.top_bar = AspectRatio(self)
        self.bot_bar = AspectRatio(self, self.settings.screen_height - 50)

    def _make_logic_dictionaries(self):
        """Create the dictionaries to process logic to replace if/elif statements."""

    def _create_sprite_groups(self):
        """Create sprite group containers for objects."""
        self.bullets = pygame.sprite.Group()
        self.beams = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.mines = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.gunners = pygame.sprite.GroupSingle()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            dt = self.calculate_delta_time()
            self._check_events()
            self.music.play_music()
            self.start_countdown()
            if self.state.state is self.state.GAMEPLAY and self.countdown <= 0:
                self.ship.update(dt)
                self.ship.arrow.update()
                self._update_bullets(dt)
                self._update_beams(dt)
                self._update_aliens(dt)
                for mine in self.mines:
                    mine.warning_arrow.update()
                self.explosions.update(dt)
                self._respawn_enemies(dt)
                self._adjust_difficulty(dt)
            self._check_mouse_visible()
            self._update_screen(dt)
            self.set_fps_cap()

    def calculate_delta_time(self):
        """Calculate delta time to ensure framerate independence."""
        dt = time.time() - self.previous_time
        self.previous_time = time.time()
        return dt

    def set_fps_cap(self):
        """Set the internal FPS cap for the game.

        Current time is calculated after all other events in the game loop have elapsed

        The time different is how long our frame took to process

        The game will be delayed based on the game's FPS if we finish the loop early.

        """
        current_time = time.time()
        time_diff = current_time - self.time_game
        delay = max(1.0 / self.settings.FPS - time_diff, 0)
        time.sleep(delay)
        self.time_game = current_time

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mousedown_events()
            elif event.type == pygame.MOUSEBUTTONUP:
                self._check_mouseup_events()
            elif event.type == pygame.JOYBUTTONDOWN:
                self.controller.check_joybuttondown_events(event)
            elif event.type == pygame.JOYBUTTONUP:
                self.controller.check_joybuttonup_events(event)
            elif event.type == pygame.JOYHATMOTION:
                self.controller.check_joyhatmotion_events(event)
            elif event.type == pygame.JOYAXISMOTION:
                self.controller.check_joyaxismotion_events(event)

    def _update_screen(self, dt):
        """Update images on the screen, and flip to the new screen."""
        if self.state.state is self.state.GAMEPLAY:
            self._scroll_background(dt)
            self.ship.blitme()
            self.ship.arrow.blitme()
            self.bullets.draw(self.screen)
            self.beams.draw(self.screen)
            self.aliens.draw(self.screen)
            self.mines.draw(self.screen)
            for mine in self.mines:
                mine.warning_arrow.blitme()
            self.gunners.draw(self.screen)
            if self.gunners and self.gunners.sprite.gunner_bullets:
                self.gunners.sprite.gunner_bullets.draw(self.screen)
            self.explosions.draw(self.screen)
            self._make_game_cinematic()
            self.scoreboard.show_score()
            if self.countdown > 0:
                self.scoreboard.create_countdown("GET READY", x_offset=-100, y_offset=0)
                self.scoreboard.create_countdown(str(self.countdown), x_offset=100, y_offset=0)
        elif self.state.state is self.state.PAUSE:
            self.pause.render_pause()
        elif self.state.state is self.state.GAMEOVER:
            self.go_menu.draw_buttons()
            self.scoreboard.show_scores_go()
        elif self.state.state is self.state.MAINMENU:
            self.main_menu.draw_buttons()
            self.scoreboard.show_scores_mm()
        elif self.state.state is self.state.OPTIONSMENU:
            self.options_menu.draw_buttons()
        elif self.state.state is self.state.CONTROLSMENU:
            self.controls_menu.draw_buttons()
        elif self.state.state is self.state.HELPMENU:
            self.help_menu.draw_buttons()
        elif self.state.state is self.state.CREDITSMENU:
            self.credits_menu.draw_buttons()
        pygame.display.flip()

    def _clear_state(self):
        """Reset the stats for the game on play/restart."""
        self.settings._initialize_dynamic_settings()
        self.stats.reset_stats()
        self.scoreboard.prep_score()
        self.scoreboard.prep_ships()
        self.scoreboard.prep_beams()
        self.scoreboard.prep_missiles()
        self.explosions.empty()
        self.mines.empty()
        self.gunners.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.beams.empty()
        if self.gunners and self.gunners.sprite.gunner_bullets:
            self.gunners.sprite.gunner_bullets.empty()
        self.ship.position_ship()
        self.ship.reset_ship_flip()
        self.settings.respawn_timer = 0.0
        self.countdown = 3
        self.last_count = pygame.time.get_ticks()

    def _update_bullets(self, dt):
        """Update position of the bullets and get rid of the old bullets."""
        self.bullets.update(dt)
        for bullet in self.bullets.copy():
            if bullet.rect.right > self.settings.screen_width or bullet.rect.right < 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collision(self.aliens, 0.5)
        self._check_bullet_alien_collision(self.mines, 1)
        self._check_bullet_alien_collision(self.gunners, 3.0)

    def _update_beams(self, dt):
        """Update position of the beams and get rid of the old beams."""
        self.beams.update(dt)
        for beam in self.beams.copy():
            if beam.rect.right > self.settings.screen_width or beam.rect.right < 0:
                self.beams.remove(beam)
        self._check_bullet_alien_collision(self.aliens, 0.5)
        self._check_bullet_alien_collision(self.mines, 0.75)
        self._check_bullet_alien_collision(self.gunners, 3.0)

    def _check_bullet_alien_collision(self, enemy_list, score_multiplier):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(enemy_list, self.bullets, False, False)
        collisions_beam = pygame.sprite.groupcollide(enemy_list, self.beams, False, False)
        self._process_collision(collisions, enemy_list, score_multiplier, False)
        self._process_collision(collisions_beam, enemy_list, score_multiplier, True)

    def _process_collision(self, collisions, enemy_list, score_multiplier, is_beam):
        """Process the game logic based on the type of collision."""
        if collisions:
            for alien_index, bullet_indexes in collisions.items():
                if enemy_list is self.aliens or enemy_list is self.mines:
                    self._process_trash_and_mines(alien_index, bullet_indexes, score_multiplier, is_beam)
                elif enemy_list is self.gunners:
                    if self.gunners and self.gunners.sprite.hitpoints > 0:
                        self._damage_gunner(alien_index, bullet_indexes, is_beam)
                    else:
                        self._kill_gunner(alien_index, bullet_indexes, score_multiplier)

    def _process_trash_and_mines(self, alien_index, bullet_indexes, score_multiplier, is_beam):
        """If the enemy is a trash mob or a mine, calculate score, effects, and cleanup."""
        self._calculate_score(alien_index, bullet_indexes, score_multiplier)
        self._play_explosion(alien_index)
        if not is_beam:
            self.bullets.remove(bullet_indexes)
        self._collision_cleanup_and_score(alien_index)

    def _damage_gunner(self, alien_index, bullet_indexes, is_beam):
        """If the enemy is a gunner and isn't killed by an impact,

        calculate damage dealt and effects.
        """
        if is_beam:
            self.gunners.sprite.hitpoints -= 5
            self._play_impact(alien_index, beam_impact=True)
            if self.gunners.sprite.hitpoints > 0:
                self.beams.remove(bullet_indexes)
        elif not is_beam:
            self.gunners.sprite.hitpoints -= 1
            self._play_impact(alien_index)
            self.bullets.remove(bullet_indexes)

    def _kill_gunner(self, alien_index, bullet_indexes, score_multiplier):
        """If the enemy is a gunner and we kill it, calculate score, effects, and cleanup."""
        self._calculate_score(alien_index, bullet_indexes, score_multiplier)
        self._play_explosion(alien_index, is_gunner=True)
        self._collision_cleanup_and_score_gunner(alien_index)

    def _collision_cleanup_and_score_gunner(self, alien_index):
        """Remove collided gunners and bullets and adjusts score."""
        if self.gunners and self.gunners.sprite.gunner_bullets:
            self._explode_missiles()
        alien_index.kill()
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

    def _collision_cleanup_and_score(self, alien_index):
        """Remove collided aliens and adjusts score."""
        alien_index.kill()
        self.scoreboard.prep_score()
        self.scoreboard.check_high_score()

    def _explode_missiles(self):
        """Play impact and sounds if enabled."""
        for chonkymissile in self.gunners.sprite.gunner_bullets:
            explosion = Explosion(chonkymissile.rect.center, 2)
            self.explosions.add(explosion)

    def _calculate_score(self, alien_index, projectile_index, enemy_mult=1):
        """Calculate score multipliers for killed enemies."""
        cqc_mult = self._check_cqc_distance(alien_index)
        backstab_mult = self._check_backstab(projectile_index)
        bonus_mult = 1.25 if (cqc_mult > 1 and backstab_mult > 1) else 1
        self.stats.score += round(self.settings.alien_points * (cqc_mult + backstab_mult) * bonus_mult * enemy_mult)
        self.stats.hidden_score += round(
            self.settings.alien_points * (cqc_mult + backstab_mult) * bonus_mult * enemy_mult
        )
        self._calculate_beam_addition()

    def _calculate_beam_addition(self):
        """Calculate if the player should get an extra beam charge or points if pass the score threshold."""
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

    def _play_explosion(self, alien_index, is_gunner=False):
        """Plays explosions and sounds if enabled."""
        if not is_gunner:
            explosion = Explosion(alien_index.rect.center)
        else:
            explosion = Explosion(alien_index.rect.center, 3)
        self.explosions.add(explosion)
        self.sound.play_sfx("explosion")

    def _play_impact(self, alien_index, beam_impact=False):
        """Plays impact and sounds if enabled."""
        explosion = Explosion(alien_index.rect.center, 2)
        self.explosions.add(explosion)
        self.sound.play_impact_sfx(beam_impact)

    def _check_cqc_distance(self, alien):
        """Check to see if the distance between the ship and alien is eligible for a score bonus."""
        formula = sqrt(
            (self.ship.rect.centerx - alien.rect.centerx) ** 2 + (self.ship.rect.centerx - alien.rect.centerx) ** 2
        )
        if formula < 201:
            return 4
        else:
            return 1

    def _check_backstab(self, bullet_indexes):
        """Check to see if the bullet hit the alien from behind for a score bonus."""
        multiplier = 0
        for bullet_index in bullet_indexes:
            if bullet_index.direction < 0:
                multiplier += 4
            else:
                multiplier += 1 if not multiplier else 0
        return multiplier

    def _update_aliens(self, dt):
        """Check if the player collides with aliens, then delete trash aliens if they go offscreen."""
        self.aliens.update(dt)
        self.mines.update(dt)
        self.gunners.update(dt)
        if pygame.sprite.spritecollide(self.ship, self.aliens, False, pygame.sprite.collide_circle):
            self._ship_hit()
        if pygame.sprite.spritecollide(self.ship, self.mines, False, pygame.sprite.collide_circle):
            self._ship_hit()
        if pygame.sprite.spritecollide(self.ship, self.gunners, False, pygame.sprite.collide_mask):
            self._ship_hit()
        if (
            self.gunners
            and self.gunners.sprite.gunner_bullets
            and pygame.sprite.spritecollide(
                self.ship, self.gunners.sprite.gunner_bullets, False, pygame.sprite.collide_mask
            )
        ):
            self._ship_hit()
        for alien in self.aliens.copy():
            if alien.rect.left < -100:
                self.aliens.remove(alien)

    def _scroll_background(self, dt):
        """Smoothly scrolls the background image on the screen to give illusion of movement."""
        self.rel_background_x = self.settings.background_x % self.background_image.get_rect().width
        self.screen.blit(self.background_image, (self.rel_background_x - self.background_image.get_rect().width, 0))
        if self.rel_background_x < self.settings.screen_width:
            self.screen.blit(self.background_image, (self.rel_background_x, 0))
        self.settings.background_x += floor((self.settings.scroll_speed * dt * 10) / 10)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        '''self.main_menu = MainMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.options_menu = OptionsMenu(self)
        self.controls_menu = ControlsMenu(self)
        self.help_menu = HelpMenu(self)
        self.go_menu = GameOverMenu(self)'''
        if self.state.state == self.state.MAINMENU:
            if event.key == pygame.K_UP:
                self.main_menu.update_cursor(direction=1)
            elif event.key == pygame.K_DOWN:
                self.main_menu.update_cursor(direction=-1)
            elif event.key == pygame.K_RETURN:
                self.sound.play_sfx("options_menu")
                self.main_menu.enter_pressed = True
                self.main_menu.menu_event_dict.get(self.main_menu.buttons[self.main_menu.index])()
        elif self.state.state == self.state.OPTIONSMENU:
            if event.key == pygame.K_UP:
                self.options_menu.update_cursor(direction=1)
            elif event.key == pygame.K_DOWN:
                self.options_menu.update_cursor(direction=-1)
            elif event.key == pygame.K_RETURN:
                self.sound.play_sfx("options_menu")
                self.options_menu.enter_pressed = True
                (self.options_menu.menu_event_dict.get(self.options_menu.buttons[self.options_menu.index])
                 (direction=1))
        elif self.state.state == self.state.HELPMENU:
            if event.key == pygame.K_UP:
                self.help_menu.update_cursor(direction=1)
            elif event.key == pygame.K_DOWN:
                self.help_menu.update_cursor(direction=-1)
            elif event.key == pygame.K_RETURN:
                self.sound.play_sfx("options_menu")
                self.help_menu.enter_pressed = True
                self.help_menu.menu_event_dict.get(self.help_menu.buttons[self.help_menu.index])()
        elif self.state.state == self.state.CONTROLSMENU:
            if event.key == pygame.K_UP:
                self.controls_menu.update_cursor(direction=1)
            elif event.key == pygame.K_DOWN:
                self.controls_menu.update_cursor(direction=-1)
            elif event.key == pygame.K_RETURN:
                self.sound.play_sfx("options_menu")
                self.controls_menu.enter_pressed = True
                self.controls_menu.menu_event_dict.get(self.controls_menu.buttons[self.controls_menu.index])(self.controls_menu.buttons[self.controls_menu.index], self.controls_menu.key_buttons.get(self.controls_menu.buttons[self.controls_menu.index]))
        elif self.state.state == self.state.CREDITSMENU:
            if event.key == pygame.K_UP:
                self.credits_menu.update_cursor(direction=1)
            elif event.key == pygame.K_DOWN:
                self.credits_menu.update_cursor(direction=-1)
            elif event.key == pygame.K_RETURN:
                self.sound.play_sfx("options_menu")
                self.credits_menu.enter_pressed = True
                self.credits_menu.menu_event_dict.get(self.credits_menu.func_buttons[self.credits_menu.index])()
        elif self.state.state == self.state.GAMEPLAY:
            if event.key == self.keybinds.controls.get(self.keybinds.MOVEUP):
                self.ship.moving_up = True
            elif event.key == self.keybinds.controls.get(self.keybinds.MOVEDOWN):
                self.ship.moving_down = True
            if event.key == self.keybinds.controls.get(self.keybinds.MOVELEFT):
                self.ship.moving_left = True
            elif event.key == self.keybinds.controls.get(self.keybinds.MOVERIGHT):
                self.ship.moving_right = True
            if event.key == self.keybinds.controls.get(self.keybinds.MISSILEATTACK):
                self.ship.is_firing = True
            if event.key == self.keybinds.controls.get(self.keybinds.BEAMATTACK):
                self.ship.fire_beam()
            if event.key == self.keybinds.controls.get(self.keybinds.FLIPSHIP):
                self.ship.flip_ship()
        if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
            self.pause.check_pause()
            self._check_exit()
        if event.key == pygame.K_DELETE:
            self.stats.dump_stats_json()
            pygame.quit()
            sys.exit()

    def _check_mousedown_events(self):
        """Respond to mouse clicks."""
        mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)
        mouse_pos = pygame.mouse.get_pos()
        if mouse_buttons[0] and self.state.state == self.state.CONTROLSMENU:
            self.controls_menu.check_controls_menu_buttons(mouse_pos)
        if mouse_buttons[2] and self.state.state == self.state.CONTROLSMENU:
            self.controls_menu.clear_keybind_button(mouse_pos)
        elif (mouse_buttons[0] or mouse_buttons[2]) and (
            self.state.state != self.state.GAMEPLAY
            or self.state.state != self.state.PAUSE
            or self.state.state != self.state.CONTROLSMENU
        ):
            if self.state.state == self.state.MAINMENU:
                self.main_menu.check_menu_buttons()
            elif self.state.state == self.state.OPTIONSMENU:
                self.options_menu.check_menu_buttons()
            elif self.state.state == self.state.GAMEOVER:
                self.go_menu.check_menu_buttons()
            elif self.state.state == self.state.HELPMENU:
                self.help_menu.check_menu_buttons()
            elif self.state.state == self.state.CREDITSMENU:
                self.credits_menu.check_menu_buttons()
        if self.state.state == self.state.GAMEPLAY:
            if mouse_buttons[0]:
                self.ship.is_firing = True
            if mouse_buttons[1]:
                self.ship.fire_beam()
            if mouse_buttons[2]:
                self.ship.flip_ship()

    def _check_mouseup_events(self):
        """Respond to mouse releases."""
        mouse_buttons = pygame.mouse.get_pressed(num_buttons=3)

        if self.state.state == self.state.GAMEPLAY or self.state.state == self.state.PAUSE:
            if not mouse_buttons[0]:
                self.ship.is_firing = False

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if self.state.state == self.state.MAINMENU:
            if event.key == pygame.K_RETURN:
                self.main_menu.enter_pressed = False
        if self.state.state == self.state.OPTIONSMENU:
            if event.key == pygame.K_RETURN:
                self.options_menu.enter_pressed = False
        elif self.state.state == self.state.GAMEPLAY:
            if event.key == self.keybinds.controls.get(self.keybinds.MOVEUP):
                self.ship.moving_up = False
            elif event.key == self.keybinds.controls.get(self.keybinds.MOVEDOWN):
                self.ship.moving_down = False
            if event.key == self.keybinds.controls.get(self.keybinds.MOVELEFT):
                self.ship.moving_left = False
            elif event.key == self.keybinds.controls.get(self.keybinds.MOVERIGHT):
                self.ship.moving_right = False
            if event.key == self.keybinds.controls.get(self.keybinds.MISSILEATTACK):
                self.ship.is_firing = False

    def _check_exit(self):
        """Check to see if hitting ESC should exit the game."""
        if (self.state.state == self.state.OPTIONSMENU or self.state.state == self.state.HELPMENU
                or self.state.state == self.state.CREDITSMENU):
            self.state.state = self.state.MAINMENU
        elif self.state.state == self.state.CONTROLSMENU and pygame.K_UNDERSCORE not in self.keybinds.controls.values():
            self.state.state = self.state.MAINMENU
        elif self.state.state == self.state.MAINMENU or self.state.state == self.state.GAMEOVER:
            self.stats.dump_stats_json()
            pygame.quit()
            sys.exit()

    def _create_fleet(self):
        """Create the fleet of aliens and calculate how many are in each fleet."""
        alien = Alien(self)
        wave_spawn = randint(1, 8)
        alien_width, alien_height = alien.rect.size
        available_space_y = self.settings.screen_height - (1.50 * alien_height)
        number_aliens_y = int(available_space_y // (1.50 * alien_height))
        ship_width = self.ship.rect.width
        available_space_x = self.settings.screen_height - (3 * alien_width) - ship_width
        number_cols = available_space_x // (2 * alien_width)
        self._select_spawn_pattern(wave_spawn, number_cols, number_aliens_y)

    def _create_mine(self, spawn_number=1):
        """Create an alien and place it in a column."""
        position_list = []
        if len(self.mines) < 20:
            for j in range(0, spawn_number):
                mine = Mine(self)
                self._check_unique_spawn(mine, position_list)
                self.mines.add(mine)

    def _check_unique_spawn(self, mine, position_list):
        """Shuffles the mines' starting positions to reduce spawn clumping."""
        if not position_list:
            position_list.append(mine.random_pos)
        while mine.random_pos in position_list:
            mine.random_pos = randint(1, 10)
            mine.set_random_position()

    def _select_spawn_pattern(self, wave_number, number_cols, number_aliens_y):
        """Select a wave spawn pattern based on a random number."""
        if wave_number == 1:
            self._create_mine(5)
            self._create_trash_mobs(number_cols, number_aliens_y)
        elif wave_number == 2:
            self._create_mine(4)
            self._create_trash_mobs(number_cols + 1, number_aliens_y)
        elif wave_number == 3:
            self._create_mine(3)
            self._create_trash_mobs(number_cols + 2, number_aliens_y)
        elif wave_number == 4:
            self._create_mine(9)
            self._create_trash_mobs(1, 3)
        elif wave_number == 5:
            if not self.gunners:
                gunner = Gunner(self)
                self.gunners.add(gunner)
                self._create_mine(4)
                self._create_trash_mobs(1, 3)
            else:
                self._create_mine(9)
                self._create_trash_mobs(1, 4)
        elif wave_number == 6:
            if not self.gunners:
                self._create_mine(2)
                self._create_trash_mobs(number_cols, number_aliens_y)
                gunner = Gunner(self)
                self.gunners.add(gunner)
            else:
                self._create_mine(3)
                self._create_trash_mobs(number_cols + 2, number_aliens_y)
        elif wave_number == 7:
            if not self.gunners:
                gunner = Gunner(self)
                self.gunners.add(gunner)
                self._create_mine(2)
                self._create_trash_mobs(number_cols + 1, number_aliens_y)
            else:
                self._create_mine(1)
                self._create_trash_mobs(number_cols + 3, number_aliens_y)
        elif wave_number == 8:
            self._create_trash_mobs(number_cols + 3, number_aliens_y)
            self._create_mine(2)
        else:
            self._create_trash_mobs(number_cols + 3, number_aliens_y)

    def _create_trash_mobs(self, number_cols, number_aliens_y):
        """Spawns waves of trash mobs based on wave pattern."""
        for col_number in range(number_cols):
            for alien_number in range(number_aliens_y):
                self._create_alien(alien_number, col_number)

    def _create_alien(self, alien_number, col_number):
        """Create an alien and place it in a column."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.rect.y = alien_height + (1.65 * alien_height * alien_number) + alien.random_y
        alien.rect.x = (self.settings.screen_width + 100) + alien_width + int((2.25 * alien_width * col_number))
        alien.x = float(alien.rect.x)
        alien.y = float(alien.rect.y)
        self.aliens.add(alien)

    def _ship_hit(self):
        """Respond to the ship being hit by an alien. Delete any non-gunner aliens

        and all bullets, play explosions at the player's location, create a new fleet,

        reposition the player ship, and do a brief pause. End the game if no lives left
        """
        if self.stats.ships_remaining > 1:
            self.stats.ships_remaining -= 1
            self.scoreboard.prep_ships()
            self._empty_enemies_on_death()
            self._play_explosion_on_death()
            self.ship.position_ship()
            self.settings.respawn_timer = -0.5
            time.sleep(0.10)
        else:
            self.enter_game_over()
            self.scoreboard.prep_score_game_over()
            self.scoreboard.prep_high_score_game_over()

    def _empty_enemies_on_death(self):
        """If the player dies, clear all enemies and projectiles on the screen."""
        self.aliens.empty()
        self.mines.empty()
        self.bullets.empty()
        self.gunners.empty()
        if self.gunners and self.gunners.sprite.gunner_bullets:
            self.gunners.sprite.gunner_bullets.empty()

    def _play_explosion_on_death(self):
        """Plays an explosion at the position where the player died."""
        explosion = Explosion(self.ship.rect.center)
        self.explosions.add(explosion)
        self.sound.play_sfx("explosion")

    def _adjust_difficulty(self, dt):
        """Gradually increases the game speed as time elapses."""
        self.settings.difficulty_counter += 1 * dt
        if self.settings.difficulty_counter - 20 > 0:
            self.settings.difficulty_counter -= 20
            self.settings.increase_speed()

    def _respawn_enemies(self, dt):
        """Gradually increases the game speed as time elapses."""
        self.settings.respawn_timer += 1 * dt
        if self.settings.respawn_timer - 0.10 > 0 and not self.aliens:
            self.settings.respawn_timer -= 0.10
            self._create_fleet()

    def _make_game_cinematic(self):
        """Draws cinematic black bars around the top and bottom of the screen, forcing a 16:9 aspect ratio."""
        self.top_bar.draw_bar()
        self.bot_bar.draw_bar()

    def enter_game_over(self):
        """Game Over Screen that plays when the player dies."""
        self.state.state = self.state.GAMEOVER
        pygame.mixer.music.fadeout(500)

    def _check_mouse_visible(self):
        """Check if the game is in a state where the mouse is visible."""
        if self.state.state is self.state.GAMEPLAY:
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

    def start_countdown(self):
        """Create the game countdown timer and decrements it over time."""
        count_timer = pygame.time.get_ticks()
        if count_timer - self.last_count > 1000:
            self.countdown -= 1
            self.last_count = count_timer


if __name__ == '__main__':
    """Logs traceback in case of crash/unexcepted application exit."""
    ai = AlienInvasion()
    try:
        ai.run_game()
    except SystemExit:
        pass
    except:
        logging.basicConfig(filename="ERROR.log", filemode='w', level=logging.ERROR)
        logging.exception('')

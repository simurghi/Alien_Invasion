import pygame


class Sound:
    """Class to track and manage sound in Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize attributes of sound class."""
        self.settings = ai_game.settings
        self.state = ai_game.state
        self._load_sfx()
        self._sound_counts = {}
        self._base_volumes = {
            "bullet": 0.40,
            "beam": 0.80,
            "explosion": 0.40,
            "menu": 0.40,
            "menu_denied": 0.40,
            "menu_unselect": 0.40,
            "flip": 0.40,
            "damage": 0.55,
            "beam_damage": 0.60,
            "gunner": 0.40,
            "withmine": 0.75,
        }
        self._set_volume()

    def _load_sfx(self):
        """Load sound assets."""
        self.bullet_sfx = pygame.mixer.Sound("assets/audio/MissileFire.wav")
        self.beam_sfx = pygame.mixer.Sound("assets/audio/LaserShot.wav")
        self.explosion_sfx = pygame.mixer.Sound("assets/audio/DestroyMonster2.wav")
        self.menu_sfx = pygame.mixer.Sound("assets/audio/OptionSelect.wav")
        self.menu_denied_sfx = pygame.mixer.Sound("assets/audio/SelectMenuItemOrHover.wav")
        self.menu_unselect_sfx = pygame.mixer.Sound("assets/audio/SelectAnOption.wav")
        self.flip_sfx = pygame.mixer.Sound("assets/audio/UnitFlip.wav")
        self.damage_sfx = pygame.mixer.Sound("assets/audio/MiniHitImpact.wav")
        self.beam_damage_sfx = pygame.mixer.Sound("assets/audio/HitOnEnergeticShield.wav")
        self.gunner_sfx = pygame.mixer.Sound("assets/audio/SingleShot2.wav")
        self.detect_sfx = pygame.mixer.Sound("assets/audio/MineDetected.wav")

    def _set_volume(self):
        """Set the volumes for the game sounds."""
        self.bullet_sfx.set_volume(self._base_volumes["bullet"] * self.settings.sound_volume)
        self.beam_sfx.set_volume(self._base_volumes["beam"] * self.settings.sound_volume)
        self.explosion_sfx.set_volume(self._base_volumes["explosion"] * self.settings.sound_volume)
        self.menu_sfx.set_volume(self._base_volumes["menu"] * self.settings.sound_volume)
        self.menu_denied_sfx.set_volume(
            self._base_volumes["menu_denied"] * self.settings.sound_volume
        )
        self.menu_unselect_sfx.set_volume(
            self._base_volumes["menu_unselect"] * self.settings.sound_volume
        )
        self.flip_sfx.set_volume(self._base_volumes["flip"] * self.settings.sound_volume)
        self.damage_sfx.set_volume(self._base_volumes["damage"] * self.settings.sound_volume)
        self.beam_damage_sfx.set_volume(
            self._base_volumes["beam_damage"] * self.settings.sound_volume
        )
        self.gunner_sfx.set_volume(self._base_volumes["gunner"] * self.settings.sound_volume)
        self.detect_sfx.set_volume(self._base_volumes["withmine"] * self.settings.sound_volume)

    def play_sfx(self, sound_event):
        """Play sound effects based on game state and event."""
        if not self.settings.sound_volume:
            return

        sound_map = {
            # Gameplay (scaled)
            "explosion": ({self.state.GAMEPLAY}, self.explosion_sfx),
            "bullet": ({self.state.GAMEPLAY}, self.bullet_sfx),
            "beam": ({self.state.GAMEPLAY}, self.beam_sfx),
            "flip": ({self.state.GAMEPLAY}, self.flip_sfx),
            "gunner": ({self.state.GAMEPLAY}, self.gunner_sfx),
            "mine": ({self.state.GAMEPLAY}, self.detect_sfx),

            # Menu (no scaling)
            "options_menu": (self.state.MENU_STATES, self.menu_sfx),
            "options_menu_unselect": (self.state.MENU_STATES, self.menu_unselect_sfx),
            "options_menu_denied": (self.state.MENU_STATES, self.menu_denied_sfx),

            # Game over
            "game_over": ({self.state.GAMEOVER}, self.menu_sfx),
        }

        if sound_event not in sound_map:
            return

        required_states, sound = sound_map[sound_event]

        if self.state.state not in required_states:
            return

        # --- Gameplay sounds: apply scaling ---

        if sound_event in {
            "explosion", "bullet", "beam", "flip", "gunner", "withmine"
        }:
            count = self._sound_counts.get(sound_event, 0)
            scale = max(0.2, 1.0 / (count + 1))
            base_volume = self._base_volumes.get(sound_event, 0.4)

            sound.set_volume(base_volume * self.settings.sound_volume * scale)
            self._sound_counts[sound_event] = count + 1

        sound.play()

    def play_impact_sfx(self, beam_impact):
        """Check to see if the game should play damage SFX and play beam or bullet sounds."""
        if (
            self.settings.sound_volume
            and self.state.state is self.state.GAMEPLAY
            and not beam_impact
        ):
            self.damage_sfx.play()
        elif self.settings.sound_volume and self.state.state is self.state.GAMEPLAY and beam_impact:
            self.beam_damage_sfx.play()

    def reset_frame(self):
        self._sound_counts.clear()

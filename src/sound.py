import pygame

class Sound:
    """Class to track and manage sound in Alien Invasion."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self._load_sfx()
        self._set_volume()
 
    def _load_sfx(self):
        """Loads sound assets."""
        self.bullet_sfx = pygame.mixer.Sound("assets/audio/MissileFire.wav")
        self.beam_sfx = pygame.mixer.Sound("assets/audio/LaserShot.wav")
        self.explosion_sfx = pygame.mixer.Sound("assets/audio/DestroyMonster2.wav")
        self.menu_sfx = pygame.mixer.Sound("assets/audio/OptionSelect.wav")
        self.flip_sfx = pygame.mixer.Sound("assets/audio/UnitFlip.wav")
        self.damage_sfx = pygame.mixer.Sound("assets/audio/MiniHitImpact.wav")
        self.beam_damage_sfx = pygame.mixer.Sound("assets/audio/HitOnEnergeticShield.wav")

    def _set_volume(self):
        """Sets the volumes for the game sounds."""
        self.bullet_sfx.set_volume(0.40)
        self.beam_sfx.set_volume(0.80)
        self.explosion_sfx.set_volume(0.40)
        self.menu_sfx.set_volume(0.40)
        self.flip_sfx.set_volume(0.40)
        self.damage_sfx.set_volume(0.55)
        self.beam_damage_sfx.set_volume(0.60)

    def play_sfx(self, sound_event):
        """Checks to see if the game should play explosion SFX."""
        if self.settings.play_sfx:
            if (sound_event == "explosion" and 
                    self.stats.state is self.stats.GAMEPLAY):
                self.explosion_sfx.play()
            elif (sound_event == "bullet" and 
                self.stats.state is self.stats.GAMEPLAY):
                self.bullet_sfx.play()
            elif (sound_event == "beam" and 
                self.stats.state is self.stats.GAMEPLAY):
                self.beam_sfx.play()
            elif (sound_event == "flip" and 
                    self.stats.state is self.stats.GAMEPLAY):
                self.flip_sfx.play()

    def play_impact_sfx(self, beam_impact):
        """Checks to see if the game should play damage SFX
        and play beam or bullet sounds."""
        if (self.settings.play_sfx and 
                self.stats.state is self.stats.GAMEPLAY and not beam_impact):
            self.damage_sfx.play()
        elif (self.settings.play_sfx and 
                self.stats.state is self.stats.GAMEPLAY and beam_impact):
            self.beam_damage_sfx.play()

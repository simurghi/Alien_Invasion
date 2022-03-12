import pygame

class Sound:
    """Class to track and manage sound in Alien Invasion."""
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.state = ai_game.state
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
        self.gunner_sfx = pygame.mixer.Sound('assets/audio/SingleShot2.wav')
        self.detect_sfx = pygame.mixer.Sound('assets/audio/MineDetected.wav')

    def _set_volume(self):
        """Sets the volumes for the game sounds."""
        self.bullet_sfx.set_volume(0.40)
        self.beam_sfx.set_volume(0.80)
        self.explosion_sfx.set_volume(0.40)
        self.menu_sfx.set_volume(0.40)
        self.flip_sfx.set_volume(0.40)
        self.damage_sfx.set_volume(0.55)
        self.beam_damage_sfx.set_volume(0.60)
        self.gunner_sfx.set_volume(0.40)
        self.detect_sfx.set_volume(0.75)

    def play_sfx(self, sound_event):
        """Checks to see if the game should play explosion SFX."""
        if self.settings.play_sfx:
            if (sound_event == "explosion" and 
                    self.state.state is self.state.GAMEPLAY):
                self.explosion_sfx.play()
            elif (sound_event == "bullet" and 
                self.state.state is self.state.GAMEPLAY):
                self.bullet_sfx.play()
            elif (sound_event == "beam" and 
                self.state.state is self.state.GAMEPLAY):
                self.beam_sfx.play()
            elif (sound_event == "flip" and 
                    self.state.state is self.state.GAMEPLAY):
                self.flip_sfx.play()
            elif (sound_event == "gunner" and 
                    self.state.state is self.state.GAMEPLAY):
                self.gunner_sfx.play()
            elif (sound_event == "mine" and
                    self.state.state is self.state.GAMEPLAY):
                self.detect_sfx.play()
            elif (sound_event == "options_menu" and 
                    self.state.state is not self.state.GAMEOVER):
                self.menu_sfx.play()
            elif (sound_event == "game_over" and 
                    self.state.state is self.state.GAMEOVER):
                self.menu_sfx.play()
            else:
                pass

    def play_impact_sfx(self, beam_impact):
        """Checks to see if the game should play damage SFX
        and play beam or bullet sounds."""
        if (self.settings.play_sfx and 
                self.state.state is self.state.GAMEPLAY and not beam_impact):
            self.damage_sfx.play()
        elif (self.settings.play_sfx and 
                self.state.state is self.state.GAMEPLAY and beam_impact):
            self.beam_damage_sfx.play()

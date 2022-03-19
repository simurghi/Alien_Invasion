import pygame 

class Music:
    """Class to track and manage music based on game state."""

    def __init__(self, ai_game):
        """Initialize music state."""
        self.state = ai_game.state
        self.settings = ai_game.settings

    def play_music(self):
        """Selects which music to play based on the state of the game."""
        self._toggle_mute()
        if (self.state.state is self.state.MAINMENU 
                or self.state.state is self.state.OPTIONSMENU) and not self.state.music_state["MENU"]:
                pygame.mixer.music.load("assets/audio/menu.wav")
                pygame.mixer.music.play(-1)
                self._clear_music_state()
                self.state.music_state["MENU"] = True
        elif self.state.state is self.state.GAMEPLAY and not self.state.music_state["GAMEPLAY"]:
                pygame.mixer.music.load("assets/audio/battle.wav")
                pygame.mixer.music.play(-1)
                self._clear_music_state()
                self.state.music_state["GAMEPLAY"] = True
        elif self.state.state is self.state.PAUSE and not self.state.music_state["PAUSE"]:
                pygame.mixer.music.load("assets/audio/loading.wav")
                pygame.mixer.music.play(-1)
                self._clear_music_state()
                self.state.music_state["PAUSE"] = True
        elif self.state.state is self.state.GAMEOVER and not self.state.music_state["GAMEOVER"]:
                pygame.mixer.music.load("assets/audio/Disengage.wav")
                pygame.mixer.music.play(-1)
                self._clear_music_state()
                self.state.music_state["GAMEOVER"] = True

    def _toggle_mute(self):
        """Helper methods that sets volume of a track based on state and if option enabled."""
        if not self.settings.play_music:
            pygame.mixer.music.set_volume(0.0)
        elif self.state.music_state["GAMEOVER"] and self.settings.play_music:
            pygame.mixer.music.set_volume(0.5)
        elif self.settings.play_music:
            pygame.mixer.music.set_volume(1.0)

    def _clear_music_state(self):
        """Helper method that clears the music state dictionary to False values."""
        for music in self.state.music_state:
            self.state.music_state[music] = False


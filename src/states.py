import pygame

class GameState:
    """Class to manage the state of the game."""

    def __init__(self):
        self._create_game_states()
        self._set_dynamic_states()

    def _create_game_states(self):
        """Creates instance variables necessary for the game states to function."""
        self.MAINMENU = 1
        self.GAMEPLAY = 2
        self.PAUSE = 3
        self.GAMEOVER = 4
        self.OPTIONSMENU = 5

    def _set_dynamic_states(self):
        """Creates the game states that game be changed throughout the game."""
        self.state = self.MAINMENU
        self.pause_state = 0
        self.music_state = {"GAMEPLAY": False, "MENU": False, "GAMEOVER": False, "PAUSE": False}


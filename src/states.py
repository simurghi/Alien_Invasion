

class GameState:
    """Class to manage the state of the game."""

    def __init__(self):
        """Create the game state constants."""
        self._create_game_states()
        self._set_dynamic_states()

    def _create_game_states(self):
        """Create instance variables necessary for the game states to function."""
        self.MAINMENU = 1
        self.GAMEPLAY = 2
        self.PAUSE = 3
        self.GAMEOVER = 4
        self.OPTIONSMENU = 5
        self.CONTROLSMENU = 6
        self.HELPMENU = 7
        self.CREDITSMENU = 8

    def _set_dynamic_states(self):
        """Create the game states that game be changed throughout the game."""
        self.state = self.MAINMENU
        self.pause_state = 0
        self.music_state = {"COUNTDOWN": False, "GAMEPLAY": False, "MENU": False, "GAMEOVER": False, "PAUSE": False}

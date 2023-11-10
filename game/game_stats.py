# DEFINE GAME STATS


class GameStats:
    """Track stats as the game is running"""

    def __init__(self, si_game):
        """Initialize stats"""

        # Import settings from main game
        self.settings = si_game.settings

        # High score attribute
        # self.high_score_file = 'high_score.txt'

        # Initialize this attribute within the method call, instead of init
        self.reset_all_stats()

        # Get the highest score
        # self.get_high_score()

        # Start space Invaders when this flag is True
        self.game_active = False

        # Any time the game is loaded this will be True
        self.first_run = True

    def reset_all_stats(self):
        """Initilalize statistics that can change during the game"""

        # Reset the amount of ships left
        self.ships_left = self.settings.ship_limit

        # Reset the ships health
        self.ship_health = self.settings.ship_max_health

        # Initialize score message and set the score to zero
        self.score_txt = 'XP: '
        self.score = 0

        # Initialize level message and set the level to one
        self.level_txt = 'LEVEL: '
        self.level = 1

    def get_high_score(self):
        """open txt file to get the highest score"""

        try:
            with open(self.high_score_file) as f:
                scores = f.readlines()
        except FileNotFoundError:
            self.high_score = 0
        else:
            self.high_score = max(int(score) for score in scores)

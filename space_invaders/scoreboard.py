# SCOREBOARD MODULE

import pygame
from ship import Ship


class Scoreboard():
    """Class to manage scoring information"""

    def __init__(self, si_game):
        """initialize scoreboard attributes"""

        # Create attribute of whole space_invaders
        self.si_game = si_game

        # si_game is feeding Scoreboard all of SpaceInvaders, we set a
        # Scoreboard.screen attribute equal to the SpaceInvaders screen
        self.screen = si_game.screen

        # Get screen rectangle attributes
        self.screen_rect = self.screen.get_rect()

        # Import Ship
        self.ship = si_game.ship

        # Import space_invaders settings
        self.settings = si_game.settings

        # Import space_invaders stats
        self.stats = si_game.stats

        # Import font and colour settings
        self.score_text = self.settings.score_font_colour
        # self.high_score_text = self.settings.hscore_font_colour
        self.font = self.settings.scoreboard_font

        # Prepare score images
        self.prep_score()
        # self.prep_high_score()
        self.prep_ship_lives()

        # Prepare level
        self.prep_level()

    def prep_score(self):
        """Turn score into rendered image"""

        # Local variable to round score in nearest 10's
        rounded_score = round(self.stats.score, -1)

        # Local variable set to store the score formatted with commas
        score_str = "{:,}".format(rounded_score)

        # Initialize an attribute which renders score as an image
        self.score_image = self.font.render(f"{self.stats.score_txt}" 
                                            f"{score_str}", True,
                                            self.score_text)

        # Display score at top left of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.settings.score_loc_x
        self.score_rect.top = self.settings.score_loc_y

    def prep_high_score(self):
        """Turn high score into rendered image"""

        # Local variable to round score in nearest 10's
        high_score = round(self.stats.high_score, -1)

        # Local variable set to store the high score formatted with commas
        score_str = "{:,}".format(high_score)

        # Initialize an attribute which renders high score as an image
        self.high_score_image = self.font.render(score_str, True,
                                                 self.high_score_text)

        # Display score at top centre of the screen
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.settings.score_loc_y

    def prep_level(self):
        """Turn level into rendered image"""

        # Local variable to round score in nearest 10's
        level = str(self.stats.level)

        # Initialize an attribute which renders score as an image
        self.level_image = self.font.render(f"{self.stats.level_txt}"
                                            f"{level}", True,
                                            self.score_text)

        # Display score at top left of the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 225
        self.level_rect.top = self.settings.score_loc_y

    def level_up(self):
        """Increment level by 1 when fleet cleared"""

        self.stats.level += 1

    def show_score(self):
        """Blit scores, level and ship lives to screen"""

        # Blit method takes in parameters that we set in prep
        self.screen.blit(self.score_image, self.score_rect)
        # self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check if new high score set when not space_invaders active"""

        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_ship_lives(self):
        """Add number of lives to sprite group"""

        self.ships = pygame.sprite.Group()

        for ship in range(self.stats.ships_left+1):
            # Create instance of Ship
            ship_life = Ship(self.si_game)

            # Set ship attributes to display lives
            ship_life.image = pygame.transform.scale(
                ship_life.image, (32, 32))

            # Set ship lives display position
            ship_life.rect.x = self.settings.screen_width - (50*ship)
            ship_life.rect.top = 15

            self.ships.add(ship_life)

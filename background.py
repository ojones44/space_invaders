# CLASS FOR THE BACKGROUND

import pygame


class Background:
    """Store and manage background"""

    def __init__(self, si_game):
        """Initialize the backgrounds data"""

        # si_game is feeding Ship all of SpaceInvaders, we set a bg.screen
        # attribute equal to the SpaceInvaders screen
        self.screen = si_game.screen

        # Import settings
        self.settings = si_game.settings

        # Assign image to attribute and get its rect
        self.image = pygame.image.load('images\\bg.jpg')
        self.scale_bg = pygame.transform.scale(
                self.image, (self.settings.screen_width,
                             self.settings.screen_height))
        self.rect = self.image.get_rect()

    def blitme(self):
        """Draw background to screen"""

        # Blit image to screen, passing it parameters we set
        self.screen.blit(self.scale_bg, (0, 0))

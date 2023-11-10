# SHIP BULLET MODULE

import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class to manage bullet behaviour"""

    def __init__(self, si_game):
        """Initialize the bullet data at ships current position"""
        super().__init__()

        # si_game is feeding Bullet all of SpaceInvaders, we set a
        # Bullet.screen attribute equal to the SpaceInvaders screen
        self.screen = si_game.screen

        # Import space_invaders settings
        self.settings = si_game.settings

        # Create colour attribute
        self.colour = self.settings.bullet_colour

        # Create bullet at X0Y0, then set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = si_game.ship.rect.midtop

        # Store the bullet position as a decimal
        self.y = float(self.rect.y)

    def update(self):
        """Fire bullet up the screen"""

        # Important: in the main program when the sprite update is called,
        # it will automatically call all update methods for each sprite
        # in the group. Therefore, this method will be called

        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed

        # Update rect position
        self.rect.y = self.y

    def drawme(self):
        """Draw bullet to screen"""

        # Draw bullet to screen feeding it parameters we set
        pygame.draw.rect(self.screen, self.colour, self.rect)

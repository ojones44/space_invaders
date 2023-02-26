# ALIEN BULLET MODULE

import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    """Class to manage bullet behaviour"""

    def __init__(self, si_game, x, y):
        """Initialize the bullet data at ships current position"""
        super().__init__()

        # si_game is feeding Bullet all of SpaceInvaders, we set a
        # Bullet.screen attribute equal to the SpaceInvaders screen
        self.screen = si_game.screen

        # Import game settings
        self.settings = si_game.settings

        # Store alien Sprite group from Main
        self.aliens = si_game.aliens

        # Create colour attribute
        self.colour = self.settings.a_bullet_colour

        # Create bullet using fed in x and y positions
        self.rect = pygame.Rect(x, y, self.settings.a_bullet_width,
                                self.settings.a_bullet_height)

        # Store the bullet position as a decimal
        self.y = float(self.rect.y)

    def update(self):
        """Fire bullet down the screen"""

        # Important: in the main program when the sprite update is called,
        # it will automatically call all update methods for each sprite
        # in the group. Therefore, this method will be called

        # Update the decimal position of the bullet
        self.y += self.settings.a_bullet_speed

        # Update rect position
        self.rect.y = self.y

    def drawme(self):
        """Draw alien bullet to screen"""

        # Draw rectangle functions takes in parameters we've set
        pygame.draw.rect(self.screen, self.colour, self.rect)

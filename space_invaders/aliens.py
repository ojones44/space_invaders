# ALIENS MODULE

import pygame
from pygame.sprite import Sprite
import random


class Alien(Sprite):
    """Class to manage alien fleet and behaviours"""

    def __init__(self, si_game):
        """Initialize alien attributes"""
        super().__init__()

        # si_game is feeding Alien all of SpaceInvaders, we set an
        # Alien.screen attribute equal to the SpaceInvaders screen
        self.screen = si_game.screen

        # Import settings into Alien class from Main
        self.settings = si_game.settings

        # Import ship for movement flag reference
        self.ship = si_game.ship

        # Import screen width for positioning calculations
        self.screen_width = self.settings.screen_width
        self.screen_height = self.settings.screen_height

        # Then use self.screen to get the rectangle shape
        self.screen_rect = si_game.screen.get_rect()

        # Load the alien images at random and get its rect.
        self.images = [self.settings.IMAGE_PATH + 'a1.png',
                       self.settings.IMAGE_PATH + 'a2.png',
                       self.settings.IMAGE_PATH + 'a3.png',
                       self.settings.IMAGE_PATH + 'a4.png',
                       self.settings.IMAGE_PATH + 'a5.png',
                       self.settings.IMAGE_PATH + 'a6.png',
                       self.settings.IMAGE_PATH + 'a7.png',
                       self.settings.IMAGE_PATH + 'a1.png',
                       ]

        self.image = pygame.image.load(random.choice(self.images))
        self.rect = self.image.get_rect()

        # Start first alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the first alien's exact horizontal position
        self.x = float(self.rect.x)

        # Store alien Sprite group from Main
        self.aliens = si_game.aliens

    def update(self):
        """Move aliens left and right"""

        # Important: in the main program when the sprite update is called,
        # it will automatically call all update methods for each sprite
        # in the group. Therefore, this method will be called

        if not self.ship.moving_up:
            # Update the decimal position of the fleet
            self.x += (self.settings.alien_speed *
                       self.settings.fleet_direction)
        else:
            # If using kamikaze, alien speed is reduced
            self.x += (self.settings.k_alien_speed *
                       self.settings.fleet_direction)

        # Update rect position with float number
        self.rect.x = self.x

    def check_edges(self):
        """Return True if an alien is at the edge of the screen"""

        # Assign screen rectangle attribute to a variable
        screen_rect = self.screen.get_rect()

        # Check if the edge of any aliens are at either edge of screen
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

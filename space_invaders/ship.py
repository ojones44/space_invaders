# CLASS FOR THE SPACESHIP

import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Store and manage all data for the spaceship"""

    def __init__(self, si_game):
        """Initialize the ships data"""

        # Inherit from Sprite
        super().__init__()

        # si_game is feeding Ship all of SpaceInvaders, we set a Ship.screen
        # attribute equal to the SpaceInvaders screen
        self.screen = si_game.screen

        # Import space_invaders settings
        self.settings = si_game.settings

        # Import stats
        self.stats = si_game.stats

        # Then use self.screen to get the rectangle shape
        self.screen_rect = si_game.screen.get_rect()

        # Load the ship image and get its rect - then update mask
        self.image = pygame.image.load(self.settings.IMAGE_PATH + "ship.png")
        self.rect = self.image.get_rect()

        # Define top of rect for Kamikaze move
        self.top = self.rect.top

        # Start each new ship at the bottom center of the screen
        # This is responsive to the pygame window
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.settings.screen_height - \
            self.settings.ship_pos

        # Store a decimal value for the ships positions
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Combo check for Kamikaze
        self.collision_list = []
        self.combo_list = []

        # Boolean flags
        self.moving_r = False
        self.moving_l = False
        self.moving_up = False
        self.kamikaze_active = False
        self.ship_hit = False
        self.all_aliens_eliminated = False
        self.health_hit = False

    def update_move(self):
        """Update the ships X position based on key presses"""

        # Increment ship image by speed defined in Setting class
        if not self.moving_up and self.moving_r and self.rect.right < \
                self.screen_rect.right:
            self.x += self.settings.ship_speed
        if not self.moving_up and self.moving_l and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from new x position
        self.rect.x = self.x

    def kamikaze(self):
        """Update ships Y position for kamikaze"""

        if self.moving_up:
            # Increment ship upwards whilst decreasing speed every iteration
            self.y -= self.settings.k_spd
            self.settings.k_spd -= self.settings.k_spd_inc

            # Update rect object from new y position through each iteration
            self.rect.y = self.y

        if self.rect.bottom >= self.settings.screen_height - \
                self.settings.ship_pos:
            # If Kamikaze is finished, reset all related attributes
            self.moving_up = False
            self.kamikaze_active = False
            self.settings.k_spd = self.settings.kamikaze_abs_speed
            self.rect.y = self.y

    def ship_centre(self):
        """Centre the ship on the space_invaders screen when a life is lost"""

        # Ship rectangle centre bottom is being put in screen middle bottom
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.settings.screen_height - \
            self.settings.ship_pos

        # Reset exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the ship at its current location"""

        # Put the ship image onto the screen, passing the image and rectangle
        self.screen.blit(self.image, self.rect)

    def draw_health_bar(self):
        """Blit full health bar to screen"""

        # Draw red health bar to screen
        pygame.draw.rect(self.screen, self.settings.segment_colour, (self.rect.x,
                         self.rect.bottom, self.rect.width,
                         self.settings.bar_height))

        # If health is still greater than 0, then draw green rectangle onto
        # screen over the red one which is constantly displayed.

        # We pass in the screen, bar colour, current ship position, bar height
        # and a calculation which works out how long to make the green bar
        # based on how much ship health is left, then multiplies our ship.rectx
        # by that percentage figure
        if self.stats.ship_health > 0:
            pygame.draw.rect(self.screen, self.settings.bar_colour,
                             (self.rect.x,
                              self.rect.bottom,
                              int(self.rect.width * (
                                  self.stats.ship_health /
                                  self.settings.ship_max_health)),
                              self.settings.bar_height))

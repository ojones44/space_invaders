# BUTTONS MODULE

import pygame.font


class GameStartButton:
    """Class to generate game buttons"""

    def __init__(self, si_game):
        """Initialize button attributes"""

        # si_game is feeding Button all of SpaceInvaders, we set a
        # Button.screen attribute equal to the SpaceInvaders screen
        self.screen = si_game.screen

        # Get screen rectangle
        self.screen_rect = self.screen.get_rect()

        # Import settings
        self.settings = si_game.settings

        # Import font settings
        self.button_font = self.settings.button_font
        self.countdown_font = self.settings.countdown_font

        # Build button rect object and center it
        self.rect = pygame.Rect(0, 0, self.settings.button_width,
                                self.settings.button_height)
        self.rect.center = self.screen_rect.center

        # Set a copy of settings countdown to use and adjust separately
        self.countdown = self.settings.countdown

        # Define a blank attribute which we start ticking only when
        # play button has been pressed in main game file
        self.last_count = None

        # The button message needs to be prepped only once
        self.msg = "I'M READY"
        self._prep_msg(self)

        # Boolean flags
        self.waiting = True

    def _prep_msg(self, msg):
        """Turn message into rendered image and center on the button"""

        # Render stored message as an image into a variable
        # Using the font.render() method
        self.msg_image = self.button_font.render(self.msg, True,
                                                 self.settings.text_colour,
                                                 self.settings.button_colour)

        # Store generated image rect into a variable
        self.msg_image_rect = self.msg_image.get_rect()

        # Centre of the msg image rectangle will match the button center
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Blit complete button to screen"""

        # Draw a blank button
        self.screen.fill(self.settings.button_colour, self.rect)

        # Draw message onto button
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def blit_countdown(self):
        """Blit countdown to screen"""

        # Set local variable, and past it the render method
        # for our countdown value which is adjusted through each
        # iteration of the game loop once the play button has been pressed
        count = self.countdown_font.render(
            str(self.countdown), True,
            self.settings.countdown_colour)

        # Store generated image rect into a variable
        count_rect = count.get_rect()

        # Centre of the msg image rectangle will match the button center
        count_rect.center = self.rect.center

        # Draw message onto button
        self.screen.blit(count, count_rect)

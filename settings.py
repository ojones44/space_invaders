# SETTINGS MODULE

import pygame.font


class Settings:
    """A class to store all settings for the game"""

    def __init__(self):
        """Initialize the game's static settings"""

        self.initialize_dynamic_settings()

        # -------------------------- #

        # Time delay / FPS
        self.fps = 120

        # -------------------------- #

        # Colours
        self.RED = (255, 0, 0)
        self.GREEN = (0, 175, 0)
        self.DARKBLUE = (0, 70, 250)
        self.YELLOW = (255, 255, 0)
        self.MAGENTA = (255, 0, 255)
        self.CYAN = (0, 255, 255)
        self.BLACK = (25, 25, 25)
        self.GRAY = (150, 150, 150)
        self.WHITE = (255, 255, 255)

        # -------------------------- #

        # Screen settings
        self.screen_width = 1000
        self.screen_height = 750

        # -------------------------- #

        # Sleep settings
        self.game_end_pause = 0.2
        self.reset_timer = 3
        self.countdown = 5

        # -------------------------- #

        # Ship settings
        self.ship_max_health = 100
        self.ship_limit = 3

        # -------------------------- #

        # Alien settings
        self.alien_drop_speed = 5
        self.alien_spacing_y = 50

        # -------------------------- #

        # Ship Bullet settings
        self.bullet_speed = 3
        self.bullet_height = 15
        self.bullet_width = 5
        self.bullet_colour = self.GREEN
        self.bullets_allowed = 3

        # -------------------------- #

        # Alien Bullet settings
        self.a_bullet_height = 8
        self.a_bullet_width = 8
        self.a_bullet_colour = self.DARKBLUE
        self.a_bullets_allowed = 5
        self.a_bullet_dynamic = self.a_bullets_allowed
        self.a_bullet_damage = 25

        # -------------------------- #

        # Ship special kamikaze move
        self.k_spd_inc = 0.16
        self.kamikaze_abs_speed = 14
        self.k_spd = self.kamikaze_abs_speed
        self.k_alien_speed = self.alien_speed / 2

        # -------------------------- #

        # Play button settings
        self.button_width = 250
        self.button_height = 75
        self.button_colour = self.BLACK
        self.text_colour = self.WHITE
        self.button_font = pygame.font.SysFont("arialrounded", 30)

        # -------------------------- #

        # Countdown settings
        self.countdown_font = pygame.font.SysFont("arialrounded", 250)
        self.countdown_colour = self.WHITE

        # -------------------------- #

        # Health bar settings
        self.bar_height = 15
        self.ship_pos = self.bar_height + 5
        self.bar_colour = self.GREEN
        self.segment_colour = self.RED

        # -------------------------- #

        # Scoreboard settings
        self.scoreboard_font = pygame.font.SysFont("bahnschrift", 30)
        self.score_font_colour = self.GRAY
        self.hscore_font_colour = self.GREEN
        self.score_loc_x = 20
        self.score_loc_y = 10

        # -------------------------- #

        # Points system

        # Ship bullet hitting alien
        self.bullet_alien_points = 50
        # Kamikaze points per alien
        self.ship_alien_points = 100
        # Alien bullet hitting ship deduction
        self.alien_bullet_points = 25
        # Alien hitting ship deduction
        self.alien_ship_points = 150

        # -------------------------- #

        # Flags
        self.alien_hit_bottom = False
        self.sleeping = True

        # -------------------------- #

        # Amount to speed settings up by through each level
        self.speedup_scale = 1.2

        # -------------------------- #

        # Amount to speed up alien when 1 left in fleet
        self.speedup_1_left = 2.5
        self.sped_up = False

    def initialize_dynamic_settings(self):
        """Initialize settings that increase when levelling up"""

        # Store dynamic settings here, so they can be reset any time
        self.ship_speed = 1.5
        self.alien_speed = 0.55
        self.a_bullet_speed = 1

        # 1 = Moving right, -1 = Moving left
        self.fleet_direction = 1

    def increase_speed(self):
        """Increase speed of game by specified scale"""

        # Increase the dynamic settings by the speedup scale
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.a_bullet_speed *= self.speedup_scale

    def one_alien_left(self):
        """Increase alien speed when only 1 left in fleet"""

        # If there's one alien left, speed up alien speed and drop speed
        self.alien_speed *= self.speedup_1_left
        self.alien_drop_speed *= self.speedup_1_left
        self.sped_up = True

    def reset_current_alien_speed(self):
        """Reset alien speed to what it was at after last alien defeated"""

        # Once last alien is defeated, reset back to speed that was running
        self.alien_speed /= self.speedup_1_left
        self.alien_drop_speed /= self.speedup_1_left
        self.sped_up = False

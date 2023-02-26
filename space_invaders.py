# All images provided by www.flaticon.com (Smashicon and Freepik)

# Library imports (sys used for exiting the game)
import sys
from time import sleep
import pygame
import random

# Module imports
from settings import Settings
from game_stats import GameStats
from background import Background
from ship import Ship
from bullet import Bullet
from alien_bullet import AlienBullet
from aliens import Alien
from game_start_button import GameStartButton
from scoreboard import Scoreboard


class SpaceInvaders:
    """Overall class to manage game assets"""

    def __init__(self):
        """Initialize the whole game"""

        # method for pygame needed to initialize its background settings
        pygame.init()

        # Set a frame rate
        self.clock = pygame.time.Clock()

        # Create instance of settings so methods can be used in this file
        self.settings = Settings()

        # Set pygame window size as an attribute, and give the window a name
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Space Invaders")

        # Create instance of GameStats to store statistics
        self.stats = GameStats(self)

        # Create instance of Ship. Feeding self parameter basically means
        # we're passing the current class we're in over to Ship
        self.ship = Ship(self)

        # Create sprite group for bullets
        self.bullets = pygame.sprite.Group()

        # Create sprite group for alien bullets
        self.alien_bullets = pygame.sprite.Group()

        # Create sprite group for aliens and load fleet once
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Create instance of Background
        self.bg = Background(self)

        # Generate play button
        self.play = GameStartButton(self)

        # Create instance of scoreboard
        self.score = Scoreboard(self)

    def run_game(self):
        """Start the main loop for game"""

        while True:

            # Limit Python to a frame rate. Without this, Python tries to run
            # the game as fast as possible, and also speeds up when files get
            # deleted. This keeps it the same speed
            self.clock.tick(self.settings.fps)

            # Check menu events needs to be outside game_active
            # So we can still detect a user quitting
            if not self.stats.game_active:
                self._check_menu_events()

            # While game is active, run these methods
            if self.stats.game_active:
                self._check_events()
                self.ship.update_move()
                self.ship.kamikaze()
                self._update_bullets()
                self._update_alien_bullets()
                self._update_kamikaze()
                self._update_aliens()

            # The update screen also needs to be outside of game_active
            # This is for menu activity
            self._update_screen()

    def _check_menu_events(self):
        """Respond to any menu activity when game not active"""

        # Loop through events and respond to user keyboard inputs
        for event in pygame.event.get():
            # If red cross is clicked with mouse, game closes
            if event.type == pygame.QUIT:
                self.store_high_score()
                sys.exit()

            # If mouse button is clicked anywhere in the play button,
            # then store position and call method
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_events(self):
        """Respond to key press and mouse events"""

        # Loop through events and respond to user keyboard inputs
        for event in pygame.event.get():
            # If red cross is clicked with mouse, game closes
            if event.type == pygame.QUIT:
                self.store_high_score()
                sys.exit()

            # If a key is pressed down, call keydown events method
            if event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            # If a key is released, call keyup events method
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            # Quit game if 'q' is pressed
            elif event.type == pygame.K_q:
                self.store_high_score()
                sys.exit()

    def _check_keydown_events(self, event):
        """Respond to key down events"""

        if event.key == pygame.K_RIGHT:
            # Move right flag set to true
            self.ship.moving_r = True

        elif event.key == pygame.K_LEFT:
            # Move left flag set to true
            self.ship.moving_l = True

        elif event.key == pygame.K_UP:
            # and self.ship.kamikaze_active:
            # Move up flag set to true
            self.ship.moving_up = True

        elif event.key == pygame.K_SPACE:
            # Call fire bullet method if space is pressed
            self._fire_bullet()

        elif event.key == pygame.K_q:
            self.store_high_score()
            # Quit game if 'q' is pressed
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key release events"""

        if event.key == pygame.K_RIGHT:
            # Move right flag set to false
            self.ship.moving_r = False

        elif event.key == pygame.K_LEFT:
            # Move left flag set to false
            self.ship.moving_l = False

    def _check_play_button(self, mouse_pos):
        """Check if mouse has been clicked anywhere on play button"""

        # The reason I have coded the play button with an if statement is
        # because I didn't want to call _create_fleet every time. As I'm using
        # random images, they'll keep changing before the game has even started

        # Store a variable of True or False based on whether the mouse has been
        # clicked over the play button rectangle
        button_clicked = self.play.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active and \
                self.stats.first_run:
            # Reset the dynamic settings
            self.settings.initialize_dynamic_settings()

            # Set the waiting for button to be clicked flag to False
            self.play.waiting = False

            # Start the count timer for countdown, only once button clicked
            self.play.last_count = pygame.time.get_ticks()

            # Play button will remove and set new game
            self._update_screen()

            # Make cursor invisible only in pygame window
            pygame.mouse.set_visible(False)

        elif button_clicked and not self.stats.game_active and \
                not self.stats.first_run:

            # Reset the dynamic settings
            self.settings.initialize_dynamic_settings()

            # Set the waiting for button to be clicked flag to False
            self.play.waiting = False

            # Start the count timer for countdown, only once button clicked
            self.play.last_count = pygame.time.get_ticks()

            # Restart game
            self._restart_game()

            # Make cursor invisible only in pygame window
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create new bullet and add to bullet sprite group"""

        # Check if bullet is allowed
        if not self.ship.moving_up and len(self.bullets) < \
                self.settings.bullets_allowed:
            # Create instance of Bullet and add to sprite group
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullet position and delete once off the screen"""

        # This will call class Bullet.update() via the sprite group
        self.bullets.update()

        # Delete bullets once off of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Call detect collision method to see if there is a hit
        self._detect_bullet_alien_collisions()

        # Call detect bullet on bullet collision to remove if True
        self._detect_bullet_on_bullet_collision()

    def _detect_bullet_alien_collisions(self):
        """Detect if ship bullet has hit an alien"""

        # Detect bullet collision with aliens, remove both if True
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)
        if collisions:
            for aliens in collisions.values():
                # If the collision returns True, then score is adjusted
                self.stats.score += self.settings.bullet_alien_points * \
                                    len(aliens)
            # Prep score is called to update the score being printed to screen
            self.score.prep_score()

        # Check if alien sprite group has 1 left and hasn't been sped up
        if len(self.aliens) == 1 and not self.settings.sped_up:
            # Increase last alien speed
            self.settings.one_alien_left()

        # Check if all aliens are defeated to start new game/level
        elif len(self.aliens) == 0:
            if self.settings.sped_up:
                # Reset alien speed to current speed
                self.settings.reset_current_alien_speed()

            # start new level
            self._new_level()

            # Increase difficulty
            self.settings.increase_speed()

            # Start the count timer for countdown, only once button clicked
            self.play.last_count = pygame.time.get_ticks()

    def _detect_bullet_on_bullet_collision(self):
        """Detect if a ship bullet collided with an alien bullet"""

        # Remove ship bullet if they collide with alien bullet.
        # Alien bullet cannot be defeated
        pygame.sprite.groupcollide(self.bullets, self.alien_bullets, True,
                                   False)

    def _update_alien_bullets(self):
        """Fire alien bullet, update pos and delete once off the screen"""

        # Check if bullet is allowed
        if len(self.alien_bullets) < self.settings.a_bullets_allowed and \
                len(self.aliens) > 0:
            # Assign a random alien from the sprite group to variable
            attack = random.choice(self.aliens.sprites())

            # Create instance of alien bullet and feed in the x and y
            # positions of the current selected random alien
            new_alien_bullet = AlienBullet(self, attack.rect.centerx,
                                           attack.rect.bottom)

            # Add alien bullet instance to sprite group
            self.alien_bullets.add(new_alien_bullet)

        # This will call class AlienBullet.update() via the sprite group
        # to move the bullet down the screen
        self.alien_bullets.update()

        # Call to see if an alien bullet has hit the ship at any point
        self._detect_bullet_ship_collisions()

        # Also call to see if an alien has hit the ship at any point
        self._detect_alien_ship_collisions()

    def _detect_bullet_ship_collisions(self):
        """Detect collisions of alien bullet on ship"""

        # Loop through a copy of the bullet sprite group
        for bullet in self.alien_bullets.copy():

            # Look for an alien bullet hitting ship, and remove bullet
            if pygame.sprite.spritecollide(self.ship, self.alien_bullets,
                                           True):
                # If we're not in Kamikaze mode, then call relevant method
                if not self.ship.moving_up:
                    self._ship_hit_by_bullet()
                    # Also update score, and then prep to blit updated score
                    self.stats.score -= self.settings.alien_bullet_points
                    self.score.prep_score()

            # Delete bullets once rect.bottom hits screen bottom
            elif bullet.rect.bottom >= self.settings.screen_height:
                self.alien_bullets.remove(bullet)

    def _detect_alien_ship_collisions(self):
        """Detect collisions of alien on ship"""

        # Detect alien collision on ship, reset game if true
        if pygame.sprite.spritecollideany(self.ship, self.alien_bullets):
            if self.settings.sped_up:
                # Reset alien speed to current speed if last alien touched ship
                self.settings.reset_current_alien_speed()
            # Update score accordingly, and prep to blit new score to screen
            self.stats.score -= self.settings.alien_ship_points
            self.score.prep_score()
            # Call relevant method
            self._ship_hit_by_alien()

    def _check_aliens_bottom(self):
        """End/restart game if aliens reach the bottom off the screen"""

        # Loops through aliens group and see if any have hit the screen bottom
        for alien in self.aliens.sprites():
            # If any have, then call relevant method to reset game
            if alien.rect.bottom >= self.settings.screen_height:
                self._aliens_reached_bottom()

    def _update_kamikaze(self):
        """Detect collision between ship and alien"""

        # Detect collision between a sprite and a group, True = kill alien
        if pygame.sprite.spritecollide(self.ship, self.aliens, True):
            # Update score accordingly, and prep to blit new score to screen
            self.stats.score += self.settings.ship_alien_points
            self.score.prep_score()

    def _update_aliens(self):
        """Run the alien update to move them"""

        # Check if fleet direction needs modifying
        self._update_fleet_edges()

        # This will call class Alien.update() via the sprite group
        # in order to keep them moving through each iteration
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # If we're not in Kamikaze mode, then call _ship_hit()
            if not self.ship.moving_up:
                self._ship_hit_by_alien()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit_by_alien(self):
        """Reset game and reduce ship lives when hit"""

        # Set ship_hit flag to True
        self.ship.ship_hit = True

        # If on last alien, reset speed before restarting level
        if self.settings.sped_up:
            self.settings.reset_current_alien_speed()

        if self.stats.ships_left > 1:
            # Decrement ships left
            self.stats.ships_left -= 1
            self.score.prep_ship_lives()

            # Reset health only
            self.stats.ship_health = self.settings.ship_max_health

            # Reset game
            self._reset_game()
        else:
            # End game, and set waiting flag to true, and make mouse visible
            self.store_high_score()
            self.stats.game_active = False
            self.play.waiting = True
            pygame.mouse.set_visible(True)

    def _ship_hit_by_bullet(self):
        """Reset game and reduce ship lives when hit"""

        # Decrement ships health
        self.stats.ship_health -= self.settings.a_bullet_damage

        if self.stats.ship_health == 0:
            if self.stats.ships_left > 1:
                # Decrement ships left
                self.stats.ships_left -= 1
                self.score.prep_ship_lives()

                # Set ship_hit flag to True
                self.ship.ship_hit = True

                # Reset health only
                self.stats.ship_health = self.settings.ship_max_health

                # If on last alien, reset speed before restarting level
                if self.settings.sped_up:
                    self.settings.reset_current_alien_speed()

                # Reset game
                self._reset_game()
            else:
                # End game, and set waiting flag to true, 
                # and make mouse visible
                self.store_high_score()
                self.stats.game_active = False
                self.play.waiting = True
                pygame.mouse.set_visible(True)

    def _aliens_reached_bottom(self):
        """Reset game and reduce ship lives when aliens reach bottom"""

        # Set alien_hit_bottom flag to True
        self.settings.alien_hit_bottom = True

        # If on last alien, reset speed before restarting level
        if self.settings.sped_up:
            self.settings.reset_current_alien_speed()

        if self.stats.ships_left > 1:
            # Decrement ships left
            self.stats.ships_left -= 1
            self.score.prep_ship_lives()

            # Reset health only
            self.stats.ship_health = self.settings.ship_max_health

            # Reset game
            self._reset_game()
        else:
            # End game, and set waiting flag to true, and make mouse visible
            self.store_high_score()
            self.stats.game_active = False
            self.play.waiting = True
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Calculate and print alien fleet onto defined screen size"""

        # Create alien - purely for calculating purposes
        alien = Alien(self)

        # Unpack size tuple
        alien_w, alien_h = alien.rect.size

        # Calculate number of aliens possible in available x + y space
        available_space_x = self.settings.screen_width - (alien_w * 2)
        available_space_y = (self.settings.screen_height - (alien_h * 3))

        # Calculate possible number of rows
        num_rows = (available_space_y //
                    (alien_h + self.settings.alien_spacing_y))

        # Calculate number of aliens possible in each row
        num_aliens = available_space_x / (alien_w * 2)
        num_aliens = round(num_aliens)

        # Create full fleet
        for r in range(num_rows):
            # Create a row of aliens in available space
            for a in range(num_aliens):
                # Call create alien method
                self._create_alien(a, r)

    def _create_alien(self, a, r):
        """Create an Alien and place it into the fleet"""

        # Create instance of Alien through each iteration of the loop
        alien = Alien(self)

        # Unpack size tuple
        alien_w, alien_h = alien.rect.size

        # Move X position along by 2 x Width - then multiply by loop iteration
        alien.x = alien_w + 2 * alien_w * a
        alien.rect.x = alien.x

        # Move Y position along by 2 x Height, then multiply by loop iteration
        alien.rect.y = (alien_h +
                        (alien_h + self.settings.alien_spacing_y) * r)

        # Add newly positioned alien to the sprite group
        self.aliens.add(alien)

    def _update_fleet_edges(self):
        """Check if the fleet is at the right or left of screen"""

        # Loop through alien group
        for alien in self.aliens.sprites():
            # See if any aliens are at either screen edge
            if alien.check_edges():
                # If True, call fleet direction change method
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Update fleet direction and drop fleet"""

        # Loop through alien group
        for alien in self.aliens.sprites():
            # Move every individual alien down the screen by the drop speed
            alien.rect.y += self.settings.alien_drop_speed

        # Change direction (not in for loop, as it only needs doing once)
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        """Run the screen updates and flip to the new screen"""

        # If ship has been hit, or aliens have reached the bottom, 
        # or all aliens have been eliminated, then method is called
        if self.ship.ship_hit or self.settings.alien_hit_bottom:
            self._reset_screen_when_life_lost()
        else:
            # Or else, if no flags are true
            # Redraw game during each iteration of the loop
            self.bg.blitme()
            self.ship.blitme()
            self.ship.draw_health_bar()
            self.score.show_score()
            self.aliens.draw(self.screen)

            # bullets.sprites returns a list of all sprites in the group
            for bullet in self.bullets.sprites():
                # Draw bullets through every iteration
                bullet.drawme()

            # alien_bullets.sprites returns a list of all sprites in the group
            for alien_bullet in self.alien_bullets.sprites():
                # Draw alien bullets through every iteration
                alien_bullet.drawme()

            # Draw the play button if game is not yet active
            if self.play.waiting:
                # Draw play button for game start prompt
                self.play.draw_button()

            # Blit countdown if not waiting for button to be clicked
            if not self.play.waiting and not self.stats.game_active:
                if self.play.countdown >= 0:
                    self._countdown()

            # Make the most recently drawn screen visible
            pygame.display.flip()

        # Reset necessary flags
        self.ship.ship_hit = False
        self.settings.alien_hit_bottom = False
        self.ship.all_aliens_eliminated = False

    def store_high_score(self):
        """Method to store high score at various points of game"""

        with open(self.stats.high_score_file, 'a') as f:
            f.write(f"{str(self.stats.score)}\n")

    def _countdown(self):
        """Begin countdown after button is clicked"""

        # Call the blit countdown method
        self.play.blit_countdown()
        # Start a counter
        count_timer = pygame.time.get_ticks()
        # If one second has passed, run statement
        if (count_timer - self.play.last_count) > 1200:
            # Minus 1 from countdown which is set through settings and 
            # game_start
            self.play.countdown -= 1
            # Equal the timers for next iteration
            self.play.last_count = count_timer

        if self.play.countdown == 0:
            # Set relevant flags
            self.stats.game_active = True
            self.stats.first_run = False
            # Reset countdown to figure defined in settings file
            self.play.countdown = self.settings.countdown

    def _reset_screen_when_life_lost(self):
        """Reset screen and pause momentarily after ship looses life"""

        # Redraw game during each iteration of the loop
        self.bg.blitme()
        self.ship.blitme()
        self.ship.draw_health_bar()
        self.score.show_score()

        # Draw aliens to screen
        self.aliens.draw(self.screen)

        # Make the most recently drawn screen visible
        pygame.display.flip()

        # Pause to allow player to get ready
        sleep(self.settings.reset_timer)

    def _new_level(self):
        """ Countdown and start new level if all aliens shot down"""

        # Clear the fleet and any bullets
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        # Create new fleet and re-centre ship
        self._create_fleet()
        self.ship.ship_centre()

        # Increase level
        self.score.level_up()
        self.score.prep_level()
        self.score.prep_ship_lives()

        # Set countdown figure
        self.play.countdown = self.settings.reset_timer

        # Set flags to initiate countdown in update screen
        self.play.waiting = False
        self.stats.game_active = False

    def _reset_game(self):
        """Reset game if ship health depleted or aliens have hit ship"""

        # Clear the fleet and any bullets
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        # Create new fleet and re-centre ship
        self._create_fleet()
        self.ship.ship_centre()

        # Pause momentarily after collision
        sleep(self.settings.game_end_pause)

    def _restart_game(self):
        """Reset new game if lost all lives"""

        # Clear the fleet and any bullets
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()

        # Create new fleet and re-centre ship
        self._create_fleet()
        self.ship.ship_centre()

        # Reset all game_stats
        self.stats.reset_all_stats()
        self.stats.get_high_score()
        self.score.prep_score()
        self.score.prep_level()
        self.score.prep_ship_lives()


if __name__ == '__main__':
    # Make a game instance, then call to run
    si = SpaceInvaders()
    si.run_game()

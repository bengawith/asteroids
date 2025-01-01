import sys
import os
from time import sleep
import pygame
from pathlib import Path

from settings import Settings
from ship import Ship
from bullet import Bullet
from asteroid import Asteroid
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard
from stars import Stars


class Asteroids:
    def __init__(self):
        # Initialising the game and creating resources
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Set to full screen mode or windowed mode for testing
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Asteroids")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.asteroid = pygame.sprite.Group()
        self.stars = Stars(self.screen, self.settings)

        self.game_active = False
        self.start_screen = True

    def main(self):
        """Main game loop."""
        while True:
            # Checking keyboard and mouse events
            self._check_events()

            self._update_screen()
            self.clock.tick(60)

    def _check_collisions(self):
        """Check for any bullets that hit asteroids and remove both."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.asteroids, True, True)
        if collisions:
            for asteroids in collisions.values():    
                self.stats.score += self.settings.asteroid_points * len(asteroids)
                self.alien_hit_sound.play()
                self._check_outer_columns()

            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.asteroids:
            # Destroy existing bullets and create a new fleet
            self.bullets.empty()
            self.settings.increase_speed()
            self.settings.increase_asteroid_speed()
            self.stars.increase_speed(1.2)
            self.sb.check_high_score()

    
    def _ship_hit(self):
        """Respond to ship being hit by alien."""

        self.ship_hit_sound.play()

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Empty bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.centre_ship()

            # Pause
            sleep(1.5)
    
    
    def _start_screen(self):
        """Display the start screen with a translucent overlay."""
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(180)
        overlay.fill(self.settings.bg_colour) 
        self.screen.blit(overlay, (0, 0))

        font_big = pygame.font.Font(self.game_font, 80)
        font_small = pygame.font.Font(self.game_font, 40)
        font_tiny = pygame.font.SysFont(None, 24)

        welcome_text = font_small.render("Welcome to...", True, (255, 255, 255))
        game_title = font_big.render("Asteroids", True, (170, 250, 50))
        instructions_text = font_tiny.render("Press: 'left key' to turn left, 'right key' to turn right, 'up key' to move forwards, 'space' to shoot, 'enter' or click PLAY to start, 'p' to pause, 'q' to quit, 'm' to mute", True, (155, 255, 255))

        welcome_rect = welcome_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 150))
        title_rect = game_title.get_rect(center=self.screen.get_rect().center)
        instructions_rect = instructions_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().bottom - 20))

        self.screen.blit(welcome_text, welcome_rect)
        self.screen.blit(game_title, title_rect)
        self.screen.blit(instructions_text, instructions_rect)

        self.play_button.set_position(self.screen.get_rect().centerx, title_rect.bottom + 50)
        self.play_button.draw_button()
        
    
    def _draw_pause_overlay(self):
        """Draw a translucent overlay and a pause symbol when the game is paused."""
        # Create a translucent grey overlay
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(128)  # Set transparency (0 fully transparent, 255 fully opaque)
        overlay.fill((100, 100, 100))  # Fill with grey color
        self.screen.blit(overlay, (0, 0))

        # Draw pause symbol (e.g., two vertical bars)
        pause_font = pygame.font.Font(self.game_font, 50)
        pause_text = pause_font.render("||", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(pause_text, pause_rect)

    
    def _game_over(self):
        """Display the game over message and the final score."""
        # Stop background music and play game over sound
        pygame.mixer.music.stop()
        self.game_over_sound.play()

        # Create overlay for game over message
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))
        self.screen.blit(overlay, (0, 0))

        game_over_font = pygame.font.Font(self.game_font, 80)
        # Use the font for game over text
        game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.screen.get_rect().centerx, self.screen.get_rect().centery - 100))

        # Display final score in font
        final_score_text = self.settings.pixel_font.render(f"Final Score: {self.stats.score:,}", True, (255, 255, 255))
        final_score_rect = final_score_text.get_rect(center=(self.screen.get_rect().center))

        # Draw the Game Over text and final score
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(final_score_text, final_score_rect)

        # Adjust the "Play Again" button position below the final score
        self.play_button.set_position(self.screen.get_rect().centerx, final_score_rect.bottom + 50)  # Place below score
        self.play_button.draw_button()

    
    def update_screen():
        self.screen.fill(self.settings.bg_colour)
        self.stars.draw_stars()
        pygame.display.flip()

        self.sb.show_score()
        if self.start_screen:
            self._start_screen()
        # Draw play button if game inactive
        if not self.game_active and not self.game_over:
            self.play_button.draw_button()

        # Draw pause overlay
        if self.paused:
            self._draw_pause_overlay()

        if self.game_over:
            self._game_over()

if __name__ == "__main__":
    as = Asteroids()
    as.main()

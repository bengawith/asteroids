import random
import pygame

class Stars:
    def __init__(self, screen, settings):
        """Initialize the star field with random positions."""
        self.screen = screen
        self.settings = settings

        self.star_speed = 1
        # Create the initial stars
        self.stars = self._create_stars()

    def _create_stars(self):
        """Create random star positions across the screen."""
        num_stars = 100  # Number of stars in the background
        stars = []
        for _ in range(num_stars):
            x = random.randint(0, self.settings.screen_width)
            y = random.randint(0, self.settings.screen_height)
            stars.append([x, y])
        return stars

    def update_stars(self):
        """Move the stars down the screen and loop them back to the top."""
        for star in self.stars:
            star[1] += self.star_speed
            # If the star goes off-screen, reset it at the top
            if star[1] > self.settings.screen_height:  
                star[1] = 0
                star[0] = random.randint(0, self.settings.screen_width)

    def draw_stars(self):
        """Draw each star on the screen."""
        for star in self.stars:
            pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(star[0], star[1], 2, 2))
            
    def increase_speed(self, factor):
        """Increase the speed of the stars by a given factor."""
        self.star_speed *= factor

from pathlib import Path
import sys

class GameStats:
    """Track statistics for Space Wars."""
    def __init__(self, game):
        """Initialize statistics."""
        self.sw_game = game
        self.settings = game.settings
        self.stars = game.stars
        self.reset_stats()

        # Determine the correct path for the high_score.txt file
        if hasattr(sys, '_MEIPASS'):
            # If running from the bundled executable
            base_path = Path(sys._MEIPASS)
        else:
            # If running from the script directly
            base_path = Path.cwd()

        # Set the path for high_score.txt
        self.high_score_path = base_path / "asteroids" / 'high_score.txt'

        # Load the high score
        self.high_score = self.read_high_score()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0

    def read_high_score(self):
        """Read high score from file, handling empty or invalid content."""
        try:
            with open(self.high_score_path, "r") as file:
                score = file.read().strip()
                if score:
                    return int(score)
                else:
                    return 0
        except (FileNotFoundError, ValueError):
            return 0
        
    def write_high_score(self):
        """Write the high score to a file."""
        with open(self.high_score_path, "w") as file:
            file.write(str(self.high_score))

    def reset_speeds(self):
        """Reset the asteroid and stars speeds to the current level's speed."""
        current_speed_factor = 1.2**self.level

        # Reset asteroid speed to current level speed
        self.settings.asteroid_speed = current_speed_factor

        # Reset stars speed to match the asteroid speed scaling
        self.stars.star_speed = current_speed_factor

import pygame
from settings import Settings


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

        if getattr(sys, '_MEIPASS', False):
            font_path = os.path.join(sys._MEIPASS, 'fonts', 'PressStart2P-Regular.ttf')
        else:
            font_path = str(next(Path.cwd().rglob('PressStart2P-Regular.ttf'), None))

        self.game_font = font_path



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

def run_game():
    
def update_screen():
    self.screen.fill()
    pygame.display.flip()

if __name__ == "__main__":
    main()

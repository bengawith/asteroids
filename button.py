import pygame.font

class Button:

    def __init__(self, game, msg, width=200, height=50):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = game.settings

        # Set dimensions and properties of the button
        self.width, self.height = width, height
        self.button_color = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.font = self.settings.pixel_font

        # Build the button's rect object and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The message to display on the button
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center  # Center the text inside the button

    def draw_button(self):
        """Draw blank button and then draw message."""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def set_position(self, x, y):
        """Set the button's position and adjust the text position."""
        self.rect.centerx = x
        self.rect.y = y  # Set Y position for the button
        self.msg_image_rect.center = self.rect.center  # Re-center the text after moving the button

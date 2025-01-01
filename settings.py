class Settings:
    def __init__(self):
        # Screen Settings
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_colour = (0,0,51)

        # Ship Settings
        self.ship_limit = 3
    
        # Asteroid Settings
        self.asteroid_min_radius = 20
        self.asteroid_kinds = 3
        self.asteroid_spawn_rate = 0.8  # seconds
        self.asteroid_max_radius = self.asteroid_min_radius * self.asteroid_kinds

        # How quickly the game speeds up
        self.speed_up_scale = 1.2
        self.score_scale = 1.5

        if getattr(sys, '_MEIPASS', False):
            font_path = os.path.join(sys._MEIPASS, 'fonts', 'PressStart2P-Regular.ttf')
        else:
            font_path = str(next(Path.cwd().rglob('PressStart2P-Regular.ttf'), None))
            self.pixel_font = Font(font_path, 28)

        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        # Initialising the settings that can change
        self.ship_speed = 2.5
        self.bullet_speed = 3.0
        self.asteroid_speed = 1.2

        self.asteroid_points = 50

    def increase_speed(self):
        # Increasing the speeds
        self.ship_speed *= self.speed_up_scale
        self.bullet_speed *= self.speed_up_scale

        self.asteroid_points = int(self.asteroid_points * self.score_scale)
    
    def increase_asteroid_speed(self):
        self.asteroid_speed *= self.speed_up_scale

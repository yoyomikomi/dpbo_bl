class Ball:
    def __init__(self, x, y, speed, color, radius, status='out', isCue=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.radius = radius
        self.status = status
        self.isCue = isCue
    
    def update_position(self, dt):
        pass

    def apply_force(self, force, angle):
        pass
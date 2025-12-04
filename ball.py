from physics import Physics

class Ball:
    def __init__(self, x, y, speed, color, radius, status='out', isCue=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.radius = radius
        self.status = status
        self.isCue = isCue

        self.angle = 0
    def update_position(self, dt):
        Physics.simulate_shot (self, dt)

    def apply_force(self, force, angle):
        self.speed = force * 3
        self.angle = angle

    def draw(self, screen, pygame):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
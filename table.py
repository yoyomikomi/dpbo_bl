import math

class Table:
    def __init__(self, width=800, height=400, hole_radius=20, color="green"):
        self.width = width
        self.height = height
        self.hole_radius = hole_radius
        self.color = color

        self.holes = [
            (0, 0),  #t-l
            (width, 0),  #t-r
            (0, height),  #b-;
            (width, height),  #b-r
            (width // 2, 0),  #t-m
            (width // 2, height)  #b-m
        ]


    def draw(self, screen, pygame):
        screen.fill(self.color)

        for hx, hy in self.holes:
            pygame.draw.circle(screen, (0, 0, 0), (hx, hy), self.hole_radius)

    def check_pocket(self, ball):
        for hx, hy in self.holes:
            dist = math.hypot(ball.x - hx, ball.y - hy)
            if dist <= self.hole_radius:
                ball.status = "in"
                ball.speed = 0
                return True   #the ball masuk
        return False

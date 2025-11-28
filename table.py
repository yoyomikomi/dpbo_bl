import math

class Table:
    def __init__(self, width=800, height=400, hole_radius=20, color="green"):
        self.width = width
        self.height = height
        self.hole_radius = hole_radius
        self.color = color

        self.holes = [
            (0, 0),
            (width, 0),
            (0, height),
            (width, height)
        ]

    def check_pocket(self, ball):
        for hx, hy in self.holes:
            dist = math.hypot(ball.x - hx, ball.y - hy)
            if dist <= self.hole_radius:
                return True   #the ball masuk
        return False
    
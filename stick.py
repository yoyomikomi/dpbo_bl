import math

class Stick:
    def __init__(self, x=0, y=0, angle=0, force=0):
        self.x = 0
        self.y = 0
        self.angle = 0
        self.force = 0
    
    def set_angle(self, angle):
        self.angle = angle

    def set_force(self, force):
        self.force = force


    def draw(self, screen, pygame, cue_ball):
        length = 120
        rad = math.radians(self.angle)

        x2 = cue_ball.x - math.cos(rad) * length
        y2 = cue_ball.y - math.sin(rad) * length

        pygame.draw.line(screen, (255, 255, 150), (cue_ball.x, cue_ball.y), (x2, y2), 4)
    
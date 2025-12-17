import math

class Stick:
    def __init__(self, x=0, y=0, angle=0, force=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.force = force
    
    def set_angle(self, angle):
        self.angle = angle

    def set_force(self, force):
        self.force = force


    def draw(self, screen, pygame, cue_ball):
        length = 120
        rad = math.radians(self.angle)

        dx = math.cos(rad)
        dy = math.sin(rad)

        # Pullback distance increases with force
        pullback = self.force * 3

        start_x = cue_ball.x - dx * pullback
        start_y = cue_ball.y - dy * pullback
        end_x = start_x - dx * length
        end_y = start_y - dy * length

        pygame.draw.line(screen, (255, 255, 150), 
                         (start_x, start_y), 
                         (end_x, end_y), 4)
        
        # Draw the tip of the stick for better visibility
        pygame.draw.circle(screen, (200, 200, 100), (int(start_x), int(start_y)), 3)
    
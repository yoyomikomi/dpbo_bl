import pygame
import math
from ball import Ball
from stick import Stick
from table import Table
from physics import Physics
from score import Score

class Game:
    def __init__(self):
        pygame.init()

        self.width = 800
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.table = Table(self.width, self.height, 20, (0, 120, 0))
        self.score = Score()

        # cue ball
        self.balls = [
            Ball(400, 200, 0, "white", 10, status="out", isCue=True),
            Ball(500, 200, 0, "red", 10, status='out'),
            Ball(520, 180, 0, "blue", 10, status='out'),
            Ball(530, 220, 0, "yellow", 10, status='out')]

        self.stick = Stick()

        self.running = True

    def start(self):
        while self.running:
            dt = self.clock.tick(60) / 100.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # shoot the cue ball
                    cue = self.balls[0]
                    self.stick.set_force(10)
                    cue.apply_force(10, self.stick.angle)

            # update stick angle based on mouse
            mx, my = pygame.mouse.get_pos()
            cue = self.balls[0]
            dx = mx - cue.x
            dy = my - cue.y
            self.stick.angle = (math.degrees(math.atan2(dy, dx)))

            # physics update
            for ball in self.balls:
                Physics.bounce(ball, self.table)
                ball.update_position(dt)

                if self.table.check_pocket(ball) and not ball.status == 'out':
                    ball.speed = 0
                    ball.status = 'in'
                    if not ball.isCue:
                        self.score.add(1) 
                        self.balls.remove(ball) # remove ball
                    else:
                        ball.x, ball.y = 400, 200
                        ball.status = 'out'

            # ball-to-ball collision detection and response
            for i in range(len(self.balls)):
                for j in range(i + 1, len(self.balls)):
                    if Physics.ball_collision_check(self.balls[i], self.balls[j], self.balls[i].radius):
                        Physics.collide_balls(self.balls[i], self.balls[j])

            # draw everything
            self.table.draw(self.screen, pygame)
            for ball in self.balls:
                ball.draw(self.screen, pygame)
            self.stick.draw(self.screen, pygame, cue)
            self.score.draw(self.screen, pygame)

            pygame.display.flip()

    def pause(self):
        pass

    def stop(self):
        self.running = False

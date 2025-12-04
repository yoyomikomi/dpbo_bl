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
            Ball(400, 200, 0, "white", 10, status="in", isCue=True),
            Ball(500, 200, 0, "red", 10),
            Ball(520, 180, 0, "blue", 10),
            Ball(530, 220, 0, "yellow", 10)]

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
                ball.update_position(dt)
                Physics.bounce(ball, self.table)

                if self.table.check_pocket(ball):
                    ball.speed = 0
                    ball.x, ball.y = -100, -100  # remove ball
                    self.score.add(1)

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

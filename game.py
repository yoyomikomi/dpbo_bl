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

        self.charge = False

        self.running = True

    def start(self):
        while self.running:
            dt = self.clock.tick(60) / 100.0

            # disable draw stick or act when balls are still moving
            balls_moving = any(abs(ball.speed) > 0.01 for ball in self.balls)

            # update stick angle based on mouse

            if not balls_moving:
                mx, my = pygame.mouse.get_pos()
                cue = self.balls[0]
                dx = mx - cue.x
                dy = my - cue.y
                self.stick.set_angle(math.degrees(math.atan2(dy, dx)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if not balls_moving:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.charge = True
                        self.start_pos = pygame.mouse.get_pos()

                    elif event.type == pygame.MOUSEMOTION and self.charge:
                        mouse_pos = pygame.mouse.get_pos()
                        # identify cue ball
                        cue = self.balls[0]

                        # calculate distance between cue ball and mouse
                        dx = mouse_pos[0] - cue.x
                        dy = mouse_pos[1] - cue.y
                        distance = (dx**2 + dy**2) ** 0.5   # Euclidean distance

                        # scale or clamp the force
                        max_force = 50
                        force = min(distance / 5, max_force)  # divide to control sensitivity

                        self.stick.set_force(force)

                    elif event.type == pygame.MOUSEBUTTONUP and self.charge:
                        cue = self.balls[0]
                        
                        # apply force to cue ball
                        cue.apply_force(self.stick.force, self.stick.angle)
                        self.charge = False
                        self.stick.force = 0

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
            if not balls_moving:
                self.stick.draw(self.screen, pygame, cue)
            self.score.draw(self.screen, pygame)

            pygame.display.flip()

    def pause(self):
        pass

    def stop(self):
        self.running = False

import pygame
import math
from ball import Ball
from stick import Stick
from table import Table
from physics import Physics
from score import Score

class Game:
    def __init__(self):
        self.state = 0  #menu
        pygame.init()

        self.width = 800
        self.height = 400
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.clock = pygame.time.Clock()

        self.table = Table(self.width, self.height, 20, (0, 120, 0))
        self.score = Score()

        # cue ball
        self.balls = []

        cue_ball = Ball(200, self.height//2, 0, "white", 10, status="out", isCue=True)
        self.balls.append(cue_ball)

        # Triangle rack
        start_x = 600     # position of the front ball
        start_y = self.height // 2
        spacing = 22      # slightly bigger than diameter (to prevent overlap)

        colors = ["yellow", "blue", "red", "purple", "orange", "green", "brown",
                "black", "yellow", "blue", "red", "purple", "orange", "green", "brown"]

        index = 0
        rows = 5

        for row in range(rows):
            for col in range(row + 1):
                x = start_x + row * spacing
                y = start_y + (col - row / 2) * spacing
                ball = Ball(x, y, 0, colors[index], 10, status="out")
                self.balls.append(ball)
                index += 1


        self.stick = Stick()

        self.charge = False

        self.running = True

    def start(self):
        start_button = pygame.Rect(self.width//2 - 60, self.height//2 - 30, 120, 60)
        pause_button = pygame.Rect(self.width - 120, 20, 100, 40)
        resume_button = pygame.Rect(self.width//2 - 60, self.height//2 - 80, 120, 60)
        quit_button = pygame.Rect(self.width//2 - 60, self.height//2, 120, 60)

        while self.running:
            dt = self.clock.tick(60) / 100.0
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            cue = self.balls[0]

            if self.state == 0:
                font = pygame.font.SysFont(None, 50)
                title = font.render("BE EL", True, (255,255,255))
                self.screen.blit(title, (self.width//2 - 120, 100))

                if Game.draw_button(self.screen, "START", start_button, pygame, (0,200,0), (0,150,0)):
                    self.state = 1  # switch to PLAYING
                # disable draw stick or act when balls are still moving
            elif self.state == 1:
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
                if Game.draw_button(self.screen, "PAUSE", pause_button, pygame, (200,0,0), (150,0,0)):
                    self.state = 2
            
            elif self.state == 2:
                pause_overlay = pygame.Surface((self.width, self.height))
                pause_overlay.set_alpha(128)
                pause_overlay.fill((0, 0, 0))
                self.screen.blit(pause_overlay, (0, 0))

                if Game.draw_button(self.screen, "RESUME", resume_button, pygame, (0,200,0), (0,150,0)):
                    self.state = 1

                if Game.draw_button(self.screen, "QUIT", quit_button, pygame, (200,0,0), (150,0,0)):
                    self.running = False

            pygame.display.flip()

    def draw_button(screen, text, rect, pygame, hover_color, default_color):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        if rect.collidepoint(mouse):
            pygame.draw.rect(screen, hover_color, rect)
        else:
            pygame.draw.rect(screen, default_color, rect)

        font = pygame.font.SysFont(None, 30)
        label = font.render(text, True, (255,255,255))
        screen.blit(label, (rect.x + 10, rect.y + 10))
        
        if rect.collidepoint(mouse) and click:
            return True
        return False
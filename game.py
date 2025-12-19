import pygame
import math
import os
from ball import Ball
from stick import Stick
from table import Table
from physics import Physics
from score import Score

class Game:
    def __init__(self, state=0):
        self.state = state  #menu
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()

        info = pygame.display.Info()
        self.screen_width, self.screen_height = info.current_w, info.current_h
        self.window_width, self.window_height = self.screen_width-10,self.screen_height-50

        self.original_width = self.window_width
        self.original_height = self.window_height

        self.border = 30
        # self.window_width = 800
        # self.intWidth = self.window_width - 30
        # self.window_height = 400
        # self.intHeight = self.window_height - 30
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.update()

        self.clock = pygame.time.Clock()

        self.table = Table(self.window_width, self.window_width - 30, self.window_height, self.window_height - 30, self.window_height//30, (0, 120, 0))
        self.score = Score()

        # cue ball
        self.balls = []

        cue_ball = Ball(self.window_width // 4, self.window_height//2, 0, "white", self.window_height // 70, status="out", isCue=True)
        self.balls.append(cue_ball)

        #triangle rack
        start_x = self.window_width - (self.window_width // 4)
        start_y = self.window_height // 2
        spacing = 22 

        colors = ["yellow", "blue", "red", "purple", "orange", "green", "brown",
                 "black", "yellow", "blue", "red", "purple", "orange", "green", "brown"
                ]

        index = 0
        rows = 5

        for row in range(rows):
            for col in range(row + 1):
                x = start_x + row * spacing
                y = start_y + (col - row / 2) * spacing
                ball = Ball(x, y, 0, colors[index], self.window_height // 70, status="out")
                self.balls.append(ball)
                index += 1


        self.stick = Stick()

        self.charge = False

        self.running = True

    def start(self):

        start_button = pygame.Rect(self.window_width//2.5, self.window_height//2 - 10, self.window_width//5, self.window_height//10)
        resume_button = pygame.Rect(self.window_width//2.5, self.window_height//2, self.window_width//5, self.window_height//10)
        quit_button = pygame.Rect(self.window_width//2.5, (self.window_height//2 + self.window_height//4), self.window_width//5, self.window_height//10)
        restart_button = pygame.Rect(self.window_width//2.5, self.window_height//4, self.window_width//5, self.window_height//10)
        replay_button = pygame.Rect(self.window_width//2.5, self.window_height//2, self.window_width//5, self.window_height//10)
        pause_surface = pygame.Surface((60, 80), pygame.SRCALPHA)


        # pause button draw
        left_bar = pygame.Rect(10, 10, 8, 30)
        right_bar = pygame.Rect(left_bar.right + 10, 10, 8, 30)

        pygame.draw.rect(
            pause_surface,
            (255, 255, 255, 180),  # alpha included
            left_bar,
            border_radius=4
        )
        pygame.draw.rect(
            pause_surface,
            (255, 255, 255, 180),
            right_bar,
            border_radius=4
        )
        # draw btn surface
        pause_rect = pause_surface.get_rect(topleft=(self.window_width - 120, 20))


        while self.running:
            dt = self.clock.tick(60) / 100.0
            self.screen.fill((0, 0, 0))

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    old_width = self.window_width
                    old_height = self.window_height
                    self.window_width, self.window_height = event.w, event.h
                    scale_x = self.window_width / old_width
                    scale_y = self.window_height / old_height
                    self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    # Update table with new dimensions
                    self.table = Table(self.window_width, self.window_width - 30, self.window_height, self.window_height - 30, self.window_height//30, (0, 120, 0))
                    # Scale ball positions and sizes
                    for ball in self.balls:
                        ball.x *= scale_x
                        ball.y *= scale_y
                        ball.radius = int(ball.radius * scale_y + (self.window_height // 500))
            cue = self.balls[0]

            if self.state == 0:
                font = pygame.font.SysFont('calibri', 50)
                title = font.render("BILIARD GAME", True, (255,255,255))
                play_overlay = pygame.Surface((self.window_width, self.window_height))
                play_overlay.set_alpha(128)
                play_overlay.fill((20, 40, 20))
                self.screen.blit(play_overlay, (0, 0))
                self.screen.blit(title, (self.window_width//2.5, self.window_height//4))

                if Game.draw_button(self.screen, "PLAY", start_button, pygame, (0,200,0), (0,150,0)):
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

                for event in events:
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
                            ball.x, ball.y = self.window_width // 4, self.window_height // 2
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
                if Game.draw_transparent_button(self.screen, pause_surface, pause_rect, pygame):
                    self.state = 2
                
                if len(self.balls) == 1:
                    self.state = 3
            
            elif self.state == 2:
                pause_overlay = pygame.Surface((self.window_width, self.window_height))
                pause_overlay.set_alpha(128)
                pause_overlay.fill((20, 40, 20))
                self.screen.blit(pause_overlay, (0, 0))

                if Game.draw_button(self.screen, "RESUME", resume_button, pygame, (0,200,0), (0,150,0)):
                    self.state = 1

                if Game.draw_button(self.screen, "QUIT", quit_button, pygame, (200,0,0), (150,0,0)):
                    self.running = False

                if Game.draw_button(self.screen, "RESTART", restart_button, pygame, (0, 0, 200), (0, 0, 150)):
                    self.__init__(state=1)

            elif self.state == 3:
                font = pygame.font.SysFont('arial', 50)
                title = font.render("GAME COMPLETED", True, (255,255,255))
                end_overlay = pygame.Surface((self.window_width, self.window_height))
                end_overlay.set_alpha(128)
                end_overlay.fill((50, 20, 40))
                self.screen.blit(end_overlay, (0, 0))
                self.screen.blit(title, (self.window_width//2 - 170, 100))

                if Game.draw_button(self.screen, "PLAY AGAIN", replay_button, pygame, (200, 50, 150), (150, 0, 100)):
                    self.__init__(state=1)

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
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        
        if rect.collidepoint(mouse) and click:
            return True
        return False
    
    def draw_transparent_button(screen, shape, btn, pygame):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        screen.blit(shape, btn)

        if btn.collidepoint(mouse) and click:
            return True
        return False


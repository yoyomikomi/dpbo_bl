import math

class Physics:
    friction = 0.98

    @staticmethod
    def simulate_shot(ball, dt):
        #stop if too slow
        if ball.speed <= 0.01:
            ball.speed = 0
            return

        rad = math.radians(ball.angle)

        #update position
        ball.x += ball.speed * math.cos(rad) * dt
        ball.y += ball.speed * math.sin(rad) * dt

        #for the friction
        ball.speed *= Physics.friction

    @staticmethod
    def bounce(ball, table):
        #left or right wall
        if ball.x - ball.radius < 0 or ball.x + ball.radius > table.width:
            ball.angle = math.pi - ball.angle

        #top or bottom wall
        if ball.y - ball.radius < 0 or ball.y + ball.radius > table.height:
            ball.angle = -ball.angle

        return None

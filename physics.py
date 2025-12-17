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

        #apdet posisi
        ball.x += ball.speed * math.cos(rad) * dt
        ball.y += ball.speed * math.sin(rad) * dt

        #for the friction
        ball.speed *= Physics.friction

    @staticmethod
    def bounce(ball, table):
        bounced = False
        #left/right walls
        if ball.x - ball.radius < table.width - table.interactableWidth:
            ball.x = ball.radius + (table.width - table.interactableWidth)
            ball.angle = 180 - ball.angle
            bounced = True
        elif ball.x + ball.radius > table.interactableWidth:
            ball.x = table.interactableWidth - ball.radius
            ball.angle = 180 - ball.angle
            bounced = True

        #top/bottom walls
        if ball.y - ball.radius < table.height - table.interactableHeight:
            ball.y = ball.radius + (table.height - table.interactableHeight)
            ball.angle = -ball.angle
            bounced = True
        elif ball.y + ball.radius > table.interactableHeight:
            ball.y = table.interactableHeight - ball.radius
            ball.angle = -ball.angle
            bounced = True

        if bounced:
            ball.angle %= 360 

    @staticmethod
    def ball_collision_check(ball1, ball2, ball_radius):
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y

        if math.hypot(dx, dy) > 2 * ball_radius:
            return False
        # Check if at least one ball is moving
        if ball1.speed == 0 and ball2.speed == 0:
            return False
        
        rad1 = math.radians(ball1.angle)
        rad2 = math.radians(ball2.angle)
        vx1 = ball1.speed * math.cos(rad1)
        vy1 = ball1.speed * math.sin(rad1)
        vx2 = ball2.speed * math.cos(rad2)
        vy2 = ball2.speed * math.sin(rad2)
        relative_dot = dx * (vx1 - vx2) + dy * (vy1 - vy2)
        return relative_dot > 0
    
    @staticmethod
    def collide_balls(ball1, ball2, restitution=1.0):
        # Vector from ball1 to ball2
        dx = ball2.x - ball1.x
        dy = ball2.y - ball1.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return  # avoid division by zero

        # Unit vector along collision axis
        nx = dx / dist
        ny = dy / dist

        # Velocities in x/y
        rad1 = math.radians(ball1.angle)
        rad2 = math.radians(ball2.angle)
        vx1 = ball1.speed * math.cos(rad1)
        vy1 = ball1.speed * math.sin(rad1)
        vx2 = ball2.speed * math.cos(rad2)
        vy2 = ball2.speed * math.sin(rad2)

        # Project velocities onto collision axis
        v1_proj = vx1 * nx + vy1 * ny
        v2_proj = vx2 * nx + vy2 * ny

        # Swap projected velocities (equal mass)
        v1_proj_new = v2_proj * restitution
        v2_proj_new = v1_proj * restitution

        # Update velocities
        vx1 += (v1_proj_new - v1_proj) * nx
        vy1 += (v1_proj_new - v1_proj) * ny
        vx2 += (v2_proj_new - v2_proj) * nx
        vy2 += (v2_proj_new - v2_proj) * ny

        # Update speed and angle
        ball1.speed = math.hypot(vx1, vy1)
        ball1.angle = math.degrees(math.atan2(vy1, vx1))
        ball2.speed = math.hypot(vx2, vy2)
        ball2.angle = math.degrees(math.atan2(vy2, vx2))

        # Optional: separate overlapping balls
        overlap = 0.5 * (2 * ball1.radius - dist + 0.1)
        ball1.x -= nx * overlap
        ball1.y -= ny * overlap
        ball2.x += nx * overlap
        ball2.y += ny * overlap

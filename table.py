import math

class Table:
    def __init__(self, width=800, interactableWidth=776, height=400, interactableHeight=376, hole_radius=20, color="green", border= 30):
        self.width = width
        self.height = height
        self.interactableWidth = interactableWidth
        self.interactableHeight = interactableHeight
        self.hole_radius = hole_radius
        self.color = color
        self.border = border
        self.corner_radius = hole_radius + 6
        self.middle_radius = hole_radius

        rail = self.border // 1.25
        w = self.width
        h = self.height

        self.holes = [
            (rail, rail, "corner"),          
            (w - rail, rail, "corner"),     
            (rail, h - rail, "corner"),      
            (w - rail, h - rail, "corner"),  
            (w // 2, rail, "middle"),
            (w // 2, h - rail, "middle")
        ]


    def draw(self, screen, pygame):
        wood = (90, 60, 30)
        felt = (20, 120, 20)
        border = 30

        pygame.draw.rect(
            screen,
            wood,
            (0, 0, self.width, self.height),
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            felt,
            (border, border, self.width - 2*border, self.height - 2*border),
            border_radius=15
        )

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(
            overlay,
            (0, 0, 0, 40),  
            (0, 0, self.width, self.height),
            border_radius=20
        )
        screen.blit(overlay, (0, 0))

        
        for hx, hy, kind in self.holes:

            if kind == "corner":
                radius = self.corner_radius
                rim = (60, 60, 60)
            else:
                radius = self.middle_radius
                rim = (40, 40, 40)

            #outer rim
            pygame.draw.circle(screen, rim, (hx, hy), radius + 4)

            #inner hole
            pygame.draw.circle(screen, (0, 0, 0), (hx, hy), radius)

            #rail-embedded mask for corner pockets
            if kind == "corner":
                mask = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    mask,
                    (0, 0, 0, 255),
                    (radius, radius),
                    radius
                )
                screen.blit(mask, (hx - radius, hy - radius))




    def check_pocket(self, ball):
        for hx, hy, _ in self.holes:
            dist = math.hypot(ball.x - hx, ball.y - hy)
            if dist <= self.hole_radius * 0.9:
                ball.status = "in"
                ball.speed = 0
                return True   #the ball masuk
        return False

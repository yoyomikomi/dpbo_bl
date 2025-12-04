class Score:
    def __init__(self):
        self.score = 0

    def add(self, points):
        self.score += points
        return self.score
    
    def show(self):
        return self.score
    
    def draw(self, screen, pygame):
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))
import pygame

# Initialize pygame
pygame.init()

# Create a simple window
window = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Pygame Test")

# Define colors
GREEN = (0, 180, 0)
WHITE = (255, 255, 255)

# Draw a circle for a few seconds
running = True
clock = pygame.time.Clock()
timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(GREEN)
    pygame.draw.circle(window, WHITE, (300, 200), 50)
    pygame.display.flip()

    clock.tick(60)
    timer += 1
    if timer > 300:  # close automatically after ~5 s
        running = False

pygame.quit()
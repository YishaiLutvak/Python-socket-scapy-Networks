import pygame
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
pygame.init()
size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Game")

WHITE = (255, 255, 255)
screen.fill(WHITE)
pygame.display.flip()

finish = False
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True
pygame.quit()

import pygame

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
FPS = 60


card = pygame.Rect(screen.get_width()//2-50, screen.get_height()//2-50, 100, 100)


while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    pygame.draw.rect(screen, "red", card)

    pygame.draw.rect(screen, "red", card)
    

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
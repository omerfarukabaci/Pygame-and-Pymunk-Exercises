import pygame

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Hello game!')
clock = pygame.time.Clock()

x = 30
y = 30

crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        print(event)

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        y -= 5
    if pressed[pygame.K_DOWN]:
        y += 5
    if pressed[pygame.K_LEFT]:
        x -= 5
    if pressed[pygame.K_RIGHT]:
        x += 5

    gameDisplay.fill((0,0,0))
    pygame.draw.rect(gameDisplay, (0, 128, 255), pygame.Rect(x, y, 60, 60))
    pygame.display.update()
    clock.tick(60)

pygame.quit()

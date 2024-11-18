import pygame

pygame.init()

window_size = (1200, 800)
screen_size = (600, 400)
max_fps = 100

dirt = pygame.image.load('data//dirt.png')

window = pygame.display.set_mode(window_size)
screen = pygame.Surface(screen_size)
clock = pygame.time.Clock()

run = True
while run:
	dt = clock.tick(max_fps)
	screen.fill((0, 0, 100))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	screen.blit(dirt, (0, 0))

	window.blit(pygame.transform.scale(screen, window_size), (0, 0))
	pygame.display.update()
	
pygame.quit()
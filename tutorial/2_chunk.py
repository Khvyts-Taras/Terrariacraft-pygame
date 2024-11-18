import pygame
import random

pygame.init()

max_fps = 100

window_size = (1200, 800)
screen_size = (600, 400)

dirt = pygame.image.load('data//dirt.png')

window = pygame.display.set_mode(window_size)
screen = pygame.Surface(screen_size)
clock = pygame.time.Clock()

class Chunk:
	def __init__(self, x, y, chunk_size, tile_size):
		self.x, self.y = x, y
		self.chunk_size = chunk_size
		self.tile_size = tile_size
		self.surface = pygame.Surface((chunk_size*tile_size, chunk_size*tile_size), pygame.SRCALPHA)
		self.tiles = [[random.randint(0, 1) for x in range(chunk_size)] for y in range(chunk_size)]

	def update_surface(self):
		self.surface.fill((0, 0, 0, 0))
		for y in range(self.chunk_size):
			for x in range(self.chunk_size):
				if self.tiles[y][x] == 1:
					self.surface.blit(dirt, (x*self.tile_size, y*self.tile_size))

	def render(self, screen):
		screen.blit(self.surface, (self.x, self.y))


tile_size = 16
chunk_size = 8

chunk = Chunk(0, 0, chunk_size, tile_size)
chunk.update_surface()

run = True
while run:
	dt = clock.tick(max_fps)
	screen.fill((0, 0, 100))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	chunk.render(screen)

	window.blit(pygame.transform.scale(screen, window_size), (0, 0))
	pygame.display.update()

pygame.quit()
import pygame
import random
import math

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

	def render(self, screen, camera):
		screen.blit(self.surface, (self.x - round(camera.x), self.y - round(camera.y)))


class World:
	def __init__(self, world_size, chunk_size, tile_size):
		self.world_size = world_size
		self.chunk_size = chunk_size
		self.tile_size = tile_size
		self.chunks = [[Chunk(x*chunk_size*tile_size, y*chunk_size*tile_size, chunk_size, tile_size) for x in range(world_size[0])]
																									 for y in range(world_size[1])]
		for y in range(self.world_size[1]):
			for x in range(self.world_size[0]):
				self.chunks[y][x].update_surface()

	def render(self, screen, camera):
		for y in range(self.world_size[1]):
			for x in range(self.world_size[0]):
				self.chunks[y][x].render(screen, camera)


class Camera:
	def __init__(self, x, y):
		self.x, self.y = x, y


tile_size = 16
chunk_size = 8
world = World((4, 3), chunk_size, tile_size)
camera = Camera(-16, -16)
camera_speed = 0.1

run = True
while run:
	dt = clock.tick(max_fps)
	screen.fill((0, 0, 100))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.set_caption(str(round(clock.get_fps())))


	key = pygame.key.get_pressed()
	if key[pygame.K_w]:
		camera.y -= camera_speed*dt
	if key[pygame.K_s]:
		camera.y += camera_speed*dt
	if key[pygame.K_a]:
		camera.x -= camera_speed*dt
	if key[pygame.K_d]:
		camera.x += camera_speed*dt

	world.render(screen, camera)

	window.blit(pygame.transform.scale(screen, window_size), (0, 0))
	pygame.display.update()

pygame.quit()
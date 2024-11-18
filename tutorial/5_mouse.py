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
					texture = pygame.transform.scale(dirt, (self.tile_size, self.tile_size))
					self.surface.blit(texture, (x*self.tile_size, y*self.tile_size))

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

	def set_tile(self, x, y, tile_type):
		chunk_x = math.floor(x/self.chunk_size/self.tile_size)
		chunk_y = math.floor(y/self.chunk_size/self.tile_size)

		tile_x = math.floor((x - chunk_x*self.chunk_size*self.tile_size)/self.tile_size)
		tile_y = math.floor((y - chunk_y*self.chunk_size*self.tile_size)/self.tile_size)

		if 0 <= chunk_x < self.world_size[0] and 0 <= chunk_y < self.world_size[1]:
			if 0 <= tile_x < self.chunk_size and 0 <= tile_y < self.chunk_size:
				self.chunks[chunk_y][chunk_x].tiles[tile_y][tile_x] = tile_type
				self.chunks[chunk_y][chunk_x].update_surface()


	def render(self, screen, camera):
		w, h = screen.get_size()

		start_x = math.floor(camera.x/self.chunk_size/self.tile_size)
		end_x = math.ceil((camera.x+w)/self.chunk_size/self.tile_size)

		start_y = math.floor(camera.y/self.chunk_size/self.tile_size)
		end_y = math.ceil((camera.y+h)/self.chunk_size/self.tile_size)

		start_x = max(min(start_x, self.world_size[0]), 0)
		end_x = max(min(end_x, self.world_size[0]), 0)

		start_y = max(min(start_y, self.world_size[1]), 0)
		end_y = max(min(end_y, self.world_size[1]), 0)

		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				self.chunks[y][x].render(screen, camera)


class Camera:
	def __init__(self, x, y):
		self.x, self.y = x, y


world = World((4, 3), chunk_size=16, tile_size=16)
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

	mouse = pygame.mouse.get_pressed()
	(mx, my) = pygame.mouse.get_pos()

	if mouse[0]:
		world.set_tile(mx/2+camera.x, my/2+camera.y, 0)
	if mouse[2]:
		world.set_tile(mx/2+camera.x, my/2+camera.y, 1)

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
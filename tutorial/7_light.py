import pygame
import random
import math

pygame.init()

max_fps = 100

window_size = (1200, 800)
screen_size = (600, 400)


tile_textures = [None, 'dirt']
wall_textures = [None, 'dirt_wall']

global_padding = 2

for i, texture in enumerate(tile_textures):
	if texture != None: tile_textures[i] = pygame.image.load(f'data//{texture}.png')
	else: tile_textures[i] = pygame.Surface((16, 16), pygame.SRCALPHA)

for i, texture in enumerate(wall_textures):
	if texture != None: wall_textures[i] = pygame.image.load(f'data//{texture}.png')
	else: wall_textures[i] = pygame.Surface((16, 16), pygame.SRCALPHA)


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
		self.walls = [[0 for x in range(chunk_size)] for y in range(chunk_size)]
		self.light = [[0 for x in range(chunk_size)] for y in range(chunk_size)]


	def update_surface(self):
		self.surface.fill((0, 0, 0, 0))
		for y in range(self.chunk_size):
			for x in range(self.chunk_size):
				#draw walls
				texture = pygame.transform.scale(wall_textures[self.walls[y][x]], (self.tile_size, self.tile_size))
				self.surface.blit(texture, (x*self.tile_size, y*self.tile_size))
				#draw tiles
				texture = pygame.transform.scale(tile_textures[self.tiles[y][x]], (self.tile_size, self.tile_size))
				self.surface.blit(texture, (x*self.tile_size, y*self.tile_size))
				#draw_shadow
				shadow = pygame.Surface((self.tile_size, self.tile_size))
				c = 255*self.light[y][x]/(global_padding*2+1)**2
				c = max(min(c+50, 255), 0)
				shadow.fill((c, c, c))
				self.surface.blit(shadow, (x*self.tile_size, y*self.tile_size), special_flags=pygame.BLEND_RGB_MULT)
				#draw frame
				pygame.draw.rect(self.surface, (255, 0, 0), (0, 0, self.chunk_size*self.tile_size, self.chunk_size*self.tile_size), 1)


	def update_light(self, light):
		self.light = light


	def render(self, screen, camera):
		screen.blit(self.surface, (self.x - round(camera.x), self.y - round(camera.y)))


class World:
	def __init__(self, world_size, chunk_size, tile_size):
		self.world_size = world_size
		self.chunk_size = chunk_size
		self.tile_size = tile_size
		self.chunks = [[Chunk(x*chunk_size*tile_size, y*chunk_size*tile_size, chunk_size, tile_size) for x in range(world_size[0])] for y in range(world_size[1])]
		for y in range(self.world_size[1]):
			for x in range(self.world_size[0]):
				self.chunks[y][x].update_light(self.get_chunk_light(x, y, global_padding))
				self.chunks[y][x].update_surface()


	def set_tile(self, x, y, tile_data):
		chunk_x = math.floor(x/self.chunk_size/self.tile_size)
		chunk_y = math.floor(y/self.chunk_size/self.tile_size)

		tile_x = math.floor((x - chunk_x*self.chunk_size*self.tile_size)/self.tile_size)
		tile_y = math.floor((y - chunk_y*self.chunk_size*self.tile_size)/self.tile_size)

		if 0 <= chunk_x < self.world_size[0] and 0 <= chunk_y < self.world_size[1]:
			if 0 <= tile_x < self.chunk_size and 0 <= tile_y < self.chunk_size:
				current_tile = self.chunks[chunk_y][chunk_x].tiles[tile_y][tile_x]
				current_wall = self.chunks[chunk_y][chunk_x].walls[tile_y][tile_x]
				old_light = int(current_tile == 0 and current_wall == 0)

				if tile_data[0] != None:
					self.chunks[chunk_y][chunk_x].tiles[tile_y][tile_x] = tile_data[0]
				if tile_data[1] != None:
					self.chunks[chunk_y][chunk_x].walls[tile_y][tile_x] = tile_data[1]

				current_tile = self.chunks[chunk_y][chunk_x].tiles[tile_y][tile_x]
				current_wall = self.chunks[chunk_y][chunk_x].walls[tile_y][tile_x]
				new_light = int(current_tile == 0 and current_wall == 0)

				if new_light > old_light:
					self.change_light(chunk_x*self.chunk_size+tile_x, chunk_y*self.chunk_size+tile_y, padding=global_padding, value=+1)
				if new_light < old_light:
					self.change_light(chunk_x*self.chunk_size+tile_x, chunk_y*self.chunk_size+tile_y, padding=global_padding, value=-1)

				self.chunks[chunk_y][chunk_x].update_surface()


	def get_chunk_light(self, chunk_x, chunk_y, padding):
		max_lights = (padding*2+1)**2
		res = []
		for y in range(chunk_y*self.chunk_size, (chunk_y+1)*self.chunk_size):
			res.append([])
			for x in range(chunk_x*self.chunk_size, (chunk_x+1)*self.chunk_size):
				lights = 0
				for dy in range(-padding, padding+1):
					for dx in range(-padding, padding+1):
						sx = x+dx
						sy = y+dy

						ch_x = math.floor(sx/self.chunk_size)
						ch_y = math.floor(sy/self.chunk_size)

						tile_x = math.floor((sx - ch_x*self.chunk_size))
						tile_y = math.floor((sy - ch_y*self.chunk_size))

						if not 0 <= ch_x < self.world_size[0] or not 0 <= ch_y < self.world_size[1]:
							lights += 1
						else:
							tile = self.chunks[ch_y][ch_x].tiles[tile_y][tile_x]
							wall = self.chunks[ch_y][ch_x].walls[tile_y][tile_x]

							if tile == 0 and wall == 0:
								lights += 1

				res[-1].append(lights)
		return res


	def change_light(self, x, y, padding, value):
		chunks_to_update = []
		for dy in range(-padding, padding+1):
			for dx in range(-padding, padding+1):
				sx = x+dx
				sy = y+dy

				ch_x = math.floor(sx/self.chunk_size)
				ch_y = math.floor(sy/self.chunk_size)

				tile_x = math.floor((sx - ch_x*self.chunk_size))
				tile_y = math.floor((sy - ch_y*self.chunk_size))

				if 0 <= ch_x < self.world_size[0] or not 0 <= ch_y < self.world_size[1]:
					self.chunks[ch_y][ch_x].light[tile_y][tile_x] += value
					if not self.chunks[ch_y][ch_x] in chunks_to_update:
						chunks_to_update.append(self.chunks[ch_y][ch_x])

		for chunk in chunks_to_update:
			chunk.update_surface()


	def render(self, screen, camera):
		w, h = screen.get_size()

		start_x = math.floor(camera.x/self.chunk_size/self.tile_size)
		start_y = math.floor(camera.y/self.chunk_size/self.tile_size)
		end_x = math.ceil((camera.x+w)/self.chunk_size/self.tile_size)
		end_y = math.ceil((camera.y+h)/self.chunk_size/self.tile_size)

		start_x = max(min(start_x, self.world_size[0]), 0)
		start_y = max(min(start_y, self.world_size[1]), 0)
		end_x = max(min(end_x, self.world_size[0]), 0)
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
	key = pygame.key.get_pressed()
	(mx, my) = pygame.mouse.get_pos()

	if key[pygame.K_e]:
		if mouse[0]:
			world.set_tile(mx/2+camera.x, my/2+camera.y, [None, 0])
		if mouse[2]:
			world.set_tile(mx/2+camera.x, my/2+camera.y, [None, 1])
	else:
		if mouse[0]:
			world.set_tile(mx/2+camera.x, my/2+camera.y, [0, None])
		if mouse[2]:
			world.set_tile(mx/2+camera.x, my/2+camera.y, [1, None])

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
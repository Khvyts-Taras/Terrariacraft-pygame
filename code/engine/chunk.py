import pygame
import math
from engine import textures


class Chunk:
	def __init__(self, x, y, chunk_size, tile_size, world):
		self.x, self.y = x, y
		self.chunk_size = chunk_size
		self.tile_size = tile_size
		self.world = world
		self.surface = pygame.Surface((self.chunk_size * self.tile_size, self.chunk_size * self.tile_size),
			pygame.SRCALPHA)

		self.tile_ids = [[world.generator.generate_tile(self.x * chunk_size + x, self.y * chunk_size + y)
			for x in range(chunk_size)]
			for y in range(chunk_size)]

		self.update_surface()


	def set_tile(self, tile_x, tile_y, tile_id):
		self.tile_ids[tile_y][tile_x] = tile_id
		pygame.draw.rect(self.surface, (0, 0, 0, 0),
			(tile_x * self.tile_size, tile_y * self.tile_size, self.tile_size, self.tile_size))
		self.surface.blit(textures.block_textures[tile_id], (tile_x * self.tile_size, tile_y * self.tile_size))


	def update_surface(self):
		self.surface.fill((0, 0, 0, 0))
		for y in range(self.chunk_size):
			for x in range(self.chunk_size):
				tile_id = self.tile_ids[y][x]
				texture = textures.block_textures[tile_id]
				self.surface.blit(texture, (x * self.tile_size, y * self.tile_size))


	def render(self, screen, camera):
		render_x = math.floor(self.x * (self.chunk_size * self.tile_size) - camera.x + screen.get_width()/2)
		render_y = math.floor(self.y * (self.chunk_size * self.tile_size) - camera.y + screen.get_height()/2)
		screen.blit(self.surface, (render_x, render_y))

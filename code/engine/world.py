import math
from engine import chunk
from engine import world_generator


class World:
	def __init__(self, size, chunk_size, tile_size):
		self.size = size
		self.chunk_size = chunk_size
		self.tile_size = tile_size
		self.generator = world_generator.WorldGenerator(self)
		self.chunks = [[chunk.Chunk(x, y, chunk_size, tile_size, self)
			for x in range(size[0])]
			for y in range(size[1])]


	def get_tile(self, x, y):
		x, y = round(x), round(y)

		chunk_x = x // (self.chunk_size * self.tile_size)
		chunk_y = y // (self.chunk_size * self.tile_size)

		if 0 <= chunk_x < self.size[0] and 0 <= chunk_y < self.size[1]:
			tile_x = x % (self.chunk_size * self.tile_size) // self.tile_size
			tile_y = y % (self.chunk_size * self.tile_size) // self.tile_size
			tile_id = self.chunks[chunk_y][chunk_x].tile_ids[tile_y][tile_x]

			return tile_id


	def set_tile(self, x, y, tile_id):
		x, y = round(x), round(y)

		chunk_x = x // (self.chunk_size * self.tile_size)
		chunk_y = y // (self.chunk_size * self.tile_size)

		if 0 <= chunk_x < self.size[0] and 0 <= chunk_y < self.size[1]:
			tile_x = x % (self.chunk_size * self.tile_size) // self.tile_size
			tile_y = y % (self.chunk_size * self.tile_size) // self.tile_size

			self.chunks[chunk_y][chunk_x].set_tile(tile_x, tile_y, tile_id)


	def render(self, screen, camera):
		start_x = math.floor((camera.x - screen.get_width()/2) / (self.chunk_size * self.tile_size))
		start_y = math.floor((camera.y - screen.get_height()/2) / (self.chunk_size * self.tile_size))

		end_x = math.ceil((camera.x + screen.get_width()/2) / (self.chunk_size * self.tile_size))
		end_y = math.ceil((camera.y + screen.get_height()/2) / (self.chunk_size * self.tile_size))

		start_x = min(max(start_x, 0), self.size[0])
		start_y = min(max(start_y, 0), self.size[1])

		end_x = min(max(end_x, 0), self.size[0])
		end_y = min(max(end_y, 0), self.size[1])

		for y in range(start_y, end_y):
			for x in range(start_x, end_x):
				self.chunks[y][x].render(screen, camera)


	def get_collisions(self, obj):
		x1, y1 = obj.x, obj.y
		x2, y2 = obj.x + obj.w, obj.y + obj.h

		x1 = math.floor(x1/self.tile_size)
		x2 = math.ceil(x2/self.tile_size)

		y1 = math.floor(y1/self.tile_size)
		y2 = math.ceil(y2/self.tile_size)

		x1 = max(0, min(self.size[0] * self.chunk_size, x1))
		x2 = max(0, min(self.size[0] * self.chunk_size, x2))

		y1 = max(0, min(self.size[1] * self.chunk_size, y1))
		y2 = max(0, min(self.size[1] * self.chunk_size, y2))

		collisions = []
		for y in range(y1, y2):
			for x in range(x1, x2):
				chunk_x = x // self.chunk_size
				chunk_y = y // self.chunk_size

				tile_x = x % self.chunk_size
				tile_y = y % self.chunk_size

				if self.chunks[chunk_y][chunk_x].tile_ids[tile_y][tile_x] != 0:
					collisions.append([x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size])


		return collisions
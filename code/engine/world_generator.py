import random
from engine import textures

class WorldGenerator:
	def __init__(self, world, seed=-1):
		self.world = world

		self.dx = random.randint(0, textures.height.get_width()-1)
		self.dy = random.randint(0, textures.height.get_width()-1)

		self.height = [
		    textures.height.get_at(((self.dx + x) % textures.height.get_width(), self.dy))[0]
		    for x in range(self.world.size[0] * self.world.chunk_size)
		]

	def generate_tile(self, x, y):
		tile_id = 0
		
		if y > self.height[x]:
			tile_id = 3 #grass

		if y > self.height[x] + 1:
			tile_id = 2 #dirt

		if y > self.height[x] + 5:
			tile_id = 1 #stone

		if tile_id == 1:
			if random.random() < 0.0050:
				tile_id = 4 #coal_ore
			if random.random() < 0.0010:
				tile_id = 5 #iron_ore
			if random.random() < 0.0001:
				tile_id = 6 #gold_ore

			if y > self.height[x] + 100:
				if random.random() < 0.0002:
					tile_id = 6

		return tile_id
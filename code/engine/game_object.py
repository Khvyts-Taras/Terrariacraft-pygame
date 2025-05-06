import math
import pygame

class GameObject:
	def __init__(self, x, y, w, h):
		self.x, self.y = x, y
		self.w, self.h = w, h

		self.vx, self.vy = 0, 0

	def update(self, world):
		self.vy += 0.001

		self.vx *= 0.99
		self.vy *= 0.999


		self.x += self.vx
		collisions = world.get_collisions(self)
		if len(collisions) > 0:
			if self.vx > 0:
				collision = min(collisions, key=lambda x: x[0])
				self.x = collision[0] - self.w
			else:
				collision = max(collisions, key=lambda x: x[0])
				self.x = collision[0] + collision[2]
			self.vx = 0
		
		self.y += self.vy
		collisions = world.get_collisions(self)
		if len(collisions) > 0:
			if self.vy > 0:
				collision = min(collisions, key=lambda x: x[1])
				self.y = collision[1] - self.h
			else:
				collision = max(collisions, key=lambda x: x[1])
				self.y = collision[1] + collision[3]
			self.vy = 0


		if abs(self.vx) < 0.0001:
			self.vx = 0
			self.x = round(self.x)
		if abs(self.vy) < 0.0001:
			self.vy = 0
			self.y = round(self.y)


		if self.x < 0:
			self.x = 0
			self.vx = 0

		if self.x + self.w > world.size[0]*world.chunk_size*world.tile_size:
			self.x = world.size[0]*world.chunk_size*world.tile_size - self.w
			self.vx = 0

		if self.y < 0:
			self.y = 0
			self.vy = 0

		if self.y + self.h > world.size[1]*world.chunk_size*world.tile_size:
			self.y = world.size[1]*world.chunk_size*world.tile_size - self.h
			self.vy = 0


	def render(self, screen, camera):
		render_x = math.floor(self.x - camera.x + screen.get_width()/2)
		render_y = math.floor(self.y - camera.y + screen.get_height()/2)

		pygame.draw.rect(screen, (255, 0, 0), (render_x, render_y, self.w, self.h))

class GroundCheck:
	def __init__(self, target):
		self.target = target
		self.update()

	def update(self):
		self.x = self.target.x
		self.y = self.target.y + self.target.h
		self.w = self.target.w
		self.h = 1


	def on_collision(self, world):
		collisions = world.get_collisions(self)
		return collisions != []

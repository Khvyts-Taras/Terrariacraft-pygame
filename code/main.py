import pygame
import random
import math

from engine import properties
from engine import textures
from engine import chunk
from engine import world
from engine import camera
from engine import game_object

pygame.init()

class App:
	def __init__(self):
		self.running = False
		self.window = pygame.display.set_mode(properties.window_size, pygame.RESIZABLE)
		self.scale = properties.scale
		self.screen = pygame.Surface((
			properties.window_size[0] // self.scale, 
			properties.window_size[1] // self.scale
		))
		self.clock = pygame.time.Clock()

		pygame.display.set_icon(textures.icon)
		pygame.display.set_caption(properties.window_name)

		self.world = world.World([properties.world_size_x, properties.world_size_y], properties.chunk_size, properties.tile_size)
		
		spawn_x = properties.world_size_x/2 * properties.chunk_size * properties.tile_size
		spawn_y = self.world.generator.height[int(properties.world_size_x/2) * properties.chunk_size]*properties.tile_size - 48
		self.player = game_object.GameObject(spawn_x, spawn_y, 16, 32)
		self.player.ground_check = game_object.GroundCheck(self.player)
		self.camera = camera.Camera(self.player.x, self.player.y)

		self.camera.target = self.player

		self.selected_block_id = 1


	def run(self):
		self.running = True
		while self.running:
			#dt = self.clock.tick(properties.max_fps)
			key = pygame.key.get_pressed()
			if key[pygame.K_p]:
				dt = self.clock.tick(30)
			else:
				dt = self.clock.tick(100)

			self.update_frame(min(dt, 100))
		pygame.quit()


	def update_frame(self, dt):
		self.screen.fill((255, 255, 255))
		self.events = pygame.event.get()
		key = pygame.key.get_pressed()

		for event in self.events:
			if event.type == pygame.QUIT:
				self.running = False

			elif event.type == pygame.VIDEORESIZE:
				self.screen = pygame.Surface((
					pygame.display.get_window_size()[0]//self.scale,
					pygame.display.get_window_size()[1]//self.scale
					))

			elif event.type == pygame.MOUSEBUTTONDOWN:
				screen_x = event.pos[0]/self.scale - self.screen.get_width()/2
				screen_y = event.pos[1]/self.scale - self.screen.get_height()/2

				x = screen_x + self.camera.x
				y = screen_y + self.camera.y

				l = math.hypot(screen_x, screen_y)

				if event.button == 1:
					if l < 150:
						block_type = self.world.get_tile(x, y)
						self.world.set_tile(x, y, 0)

				if event.button == 2:
					block_type = self.world.get_tile(x, y)
					if block_type != 0:
						self.selected_block_id = block_type

				if event.button == 3:
					block_type = self.world.get_tile(x, y)
					if block_type == 0 and l < 150:
						self.world.set_tile(x, y, self.selected_block_id)


			elif event.type == pygame.MOUSEWHEEL:
				if key[pygame.K_LCTRL]:
					self.scale = min(max(self.scale + event.y, 1), 3)
					self.screen = pygame.Surface((
						pygame.display.get_window_size()[0]//self.scale,
						pygame.display.get_window_size()[1]//self.scale
						))

		speed = 0.2
		for i in range(dt):
			for event in self.events:
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_w:
						if self.player.ground_check.on_collision(self.world):
							self.player.vy = -0.37	

			if key[pygame.K_a]:
				self.player.vx = -speed
			if key[pygame.K_d]:
				self.player.vx = speed
		
			self.player.update(self.world)
			self.player.ground_check.update()
			self.camera.update(self)

		self.render_frame()


	def render_frame(self):
		top_color = textures.sky.get_at((0, 0))
		bottom_color = textures.sky.get_at((0, 1))

		segment_count = self.screen.get_height() // 16
		segment_height = self.screen.get_height() // segment_count

		for i in range(segment_count + 1):
			t = i / (segment_count - 1)
			color = textures.lerp_color(top_color, bottom_color, t)
			pygame.draw.rect(self.screen, color, (0, i * segment_height, self.screen.get_width(), segment_height))


		self.world.render(self.screen, self.camera)
		self.player.render(self.screen, self.camera)

		pygame.draw.circle(self.screen, (255, 0, 0), (self.screen.get_width()/2, self.screen.get_height()/2), 150, 1)

		scaled_screen = pygame.transform.scale_by(self.screen, self.scale)
		self.window.blit(scaled_screen, (0, 0))
		pygame.display.flip()


app = App()
app.run()
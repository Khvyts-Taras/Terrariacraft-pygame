class Camera:
	def __init__(self, x, y):
		self.x, self.y = x, y
		self.w, self.h = 0, 0
		self.target = None

	def update(self, app):
		if self.target != None:
			self.x += (self.target.x - self.x + self.target.w/2)/80
			self.y += (self.target.y - self.y + self.target.h/2)/80


		self.w = app.screen.get_width()
		self.h = app.screen.get_height()

		world_w = app.world.size[0]*app.world.chunk_size*app.world.tile_size
		world_h = app.world.size[1]*app.world.chunk_size*app.world.tile_size

		if self.x - self.w/2 < 0:
			self.x = self.w/2

		if self.x - self.w/2 + self.w > world_w:
			self.x = world_w + self.w/2 - self.w

		if self.y - self.h/2 < 0:
			self.y = self.h/2

		if self.y - self.h/2 + self.h > world_h:
			self.y = world_h + self.h/2 - self.h
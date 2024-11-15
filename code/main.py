import pygame
import random
import math
import numpy as np

pygame.init()

window_size = [1200, 800]
screen_size = [600, 400]

window = pygame.display.set_mode(window_size)
screen = pygame.Surface(screen_size)
clock = pygame.time.Clock()


#[collision, time to break, texture]
block_properties = [[0, 0, None],
					[1, 0.3, pygame.image.load('blocks/stone.png')], #1
					[1, 0.7, pygame.image.load('blocks/granite.png')], #2
					[1, 0.1, pygame.image.load('blocks/dirt.png')], #3
					[1, 0.2, pygame.image.load('blocks/grass_block_side.png')], #4
					[1, 0.2, pygame.image.load('blocks/oak_planks.png')], #5
					[0, 0.1, pygame.image.load('blocks/dark_oak_planks.png')], #6
					[0, 0.7, pygame.image.load('blocks/oak_log.png')], #7
					[0, 0.1, pygame.image.load('blocks/oak_leaves.png')], #8
]


block_size = 16


world_size = [600, 300]

height_map = pygame.image.load('height.png')
granite = pygame.image.load('noise1.png')

rand_x = random.randint(0, 2048-1)
rand_y = random.randint(0, 2048-1)

def world_gen(x, y):
	h = height[x]
	block_id = 0

	if y > height[x]:
		block_id = 4

	if y > height[x] + 1:
		block_id = 3

	if y > height[x] + 7:
		block_id = 1

	if y > height[x] + 10:
		if granite.get_at(((x+rand_x)%2048, (y+rand_y)%2048))[0] > 70:
			block_id = 2
		else:
			block_id = 1

	return block_id


height = []
for x in range(rand_x, rand_x+world_size[0]):
	height.append(height_map.get_at((x%2048, rand_y))[0]/255*world_size[1]/2)

world = [[world_gen(x, y) for x in range(world_size[0])] for y in range(world_size[1])]


tree = [[-1, -1, 8, -1, -1],
		[-1,  8, 8,  8, -1],
		[-1,  8, 7,  8, -1],
		[-1, -1, 7, -1, -1],
		[-1, -1, 7, -1, -1],
		[-1, -1, 7, -1, -1]]

tree_center = [5, 2]

num_trees = 70
for i in range(num_trees):
	x = random.randint(0, world_size[0]-1)
	y = int(height[x])

	for sy in range(len(tree)):
		for sx in range(len(tree[0])):
			px = x + sx
			py = y + sy

			if 0 <= px < world_size[0] and 0 <= py < world_size[1]:
				if tree[sy][sx] != -1:
					world[py - tree_center[0]][px - tree_center[1]] = tree[sy][sx]



def create_gradient(surface, color1, color2, steps):
	width, height = surface.get_size()
	r1, g1, b1 = color1
	r2, g2, b2 = color2

	for i in range(steps):
		r = r1 + (r2 - r1) * i // (steps - 1)
		g = g1 + (g2 - g1) * i // (steps - 1)
		b = b1 + (b2 - b1) * i // (steps - 1)
		pygame.draw.rect(surface, (r, g, b), (0, i * math.floor(height/steps), width, math.ceil(height/steps)))




def point_to_block(x, y):
	bx = math.floor(x/block_size)
	by = math.floor(y/block_size)

	in_world = not (bx < 0 or bx > world_size[0]-1 or by < 0 or by > world_size[1]-1)

	bx = max(0, min(bx, world_size[0]-1))
	by = max(0, min(by, world_size[1]-1))

	return bx, by, in_world

def render_world():
	start_x, start_y, _ = point_to_block(cam_x, cam_y)
	end_x, end_y, _ = point_to_block(cam_x+screen_size[0], cam_y+screen_size[1])

	for y in range(start_y, end_y+1):
		for x in range(start_x, end_x+1):
			block_id = world[y][x]
			if block_id > 0:

				screen.blit(block_properties[block_id][2], (math.floor(x*block_size - cam_x), math.floor(y*block_size - cam_y)))

def on_collision(a, b):
	x1, y1, w1, h1 = a
	x2, y2, w2, h2 = b
	return (x1+w1 > x2 and x1 < x2+w2) and (y1+h1 > y2 and y1 < y2+h2)

class Object:
	def __init__(self, x, y, w, h):
		self.x, self.y = x, y
		self.w, self.h = w, h

		self.vx, self.vy = 0, 0

	def get_collisions(self):
		start_x, start_y, start_in_world = point_to_block(player.x, player.y)
		end_x, end_y, end_in_world = point_to_block(player.x+player.w, player.y+player.h)

		collisions = []

		if start_in_world or end_in_world:
			for y in range(start_y, end_y+1):
				for x in range(start_x, end_x+1):
					if block_properties[world[y][x]][0]:
						collisions.append((x*block_size, y*block_size, block_size, block_size))

		return collisions


	def update(self, dt):
		self.vy += 0.4*dt

		self.vx *= 0.9**dt
		self.vy *= 0.99**dt

		self.x += self.vx*dt
		for collision in self.get_collisions():
			if on_collision((self.x, self.y, self.w, self.h), collision):
				if self.vx > 0:
					self.x = collision[0] - self.w
				else:
					self.x = collision[0] + collision[2]
				self.vx = 0

		self.y += self.vy*dt
		for collision in self.get_collisions():
			if on_collision((self.x, self.y, self.w, self.h), collision):
				if self.vy > 0:
					self.y = collision[1] - self.h
				else:
					self.y = collision[1] + collision[3]
				self.vy = 0


	def render(self):
		pygame.draw.rect(screen, (255, 50, 50), (self.x - cam_x, self.y - cam_y, self.w, self.h))


player = Object(world_size[0]*block_size//2, height[world_size[0]//2]*block_size-32, 16, 32)

cam_x = player.x - screen_size[0]/2 + player.w/2
cam_y = player.y - screen_size[1]/2 + player.h/2

break_timer = 0

last_bx, last_by = 0, 0


current_slot = 0
current_block = 6

inventory = [1, 2, 3, 4, 5, 6, 0, 0]

time = 0
while 1:
	dt = clock.tick(60)
	if dt > 100:
		continue
	time += dt/1000
	screen.fill((138, 219, 237))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_w:
				player.vy = -7
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				break_timer = time
		if event.type == pygame.MOUSEWHEEL:
			current_slot = (current_slot - event.y)%8



	key = pygame.key.get_pressed()
	if key[pygame.K_w]:
		pass
	if key[pygame.K_s]:
		pass
	if key[pygame.K_a]:
		player.vx -= 0.4
	if key[pygame.K_d]:
		player.vx += 0.4

	if key[pygame.K_i]:
		cam_y -= 3
	if key[pygame.K_k]:
		cam_y += 3
	if key[pygame.K_j]:
		cam_x -= 3
	if key[pygame.K_l]:
		cam_x += 3

	if key[pygame.K_1]:
		current_slot = 0		
	if key[pygame.K_2]:
		current_slot = 1
	if key[pygame.K_3]:
		current_slot = 2
	if key[pygame.K_4]:
		current_slot = 3
	if key[pygame.K_5]:
		current_slot = 4
	if key[pygame.K_6]:
		current_slot = 5
	if key[pygame.K_7]:
		current_slot = 6
	if key[pygame.K_8]:
		current_slot = 7
	if key[pygame.K_9]:
		current_slot = 8

	current_block = inventory[current_slot]




	pos = pygame.mouse.get_pos()
	mx = pos[0]/2 + cam_x
	my = pos[1]/2 + cam_y


	bx, by, in_world = point_to_block(mx, my)
	if bx != last_bx or by != last_by:
		break_timer = time

	if pygame.mouse.get_pressed()[0] and in_world:
		if time > break_timer + block_properties[world[by][bx]][1]:
			world[by][bx] = 0
			break_timer = time

	if pygame.mouse.get_pressed()[1] and in_world:
		if world[by][bx] in inventory:
			current_slot = inventory.index(world[by][bx])
		else:
			if 0 in inventory:
				inventory[inventory.index(0)] = world[by][bx]
			else:
				inventory[current_slot] = world[by][bx]

	if pygame.mouse.get_pressed()[2] and in_world:
		if world[by][bx] == 0:
			world[by][bx] = current_block

	last_bx, last_by = bx, by



	player.update(dt/16)

	cam_x += (player.x - screen_size[0]/2 + player.w/2 - cam_x)/10
	cam_y += (player.y - screen_size[1]/2 + player.h/2 - cam_y)/10

	create_gradient(screen, (66, 135, 245), (151, 201, 240), 30)
	render_world()
	player.render()


	if pygame.mouse.get_pressed()[0]:
		if world[by][bx] != 0:
			progress = min((time - break_timer)/block_properties[world[by][bx]][1], 1)
			pygame.draw.rect(screen, (50, 50, 50), (bx*block_size - cam_x, by*block_size - cam_y, progress*block_size, block_size))



	slot_size = 20
	for i in range(len(inventory)):
		pygame.draw.rect(screen, (70, 50, 50), (i*slot_size, 0, slot_size, slot_size))

		selected_color = (150, 120, 120)
		if current_slot == i:
			selected_color = (230, 210, 210)
		pygame.draw.rect(screen, selected_color, (i*slot_size, 0, slot_size, slot_size), 1)

		if inventory[i] != 0:
			screen.blit(block_properties[inventory[i]][2], (i*slot_size + slot_size/2 - block_size/2, slot_size/2 - block_size/2))


	window.blit(pygame.transform.scale(screen, window_size), (0, 0))
	pygame.display.update()
	
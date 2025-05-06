import pygame
from engine import properties


icon = pygame.image.load('textures/icons/icon.png')
sky = pygame.image.load('textures/maps/sky.png')
height = pygame.image.load('textures/maps/height.png')

air_texture = pygame.Surface((properties.tile_size, properties.tile_size), pygame.SRCALPHA)
air_texture.fill((0, 0, 0, 0))

block_textures = [air_texture,
				  pygame.image.load('textures/blocks/stone.png'),
				  pygame.image.load('textures/blocks/dirt.png'),
				  pygame.image.load('textures/blocks/grass.png'),
				  pygame.image.load('textures/blocks/coal_ore.png'),
				  pygame.image.load('textures/blocks/iron_ore.png'),
				  pygame.image.load('textures/blocks/gold_ore.png')]

def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))
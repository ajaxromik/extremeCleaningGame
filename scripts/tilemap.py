# MyPygame: tilemap
# William Carr
# ProgLang
# 9/18/2024

import pygame

class Tilemap:
	SURROUND_OFFSETS = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,0),(0,1),(1,-1),(1,0),(1,1)]
	SOLID_TILES = {'grass', 'stone', 'stopSign'}

	def __init__(self, game, tile_size=16):
		self.game = game
		self.tile_size = tile_size
		self.map = {}
		self.offgrid_tiles = []

	def render(self, surf):
		for tile in self.offgrid_tiles:
			surf.blit(self.game.assets[tile['type']][tile['variant']], tile['pos'])

		for loc in self.map:
			tile = self.map[loc]
			surf.blit(self.game.assets[tile['type']][tile['variant']], (tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size))

	"""
	Takes a pixel (x,y) position and finds the tiles surrounding that spot
	"""
	def tiles_touched(self, pos):
		tiles = []
		tile_coords = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
		for offset in self.SURROUND_OFFSETS:
			current_tile = str(tile_coords[0] + offset[0]) + ';' + str(tile_coords[1] + offset[1])
			if current_tile in self.map:
				print(current_tile)
				tiles.append(self.map[current_tile])
		return tiles

	def solid_tiles_touched(self, pos):
		rects = []
		for tile in self.tiles_touched(pos):
			if tile['type'] in self.SOLID_TILES:
				rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
		return rects

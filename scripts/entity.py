# MyPygame: entities
# William Carr
# ProgLang
# 10/16/2024

import pygame

class TouchableBox:
	def __init__(self, game, pos, size, e_type='', solid=False):
		# print(f"pos: {pos} size: {size} e_type: {e_type} solid: {solid}")
		self.game = game
		self._pos = list(pos) # underscore apparently means its supposed to be used only internally
		self.type = e_type
		self.size = size
		self.solid = solid # boolean of whether player can pass through them
		self.hitbox = pygame.Rect(pos, size)

	@property
	def pos(self): # getter that allows use like a property
		return self._pos

	@pos.setter
	def pos(self, newPos):
		if newPos != self.pos:
			self._pos = newPos
			self.hitbox = pygame.Rect(newPos, self.size)

	def checkCollide(self, rect, action):
		touching = self.hitbox.colliderect(rect)
		action(touching)
		return touching

	def render(self, surface):
		surface.blit(self.game.assets[self.type], self.pos)

class PhysicsEntity:
	def __init__(self, game, e_type, pos, size):
		self.game = game
		self.type = e_type
		self.pos = list(pos)
		self.size = size
		self.velocity = [0,0]
		self.hitbox = pygame.Rect(pos, size)
		# self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

	"""
	Moves an entity by a movement vector adding on to the object's current velocity
	Current velocity is not changed from it
	"""
	def update(self, tilemap, collidables, movement=(0,0)):
		# self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

		frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

		self.pos[0] += frame_movement[0]
		self.pos[1] += frame_movement[1]

		self.hitbox = pygame.Rect(self.pos, self.size)

		for obj in collidables.values():
			if obj.solid == True and self.hitbox.colliderect(obj.hitbox):
				intersection = self.hitbox.clip(obj.hitbox) # rect of intersection
				# print("hit")
				if intersection.width > intersection.height: # this means closer to the top or bottom
					if intersection.top == obj.hitbox.top: # closest to top
						self.hitbox.bottom = obj.hitbox.top
					else:
						self.hitbox.top = obj.hitbox.bottom
					self.pos[1] = self.hitbox.y
					# print(f"y {self.pos[1]}")
				else:
					if intersection.left == obj.hitbox.left: # closest to left side of box
						self.hitbox.right = obj.hitbox.left
					else:
						self.hitbox.left = obj.hitbox.right
					self.pos[0] = self.hitbox.x
					# print(f"x {self.pos[0]}")
					
		# would work if the avatar is one tile in size, but that's not the case here
		# for rect in tilemap.solid_tiles_touched(self.pos):
		# 	if self.hitbox.colliderect(rect):
		# 		if frame_movement[0] > 0:
		# 			self.hitbox.right = rect.left
		# 			self.collisions['right'] = True
		# 		if frame_movement[0] < 0:
		# 			self.hitbox.left = rect.right
		# 			self.collisions['left'] = True
		# 		self.pos[0] = self.hitbox.x
		# 		if frame_movement[1] > 0:
		# 			self.hitbox.bottom = rect.top
		# 			self.collisions['down'] = True
		# 		if frame_movement[1] < 0:
		# 			self.hitbox.top = rect.bottom
		# 			self.collisions['up'] = True
		# 		self.pos[1] = self.hitbox.y

	def render(self, surface):
		surface.blit(self.game.assets[self.type], self.pos)

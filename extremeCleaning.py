# Pygame Project
# William Carr
# ProgLang
# 10/16/2024

import pygame
import sys
import random

from scripts.utils import load_image, load_images
from scripts.entity import PhysicsEntity, TouchableBox

window_leave, window_enter = 32784, 32783

class Game:

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('farming simulator')

		self.scr_res = (640,480)
		self.screen = pygame.display.set_mode(self.scr_res)

		self.display = pygame.Surface(self.scr_res) # tuple(x // 2 for x in scr_res)

		cardboardBox = pygame.Surface((32,32))
		cardboardBox.fill((100,65,23))

		self.assets = {
			'player': load_image('frog.png'),
			'cardboardBox' : cardboardBox,
		}

		self.clock = pygame.time.Clock()

		player_img = self.assets['player']
		self.player = PhysicsEntity(self, 'player', (290, 190), (player_img.get_width(), player_img.get_height()))

		self.collidables = {
			'leftWall': TouchableBox(self, (-30, 0), (20,self.scr_res[1]), solid=True),
			'rightWall': TouchableBox(self, (10+self.scr_res[0], 0), (20,self.scr_res[1]), solid=True),
			'topWall': TouchableBox(self, (0, -30), (self.scr_res[0],20), solid=True),
			'bottomWall': TouchableBox(self, (0, 10+self.scr_res[1]), (self.scr_res[0],20), solid=True),
			'mouseChaser' : TouchableBox(self, (100,100), (24,24), "mouseChaser")
		}

		# box setup
		for i in range(4):
			for j in range(2):
				box = TouchableBox(self, ((6+i*9)*16, (8+j*14)*16), (32,32), 'cardboardBox', False)
				# any future customization
				self.collidables['cardboard'+str(i+j*4)] = box
		self.breakables = [f"cardboard{i}" for i in range(8)]
		self.harvested = 0

	def run(self):
		onScreen = True
		# 0 means nothing is pressed for that direction, 1 is an arrow key or one of the wasd keys, 2 is both
		moving = {'up': 0, 'down': 0, 'right': 0, 'left': 0}
		while True:

			self.display.fill((14,219,50))

			a = TouchableBox(self, (6*16, 8*16), (32,32), 'cardboardBox', False)
			a.render(self.display)
			a.checkCollide(self.player.hitbox, lambda bool: print("touching!") if bool else 0)

			for box in list(map(lambda key: self.collidables[key], self.breakables)):
				box.render(self.display)

			self.player.update(self.collidables)

			# self.collidables['collision_area'].checkCollide(self.player.hitbox, lambda bool: (
			# 	pygame.draw.rect(self.display, ((0,0,255) if bool else (255,255,0)), self.collidables['collision_area'].hitbox)))

			self.player.render(self.display)

			mousePos = (m_x,m_y) = pygame.mouse.get_pos()

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_LEFT:
						moving['left'] += 1
						if moving['left'] == 1:
							self.player.velocity[0] += -3
					elif event.key == pygame.K_RIGHT:
						moving['right'] += 1
						if moving['right'] == 1:
							self.player.velocity[0] += 3
					elif event.key == pygame.K_UP:
						moving['up'] += 1
						if moving['up'] == 1:
							self.player.velocity[1] += -3
					elif event.key == pygame.K_DOWN:
						moving['down'] += 1
						if moving['down'] == 1:
							self.player.velocity[1] += 3
					elif event.key == pygame.K_a:
						moving['left'] += 1
						if moving['left'] == 1:
							self.player.velocity[0] += -3
					elif event.key == pygame.K_d:
						moving['right'] += 1
						if moving['right'] == 1:
							self.player.velocity[0] += 3
					elif event.key == pygame.K_w:
						moving['up'] += 1
						if moving['up'] == 1:
							self.player.velocity[1] += -3
					elif event.key == pygame.K_s:
						moving['down'] += 1
						if moving['down'] == 1:
							self.player.velocity[1] += 3
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						moving['left'] -= 1
						if moving['left'] == 0:
							self.player.velocity[0] += 3
					elif event.key == pygame.K_RIGHT:
						moving['right'] -= 1
						if moving['right'] == 0:
							self.player.velocity[0] += -3
					elif event.key == pygame.K_UP:
						moving['up'] -= 1
						if moving['up'] == 0:
							self.player.velocity[1] += 3
					elif event.key == pygame.K_DOWN:
						moving['down'] -= 1
						if moving['down'] == 0:
							self.player.velocity[1] += -3
					elif event.key == pygame.K_a:
						moving['left'] -= 1
						if moving['left'] == 0:
							self.player.velocity[0] += 3
					elif event.key == pygame.K_d:
						moving['right'] -= 1
						if moving['right'] == 0:
							self.player.velocity[0] += -3
					elif event.key == pygame.K_w:
						moving['up'] -= 1
						if moving['up'] == 0:
							self.player.velocity[1] += 3
					elif event.key == pygame.K_s:
						moving['down'] -= 1
						if moving['down'] == 0:
							self.player.velocity[1] += -3

				### window logic
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == window_leave:
					onScreen = False
				elif event.type == window_enter:
					onScreen = True

			self.screen.blit(self.display, (0,0))
			pygame.display.update()
			self.clock.tick(60)

game = Game().run()
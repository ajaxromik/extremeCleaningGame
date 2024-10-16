# Pygame Project
# William Carr
# ProgLang
# 10/16/2024

import pygame
import sys
import random

from scripts.utils import load_image, load_images
from scripts.entity import PhysicsEntity, TouchableBox
from scripts.tilemap import Tilemap

window_leave, window_enter = 32784, 32783

class Game:

	def __init__(self):
		pygame.init()
		pygame.display.set_caption('farming simulator')

		self.scr_res = (640,480)
		self.screen = pygame.display.set_mode(self.scr_res)

		self.display = pygame.Surface(self.scr_res) # tuple(x // 2 for x in scr_res)

		# must be tuple to initialize plants correctly
		plants = (tillAsset, seedAsset, sproutAsset, grownAsset) = tuple(pygame.Surface((32,32)) for _ in range(4))
		for plant in plants:
			plant.fill((100,65,23))
		seedAsset.fill((34,139,34),rect=(14,14,4,4))
		sproutAsset.fill((34,139,34),rect=(10,10,12,12))
		grownAsset.fill((34,139,34),rect=(4,4,24,24))

		mouseAsset = pygame.Surface((24,24))
		mouseAsset.fill((0,63,191))


		self.assets = {
			'player': load_image('frog.png'),
			'grass': load_images('tiles/grass'),
			'stone': load_images('tiles/stone'),
			'stopSign' : load_image('stop.png'),
			'unplantedTill' : tillAsset,
			'seededTill' : seedAsset,
			'sproutTill' : sproutAsset,
			'grownTill' : grownAsset,
			'mouseChaser' : mouseAsset,
		}

		self.clock = pygame.time.Clock()

		player_img = self.assets['player']
		self.player = PhysicsEntity(self, 'player', (290, 190), (player_img.get_width(), player_img.get_height()))

		self.collidables = {
			# 'stopSign': TouchableBox(self, (296, 400), (48,48), 'stopSign', False),
			'leftWall': TouchableBox(self, (-30, 0), (20,self.scr_res[1]), solid=True),
			'rightWall': TouchableBox(self, (10+self.scr_res[0], 0), (20,self.scr_res[1]), solid=True),
			'topWall': TouchableBox(self, (0, -30), (self.scr_res[0],20), solid=True),
			'bottomWall': TouchableBox(self, (0, 10+self.scr_res[1]), (self.scr_res[0],20), solid=True),
			# 'collision_area': TouchableBox(self, (100,100),(50,300)),
			'mouseChaser' : TouchableBox(self, (100,100), (24,24), "mouseChaser")
		}

		self.tilemap = Tilemap(self, tile_size=16)

		# till setup with some custom vars
		for i in range(4):
			for j in range(2):
				# print(f"{i}, {j}, {i+j*4}") #tillspot6 should be special
				till = TouchableBox(self, ((6+i*9)*16, (8+j*14)*16), (32,32), 'unplantedTill')
				till.planted = False
				till.water = 0
				till.harvestTime = -1000
				# growEvent = pygame.event.custom_type()
				# till.growEvent = pygame.event.Event(growEvent, {'touchBox': till})
				self.collidables['tillSpot'+str(i+j*4)] = till
		self.tillSpots = [f"tillSpot{i}" for i in range(8)]
		self.harvested = 0

	def run(self):
		onScreen = True
		moving = {'up': False, 'down': False, 'right': False, 'left': False} # to allow both arrow keys and wasd
		while True:
			self.player.update(self.tilemap, self.collidables)

			self.display.fill((14,219,50))

			self.tilemap.render(self.display)

			# self.collidables['stopSign'].render(self.display)

			# self.collidables['collision_area'].checkCollide(self.player.hitbox, lambda bool: (
			# 	pygame.draw.rect(self.display, ((0,0,255) if bool else (255,255,0)), self.collidables['collision_area'].hitbox)))

			# till spots 
			# print(pygame.time.get_ticks() - self.collidables['tillSpot0'].harvested)
			for till in list(map(lambda key: self.collidables[key], self.tillSpots)): # cool bit of lambda functions
				"""
				Till spots can be 1. unplanted, 2. planted, 3. sprouting, and 4. harvestable
				cycle goes as such:
				1 when untouched 
				2 after farmer touches it
				3 after mouse watered it enough
				4 after mouse watered it enough
				1 after harvesting by farmer again
				"""
				# timeSinceUpdated = pygame.time.get_ticks() - till.updated
				# if till.planted and till.type == 'unplantedTill' and timeSinceUpdated > 1000:
				# 	till.planted = False # 3s cooldown to plant again
				
				if till.hitbox.colliderect(self.player.hitbox):
					# print(f"{till.harvestTime}	{pygame.time.get_ticks()}")
					# if till.planted and till.type == 'grownTill' and timeSinceUpdated > 1000: # harvest touch
					if till.planted and till.type == 'grownTill':
						self.harvested += 1
						till.harvestTime = pygame.time.get_ticks()
						print(self.harvested)
						till.type = 'unplantedTill'
						till.planted = False
						till.water = 0
					elif not till.planted and pygame.time.get_ticks() - till.harvestTime >= 1000: # plant new seed
						till.planted = True
						till.type = 'seededTill'
						# pygame.time.set_timer(till.growEvent, 5000, 1) # just make these happen with cursor though

						# print(f'seeded {till}')
					# elif till.type == 'seededTill' and timeSinceUpdated > 3000: # incorrect logic for not touching but ok for temp

					# elif till.type == 'sproutTill' and timeSinceUpdated > 3000:
						# print(f'sending {till.growEvent}\npeeking? {pygame.event.peek(till.growEvent.type)}')
						# pygame.time.set_timer(till.growEvent, 5000, 1) # otherwise the timer would keep being reset to 5 seconds

				if till.planted and till.hitbox.colliderect(self.collidables['mouseChaser'].hitbox):
					till.water += 1
					# print(f"w:{till.water}	t:{pygame.time.get_ticks()}")
					if till.type == 'seededTill' and till.water > 180: # because 3 seconds * 60 ticks per second
						# print(timeSinceUpdated)
						till.water = 0
						till.type = 'sproutTill'
					elif till.type == 'sproutTill' and till.water > 180:
						till.water = 0
						till.type = 'grownTill'

				till.render(self.display)
				# if till.colliderect(self.player.hitbox):


			self.player.render(self.display)

			mousePos = (m_x,m_y) = pygame.mouse.get_pos()

			if onScreen and m_x in range(12,self.scr_res[0]-12) and m_y in range(12,self.scr_res[1]-12): # should render behind farming tills
				self.collidables['mouseChaser'].pos = tuple(i-12 for i in mousePos) # moves the box to be centered around mouse
				# print("pos: "+str(self.collidables['mouseChaser'].pos))
				self.collidables['mouseChaser'].render(self.display)

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if not moving['left'] and event.key == pygame.K_LEFT:
						moving['left'] = True
						self.player.velocity[0] += -3
					elif not moving['right'] and event.key == pygame.K_RIGHT:
						moving['right'] = True
						self.player.velocity[0] += 3
					elif not moving['up'] and event.key == pygame.K_UP:
						moving['up'] = True
						self.player.velocity[1] += -3
					elif not moving['down'] and event.key == pygame.K_DOWN:
						moving['down'] = True
						self.player.velocity[1] += 3
					elif not moving['left'] and event.key == pygame.K_a:
						moving['left'] = True
						self.player.velocity[0] += -3
					elif not moving['right'] and event.key == pygame.K_d:
						moving['right'] = True
						self.player.velocity[0] += 3
					elif not moving['up'] and event.key == pygame.K_w:
						moving['up'] = True
						self.player.velocity[1] += -3
					elif not moving['down'] and event.key == pygame.K_s:
						moving['down'] = True
						self.player.velocity[1] += 3
				elif event.type == pygame.KEYUP:
					if moving['left'] and event.key == pygame.K_LEFT:
						moving['left'] = False
						self.player.velocity[0] += 3
					elif moving['right'] and event.key == pygame.K_RIGHT:
						moving['right'] = False
						self.player.velocity[0] += -3
					elif moving['up'] and event.key == pygame.K_UP:
						moving['up'] = False
						self.player.velocity[1] += 3
					elif moving['down'] and event.key == pygame.K_DOWN:
						moving['down'] = False
						self.player.velocity[1] += -3
					elif moving['left'] and event.key == pygame.K_a:
						moving['left'] = False
						self.player.velocity[0] += 3
					elif moving['right'] and event.key == pygame.K_d:
						moving['right'] = False
						self.player.velocity[0] += -3
					elif moving['up'] and event.key == pygame.K_w:
						moving['up'] = False
						self.player.velocity[1] += 3
					elif moving['down'] and event.key == pygame.K_s:
						moving['down'] = False
						self.player.velocity[1] += -3

				### window logic
				elif event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == window_leave:
					onScreen = False
				elif event.type == window_enter:
					onScreen = True
				# elif event.type >= pygame.USEREVENT:
				# 	print('getting grow')
				# 	try:
				# 		till = event.__dict__['touchBox'] # gets the till from the event dictionary
				# 		match till.type:
				# 			case 'seededTill':
				# 				till.type = 'sproutTill'
				# 			case 'sproutTill':
				# 				till.type = 'grownTill'
				# 	except NameError:
				# 		print('failed') 
				# else:
				# 	print(event)

			self.screen.blit(self.display, (0,0))
			pygame.display.update()
			self.clock.tick(60)

game = Game().run()
import pygame
from pygame import *

#base entity that is used to create most objects
class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

#block used to create the map
class Platform(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/block.png").convert_alpha()
		self.image = pygame.transform.scale(self.image,(16*3,16*3))
		self.rect = Rect(x, y, 16*3, 16*3)

#used to create the King NPC
class King(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/king.png").convert_alpha()
		self.image = pygame.transform.scale(self.image,(16*4,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)

#create the Prinecss NPC
class Princess(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/p2.png").convert_alpha()
		self.image = pygame.transform.scale(self.image,(16*4,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)
		
#used to determine exit to the new map
#currently image just set to blue filling for distinction
class ExitBlock(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/gate.png").convert_alpha()
		self.image = pygame.transform.scale(self.image,(16*3, 16*6))
		self.rect = Rect(x, y, 16*3, 16*6)
		
#used to determine exit to the previous map
#currently image just set to blue filling for distinction
class PreviousBlock(Platform):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/gate.png").convert_alpha()
		self.image = pygame.transform.scale(self.image,(16*3,16*6))
		self.rect = Rect(x, y, 16*3, 16*6)
		
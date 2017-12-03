#Project 3 - CPSC 386 - MW 5:30 PM
#AMMU - Danial Moahmmad, Felicia Aubert, Annette Ulrichsen, Christopher Menesis
#Platformer - goal is to find the princess
#Sources: Anthony Biron - https://www.youtube.com/channel/UCy0eKoY5BVtcJHFQGKVe1yg
#ChiliGames - Knight images - https://opengameart.org/content/knight-and-knight-animation
#Platform - Kenney - https://opengameart.org/content/platformer-tiles
#Princess image - ?
#Music - Code Manu - https://opengameart.org/content/platformer-game-music-pack
#Background Image - DPP Reskinning - http://appreskinning.blogspot.com/2017/07/backgrounds-for-2d-platforms-pack.html

#! /usr/bin/python
import sys
import os
import pygame
from pygame import *
from time import sleep

WIN_WIDTH = 256*3
WIN_HEIGHT = 224*3
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)

#determine whether to switch maps - used in while loop
moveNext = False
movePrev = False
done = False

#standard pygame initializations
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
newX = 0
newY = 0
pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Knight's Quest")
pygame.mixer.music.load('music/bg.mp3')
pygame.mixer.music.play(-1)

#set character animations and sizes
character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/stand.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightstand1 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/run1.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightwalk1 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/run2.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightwalk2 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/run3.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightwalk3 = character

character = Surface((16,32),pygame.SRCALPHA)
character = pygame.image.load("images/jump.png").convert_alpha()
character = pygame.transform.scale(character, (16*4,32*3))
knightjump1 = character

#allow for font to be rendered later
pygame.font.init()
dialogFont = pygame.font.SysFont("garuda", 20)
pygame.display.update()
white = (255,255,255)
black = (0,0,0)


def main():
	#initialize all required variables
	timer = pygame.time.Clock()
	currLevel = 1
	up = down = left = right = running = False
	platforms = []
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	bgImg = pygame.image.load('images/bg1.png')
	background.blit(bgImg, (0,0))
	screen.blit(background, (0,0))
	
	pygame.display.update()
	#bg = Surface((WIN_WIDTH,WIN_HEIGHT)).convert()
	entities = pygame.sprite.Group()
	speech = pygame.image.load("images/title.png").convert()
	speech = pygame.transform.scale(speech ,(171*2,108*2))
	screen.blit(speech, (HALF_WIDTH - 171 ,HALF_HEIGHT - 108))
	
	pygame.display.update()
	sleep(2)
	x = y = 0
	level = getLevel(currLevel)
	
	# build the level based off the level returned
	for row in level:
		for col in row:
			if col == "P":
				p = Platform(x, y)
				platforms.append(p)
				entities.add(p)
			if col == "e":
				e = ExitBlock(x, y)
				platforms.append(e)
				entities.add(e)
				
			if col == "B":
				B = PreviousBlock(x, y)
				platforms.append(B)
				entities.add(B)
		
			if col == "K":
				k = King(x, y)
				platforms.append(k)
				entities.add(k)
				
			if col == "F":
				F = Princess(x, y)
				platforms.append(F)
				entities.add(F)
					
			x += 16*3
		y += 16*3
		x = 0

	total_level_width  = len(level[0])*16*3
	total_level_height = len(level)*16*3
	camera = Camera(complex_camera, total_level_width, total_level_height)
	player = Player(newX, newY)
	entities.add(player)

	#game run loop
	while 1:
		timer.tick(60)
		#allows for character to be moved
		for e in pygame.event.get():
			if e.type == QUIT: raise SystemExit("QUIT")
			if e.type == KEYDOWN and e.key == K_ESCAPE:
				raise SystemExit("ESCAPE")
			if e.type == KEYDOWN and e.key == K_UP:
				up = True
			if e.type == KEYDOWN and e.key == K_DOWN:
				down = True
			if e.type == KEYDOWN and e.key == K_LEFT:
				left = True
			if e.type == KEYDOWN and e.key == K_RIGHT:
				right = True
			if e.type == KEYUP and e.key == K_UP:
				up = False
			if e.type == KEYUP and e.key == K_DOWN:
				down = False
			if e.type == KEYUP and e.key == K_RIGHT:
				right = False
			if e.type == KEYUP and e.key == K_LEFT:
				left = False
			
		screen.blit(background,(0,0))
		camera.update(player)
		# update player, draw everything else
		player.update(up, down, left, right, running, platforms)     
		
		#if reached portal, move to respective map or finish the game
		if (moveNext == True or movePrev == True or done == True):
			x=0
			y=0
			if moveNext:
				currLevel = currLevel + 1
			if movePrev:
				currLevel = currLevel - 1			
			
			#reset platforms in order to build the new map
			platforms=[]
			#get the next or previous level
			level = getLevel(currLevel)
			
			#if game is finished, display dialogue and leave game loop
			if done:
				for e in entities:
					screen.blit(e.image, camera.apply(e))
				speech = pygame.image.load("images/princess-dialogue.png").convert_alpha()
				screen.blit(speech, (40,0))
				pygame.display.update()
				sleep(2)
				break
				
			entities = pygame.sprite.Group()
		
			for row in level:
				for col in row:
					if col == "P":
						p = Platform(x, y)
						platforms.append(p)
						entities.add(p)
					if col == "e":
						e = ExitBlock(x, y)
						platforms.append(e)
						entities.add(e)					
					if col == "B":
						B = PreviousBlock(x, y)
						platforms.append(B)
						entities.add(B)					
					if col == "K":
						k = King(x, y)
						platforms.append(k)
						entities.add(k)					
					if col == "F":
						F = Princess(x, y)
						platforms.append(F)
						entities.add(F)						
					x += 16*3
				y += 16*3
				x = 0

			total_level_width  = len(level[0])*16*3
			total_level_height = len(level)*16*3
			camera = Camera(complex_camera, total_level_width, total_level_height)
			player = Player(newX, newY)
			entities.add(player)
			sleep(.4)
		#draw all the entities added through level generation
		for e in entities:
			screen.blit(e.image, camera.apply(e))
		pygame.display.update()
	
	#display end dialogue
	screen.fill(black)
	speech = pygame.image.load("images/end-dialogue.png")
	#363 is width of image and 90 is height - will center it
	screen.blit(speech, (HALF_WIDTH - 363/2, HALF_HEIGHT - 90/2))
	pygame.display.update()
	sleep(2.5)
	
#allows for the camera to focus on the player - source provided
#at start of the file
class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		self.state = Rect(0, 0, width, height)

	def apply(self, target):
		return target.rect.move(self.state.topleft)

	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

	l = min(0, l)                           # stop scrolling at the left edge
	l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
	t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
	t = min(0, t)                           # stop scrolling at the top
	return Rect(l, t, w, h)

#returns the next or previous level for generation
#sets character spawn coordinates
def getLevel(currLevel):
	global newX
	global newY
	global moveNext
	global movePrev
	
	level = []
	if currLevel == 1:
		level = [
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
			"P                                          P",
			"P                                          e",
			"P                                          e",
			"P                        PPPPPPPPP      PPPP",
			"P                  PP                      P",
			"P                PP                        P",
			"P                                          P",
			"P    PPPPPPPP                              P",
			"P            PP                            P",
			"P                          PPPPPPP         P",
			"P                 PPPPPP                   P",
			"P                                          P",
			"P         PPPPPPP                          P",
			"P       PP                                 P",
			"P                     PPPPPP               P",
			"P                                          P",
			"P   PPPPPPPPPPP                            P",
			"P                                          P",
			"P                                          P",
			"P                 PPPPPPPPPPP              P",
			"P                            PP            P",
			"P                              PP          P",
			"P                                          P",
			"P                                    K     P",
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
		total_level_width  = len(level[0])*16*3
		total_level_height = len(level)*16*3
		
		if movePrev:
			newX = total_level_width - 150
			newY = 164
		else:
			newX = total_level_width - 150
			newY = total_level_height - 80
		
	elif currLevel == 2:
		level = [	
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
			"e                                          P",
			"e                                          P",
			"PPP                                        P",
			"P                              PP          P",
			"P             PP                           P",
			"P      PP                             PP   P",
			"P                                    P     P",
			"P                    PP                    P",
			"P                            PP            P",
			"P                                          P",
			"P                                          P",
			"P                               PP         P",
			"P                                          P",
			"P                                          P",
			"P                                     PP   P",
			"P                                          P",
			"P                                          P",
			"P                              PP          P",
			"P                    PP                    P",
			"P                                          P",
			"P               P                          P",
			"P                                          P",
			"B        PP                                P",
			"B                                          P",
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
		total_level_width  = len(level[0])*16*3
		total_level_height = len(level)*16*3

		if movePrev:
			newX = 100
			newY = 150
		else:
			newX = 100
			newY = total_level_height - 80
	elif currLevel == 3:
		level = [	
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
			"                                                P",
			"F                                               P",
			"PPP                                             P",
			"P                                    P          P",
			"P       PP             PP                       P",
			"P               P              PP               P",
			"P                                        PP     P",
			"P                                               P",
			"P                                               P",
			"P                                     P         P",
			"P                                               P",
			"P                                PP             P",
			"P                       PP                      P",
			"P                      P                        P",
			"P                 P                             P",
			"P                                               P",
			"P              P                                P",
			"P                       P                       P",
			"P          PP                                   P",
			"P                              PP               P",
			"P                  P                            P",
			"P              PP           P                   P",
			"P                                               P",
			"P                                               P",
			"P                              PP               P",
			"P                                               P",
			"P                                               P",
			"P                                      PPP      P",
			"P                                               B",
			"P                                               B",
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
		total_level_width  = len(level[0])*16*3
		total_level_height = len(level)*16*3
		
		if movePrev:
			newX = total_level_width - 150
			newY = total_level_height - 80
		else:
			newX = total_level_width - 150
			newY = total_level_height - 80				 
	
	moveNext = False
	movePrev = False
	
	return level
	
#base entity that is used to create most objects
class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)


#player class that contains the image and position(rectangle)
#updates player position based on keypress and detects collision
class Player(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.xvel = 0
		self.yvel = 0
		self.faceright = True
		self.onGround = False
		self.airborne = True
		self.counter = 0
		self.image = knightstand1
		self.rect = Rect(x, y, 16*4, 32*3)

	def update(self, up, down, left, right, running, platforms):
		if up:
			# only jump if on the ground
			if self.onGround: self.yvel -= 10
		if down:
			pass
		if running:
			self.xvel = 12
		if left:
			self.xvel = -8
			self.faceright = False
		if right:
			self.xvel = 8
			self.faceright = True
		if not self.onGround:
			# only accelerate with gravity if in the air
			self.yvel += 0.35
			# max falling speed
			if self.yvel > 100: self.yvel = 100
		if not(left or right):
			self.xvel = 0
		if self.yvel < 0 or self.yvel > 1.2: self.airborne = True
		# increment in x direction
		self.rect.left += self.xvel
		# do x-axis collisions
		self.collide(self.xvel, 0, platforms)
		# increment in y direction
		self.rect.top += self.yvel
		# assuming we're in the air
		self.onGround = False;
		# do y-axis collisions
		self.collide(0, self.yvel, platforms)

		self.animate()

	#will perform different actions based on what the player
	#is colliding with
	def collide(self, xvel, yvel, platforms):
		global done
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if isinstance(p, PreviousBlock):
					global movePrev
					movePrev = True					
				if isinstance(p, ExitBlock):
					global moveNext
					moveNext = True				
				if isinstance(p, Princess):					
					done = True
				if isinstance(p, King):
					speech = pygame.image.load("images/king-dialogue.png").convert_alpha()
					screen.blit(speech, (440,450))			
				if xvel > 0:
					self.rect.right = p.rect.left
				if xvel < 0:
					self.rect.left = p.rect.right
				if yvel > 0:
					self.rect.bottom = p.rect.top
					self.onGround = True
					self.airborne = False
					self.yvel = 0
				if yvel < 0:
					self.rect.top = p.rect.bottom
	#Jump animations				
	def animate(self):
		if self.xvel > 0 or self.xvel < 0:
			self.walkloop()
			if self.airborne: self.updatecharacter(knightjump1)
		else:
			self.updatecharacter(knightstand1)
			if self.airborne: self.updatecharacter(knightjump1)
	#walk animations - done by alernating images
	def walkloop(self):
		if self.counter == 5:
			self.updatecharacter(knightwalk1)
		elif self.counter == 10:
			self.updatecharacter(knightwalk2)
		elif self.counter == 15:
			self.updatecharacter(knightwalk3)
			self.counter = 0
		self.counter = self.counter + 1

	def updatecharacter(self, ansurf):
		if not self.faceright: ansurf = pygame.transform.flip(ansurf,True,False)
		self.image = ansurf				
			
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
		self.image = pygame.image.load("images/exit-block.png").convert_alpha()
		self.image = pygame.transform.scale(self.image,(16*3,16*3))
		self.image.fill(Color("#0033FF"))
		self.rect = Rect(x, y, 16*3, 16*3)
		
#used to determine exit to the previous map
#currently image just set to blue filling for distinction
class PreviousBlock(Platform):
	def __init__(self, x, y):
		Platform.__init__(self, x, y)
		self.image.fill(Color("#0033FF"))
		

if __name__ == "__main__":
	main()

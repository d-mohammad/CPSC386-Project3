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

moveNext = False
movePrev = False
done = False

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
DEPTH = 32
FLAGS = 0
newX = 0
newY = 0
pygame.init()
screen = pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
pygame.display.set_caption("Use arrows to move!")

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
#action
KINGFLAG = 1
dialogFlag = 0
pygame.font.init()
dialogFont = pygame.font.SysFont("garuda", 20)
pygame.display.update()
white = (255,255,255)
black = (0,0,0)


def main():
	timer = pygame.time.Clock()
	currLevel = 1
	up = down = left = right = running = action = False
	platforms = []
	#bg = Background('bg1.png', 0, 0)
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0,0,0))
	bgImg = pygame.image.load('images/bg1.png')
	background.blit(bgImg, (0,0))
	screen.blit(background, (0,0))
	pygame.display.update()
	#bg = Surface((WIN_WIDTH,WIN_HEIGHT)).convert()
	entities = pygame.sprite.Group()
   
	x = y = 0
	level = getLevel(currLevel)

	
	# build the level
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
				
					
			if col == "f":
				f = ExitBlock2(x, y)
				platforms.append(f)
				entities.add(f)
						
			if col == "g":
				g = ExitBlock3(x, y)
				platforms.append(g)
				entities.add(g)
				
			if col == "B":
				B = PreviousBlock(x, y)
				platforms.append(B)
				entities.add(B)
				
			if col == "b":
				b = PreviousBlock2(x, y)
				platforms.append(b)
				entities.add(b)	
					
			if col == "K":
				k = King(x, y)
				platforms.append(k)
				entities.add(k)
					
			x += 16*3
		y += 16*3
		x = 0

	total_level_width  = len(level[0])*16*3
	total_level_height = len(level)*16*3
	camera = Camera(complex_camera, total_level_width, total_level_height)
	player = Player(newX, newY)
	entities.add(player)

	while 1:
		timer.tick(60)
		
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
			if e.type == KEYDOWN and e.key == K_SPACE:
				action = True
			if e.type == KEYUP and e.key == K_UP:
				up = False
			if e.type == KEYUP and e.key == K_DOWN:
				down = False
			if e.type == KEYUP and e.key == K_RIGHT:
				right = False
			if e.type == KEYUP and e.key == K_LEFT:
				left = False
			if e.type == KEYUP and e.key == K_SPACE:
				action = False
			
		#screen.blit(bg,(0,0))
		screen.blit(background,(0,0))
		camera.update(player)
		# update player, draw everything else
		player.update(up, down, left, right, running, platforms, action)     
		
		#if reached portal, reset variables and draw next map
		if (moveNext == True or movePrev == True):
			x=0
			y=0
			if moveNext:
				currLevel = currLevel + 1
			if movePrev:
				currLevel = currLevel - 1			
			
			platforms=[]
			level = getLevel(currLevel)
			
			if done:
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
						
					if col == "f":
						f = ExitBlock2(x, y)
						platforms.append(f)
						entities.add(f)
						
					if col == "g":
						g = ExitBlock3(x, y)
						platforms.append(g)
						entities.add(g)
					
						
					if col == "B":
						B = PreviousBlock(x, y)
						platforms.append(B)
						entities.add(B)
						
					if col == "b":
						b = PreviousBlock2(x, y)
						platforms.append(b)
						entities.add(b)
						
					if col == "K":
						k = King(x, y)
						platforms.append(k)
						entities.add(k)
					
						
					x += 16*3
				y += 16*3
				x = 0

			total_level_width  = len(level[0])*16*3
			total_level_height = len(level)*16*3
			camera = Camera(complex_camera, total_level_width, total_level_height)
			player = Player(newX, newY)
			entities.add(player)
			sleep(.2)
		for e in entities:
			screen.blit(e.image, camera.apply(e))
		pygame.display.update()
	
	
	font = pygame.font.Font(None, 50)
	BLACK = (0,0,0)
	text = font.render("Game Over", True, BLACK)
	text_rect = text.get_rect()
	text_x = WIN_WIDTH / 2 - text_rect.width / 2
	text_y = WIN_HEIGHT / 2 - text_rect.height / 2

	screen.blit(text, [text_x, text_y])
	pygame.display.update()
	sleep(2)
	
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

def getLevel(currLevel):
	global newX
	global newY
	global moveNext
	global movePrev
	global done
	level = []
	if currLevel == 1:
		level = [
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
			"P                                          P",
			"P                                           ",
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
			"P                                         KP",
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
		total_level_width  = len(level[0])*16*3
		total_level_height = len(level)*16*3
		
		if movePrev:
			newX = total_level_width - 150
			newY = 164
		else:
			newX = total_level_width - 300
			newY = total_level_height - 80
		
	elif currLevel == 2:
		level = [	
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
			"                                           P",
			"f                                          P",
			"PPPP                                       P",
			"P                              PP          P",
			"P         P   PP                           P",
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
			"         PP                                P",
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
			"g                                               P",
			"PPP                                             P",
			"P            PP                        P        P",
			"P                      PP                       P",
			"P     P                         PP              P",
			"P                                        PP     P",
			"P                PP                             P",
			"P  P                                            P",
			"P                                     P         P",
			"P        PP                                     P",
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
			"P                                                ",
			"P                                               b",
			"PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
		total_level_width  = len(level[0])*16*3
		total_level_height = len(level)*16*3
		
		if movePrev:
			newX = total_level_width - 150
			newY = total_level_height - 80
		else:
			newX = total_level_width - 150
			newY = total_level_height - 80
				  
	elif currLevel == 4:
		level = ["PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",
				 "                                                 ",
				 "                                                 ",
				 "                                                 ",
				 "PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",]
		done = True
	
	moveNext = False
	movePrev = False
	
	return level
	
class Entity(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

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

	def update(self, up, down, left, right, running, platforms, action):
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
		self.collide(self.xvel, 0, platforms, action)
		# increment in y direction
		self.rect.top += self.yvel
		# assuming we're in the air
		self.onGround = False;
		# do y-axis collisions
		self.collide(0, self.yvel, platforms, action)

		self.animate()

	def collide(self, xvel, yvel, platforms, action):
		for p in platforms:
			if pygame.sprite.collide_rect(self, p):
				if isinstance(p, PreviousBlock):
					global movePrev
					movePrev = True
					
				if isinstance(p, PreviousBlock2):
					global movePrev
					movePrev = True
					
				if isinstance(p, ExitBlock):
					#go to next level based on currLevel variable
					a = dialogFont.render("You found me!", True, white)
					b = dialogFont.render("Level passed" , True, white)
					pygame.draw.rect(screen, black, (400, 400, 300, 100), 0)
					screen.blit(a, (400, 400))
					screen.blit(b, (400, 430))
					pygame.display.update()
					sleep(3)
					global moveNext
					moveNext = True
					#pygame.event.post(pygame.event.Event(QUIT))
					
				
				if isinstance(p, King):
					getAction(action, KINGFLAG)
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
	def animate(self):

		if self.xvel > 0 or self.xvel < 0:
			self.walkloop()
			if self.airborne: self.updatecharacter(knightjump1)
		else:
			self.updatecharacter(knightstand1)
			if self.airborne: self.updatecharacter(knightjump1)

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
#action
def getAction(action, flag):
	#kingFlag  
	global dialogFlag
	if action:  
		if(flag == 1):
			if(dialogFlag == 0):
				a = dialogFont.render("Can you please help find", True, white)
				b = dialogFont.render("my daughter I think she's" , True, white)
				c = dialogFont.render("around here somewhere" , True, white)
				pygame.draw.rect(screen, black, (400, 400, 300, 100), 0)
				screen.blit(a, (400, 400))
				screen.blit(b, (400, 430))
				screen.blit(c, (400, 460))
				pygame.display.update()
				sleep(3)
				
				dialogFlag = dialogFlag + 1
			elif(dialogFlag == 1):
				a = dialogFont.render("Hurry!", True, white)
				pygame.draw.rect(screen, black, (500, 500, 100, 25), 0)
				screen.blit(a, (500, 500))
				
	
			
			
class Platform(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/block.png").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3))
		self.rect = Rect(x, y, 16*3, 16*3)

	def update(self):
		pass

class King(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/king.png").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)
		
class Background(Entity):
	def __init__(self, image, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load(image).convert()
		
		
class ExitBlock(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/princess.jpg").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)
		
class ExitBlock2(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/p2.png").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)
		
class ExitBlock3(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/p3.png").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)		
		
class PreviousBlock(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/princess.jpg").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)
		
class PreviousBlock2(Entity):
	def __init__(self, x, y):
		Entity.__init__(self)
		self.image = pygame.image.load("images/p2.png").convert()
		self.image = pygame.transform.scale(self.image,(16*3,16*3*2))
		self.rect = Rect(x, y-16*3, 16*3, 16*3*2)
		
		
if __name__ == "__main__":
	main()

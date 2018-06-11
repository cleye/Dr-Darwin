import pygame 
import sys
import numpy as np
import math
from button import Button
from math import pi, e
from random import randint 
from pygame.locals import *

pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width,height))

# time of last frame in milliseconds
frame_time = 0.0

LEVEL = '''
background
(31, 31, 94)
..#................#..
...#..............#...
....#............#....
.....#..........#.....
......#........#......
.......#......#.......
.......#..............
.......#..............
......................
......................
......................
'''.split("\n")

MUTANT_SPRITE = "resources/mutant.bmp"
PLAYER_SPRITE = "resources/player.bmp"

'''class Renderer:
	def __init__(self):
		pass

	def render_level(self):
'''
def sin(angle):
	return math.sin(math.radians(angle))
def sin_r(angle):
	return math.sin(angle)

def cos(angle):
	return math.cos(math.radians(angle))
def cos_r(angle):
	return math.cos(angle)

def atan(angle):
	return math.degrees(math.atan(angle))
def atan2(x, y):
	return math.degrees(math.atan2(y, x))

def dist(a, b):
	''' Distance between point a and point b '''
	return math.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

def g(z):
	try:
		result = (1 / (1 + e**-z)) 
	except:
		print("oh shoot:)")

	return result


class Player:
	def __init__(self):
		self.og_image = pygame.image.load(PLAYER_SPRITE).convert()
		self.image = self.og_image
		self.rect = self.image.get_rect()

		self.x = width/2
		self.y = height-30
		self.bullets = []

		self.vel = 0
		self.direction = 0#45

	def display(self):

		# move
		self.x += self.vel * sin(self.direction)
		self.y += self.vel * cos(self.direction)

		# rotate
		self.image = pygame.transform.rotate(self.og_image, self.direction)
		
		# position
		self.rect = self.image.get_rect()  # Replace old rect with new rect.
		self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.

		screen.blit(self.image, self.rect)

		pygame.draw.line(screen, (2,100,2),   ( self.x , self.y ),  ( self.x+40*sin(self.direction), self.y+40*cos(self.direction)), 2  ) 
		

		for b in self.bullets:
			b.display()

	def shoot(self):
		self.bullets.append(Bullet( self.x+12*sin(self.direction), self.y+12*cos(self.direction), self.direction))


class Bullet:
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.direction = direction
		self.speed = 3

	def display(self):
		self.x += self.speed*sin(self.direction)
		self.y += self.speed*cos(self.direction)
		pygame.draw.circle(screen, (255,60,60), (int(self.x), int(self.y)), 5)


class Creature:
	def __init__(self):
		self.og_image = pygame.image.load(MUTANT_SPRITE).convert()
		self.image = self.og_image
		self.rect = self.image.get_rect()
		self.x = randint(20,width-20)#width/2#randint(20,width-20)
		self.y = 20#height/2#randint(20,height-20)
		self.direction = randint(0, 359)
		self.periphery = 108 # degree of vision
		self.energy = 100

		self.left_sensor_pos = (self.x + cos(135-self.direction)*20.5, self.y + sin(135-self.direction)*20.5) 
		self.right_sensor_pos = (self.x + cos(45-self.direction)*20.5, self.y + sin(45-self.direction)*20.5)
		self.left_sensor_detect = 0
		self.right_sensor_detect = 0

		self.distance2player = 0

		# Numbers of neurons in each layer
		self.s = (None, 3, 6, 3)

		# Theta values
		self.T1 = np.random.random((self.s[2], self.s[1]+1)) * 10 - 5
		self.T2 = np.random.random((self.s[3], self.s[2]+1)) * 10 - 5


	def display(self):
		global game
		p = game.player

		#move direction

		# inputs to NN including bias unit
		inupts = np.array((1, self.left_sensor_detect, self.right_sensor_detect, self.distance2player / dist((0,0), (width, height)) ) )

		

		decision = self.make_decision(inupts, self.T1, self.T2)  #randint(-200,100)/100.

		rand = decision[0]*8-4


		# move

		collided_x = (self.x < 0 or self.x > width)
		collided_y = (self.y < 0 or self.y > height)

		if not (collided_x or collided_y):
			self.direction += rand*1
			self.x += 2.5*decision[2]*sin(self.direction)
			self.y += 2.5*decision[2]*cos(self.direction)

		# rotate
		self.image = pygame.transform.rotate(self.og_image, self.direction)
		
		# position
		self.rect = self.image.get_rect()  # Replace old rect with new rect.
		self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.




		screen.blit(self.image, self.rect)

		self.left_sensor_pos = (self.x + cos(self.direction-45)*0, self.y + sin(self.direction+45+90)*0) 
		self.right_sensor_pos = (self.x + cos(self.direction-45-90)*0, self.y + sin(self.direction+45)*0)

		angle = atan2( (self.x - p.x), (self.y - p.y) )+180

		#print (angle + self.direction)%360


		# check sensor detects player

		if 360-self.periphery+90 < (angle + self.direction)%360 or (angle + self.direction)%360 < self.periphery:
			self.left_sensor_detect = True
		else:
			self.left_sensor_detect = False


		if self.periphery+90 > (angle + self.direction)%360 > 180-self.periphery :
			self.right_sensor_detect = True
		else:
			self.right_sensor_detect = False


		pygame.draw.polygon(screen, (100,2,2),   ( (self.left_sensor_pos[0] + cos(-self.periphery+90-self.direction)*20, self.left_sensor_pos[1] + sin(-self.periphery+90-self.direction)*20), self.left_sensor_pos, (self.left_sensor_pos[0] + cos(self.periphery-self.direction)*20, self.left_sensor_pos[1] + sin(self.periphery-self.direction)*20)), 0 if self.left_sensor_detect else 2  ) 
		pygame.draw.polygon(screen, (100,2,2),   ( (self.right_sensor_pos[0] + cos(self.periphery+90-self.direction)*20, self.right_sensor_pos[1] + sin(self.periphery+90-self.direction)*20), self.right_sensor_pos, (self.right_sensor_pos[0] + cos(180-self.periphery-self.direction)*20, self.right_sensor_pos[1] + sin(180-self.periphery-self.direction)*20)), 0 if self.right_sensor_detect else 2  ) 
		

		#pygame.draw.line(screen, (2,100,2),   ( p.x , p.y ),  ( self.x, self.y), 2  ) 
		


		self.distance2player = dist((self.x, self.y), (p.x, p.y) )



	def make_decision(self, inputs, T1, T2):

		# LAYER 1 (input layer)		
		# Add bias units 
		#print inputs		

		# LAYER 2 (hidden layer)			
		# Sum up parameters with dot product
		z = np.dot(T1, inputs)					
		# Activation units for layer 2		
		a2 = g(z)							
		# Add bias units 					
		a2 = np.insert(a2, 0, 1)	


		# LAYER 3 (output layer)
		# Sum up parameters with dot product
		z = np.dot(T2, a2)
		# Activation units for layer 3 (output units)	
		a3 = g(z)

		# Return all activation units
		#print a3
		return a3


class Level:
	def __init__(self, matrix):
		self.colours = matrix[2]
		self.map = matrix[3:]
		self.w = len(self.map[0])
		self.h = len(self.map)



	def display(self):
		for i in range(self.h-1):
			for j in range(self.w-1):
				if self.map[i][j] == "#":
					pygame.draw.rect(screen, (200,200,200), (j*width/self.w, i*height/self.h, width/self.w, height/self.h))


class Game:
	STATE_MAIN_MENU = 0
	STATE_IN_GAME = 1

	def __init__(self):

		self.state = Game.STATE_MAIN_MENU

		self.key_right = False
		self.key_left = False
		self.key_up = False
		self.key_down = False
		self.key_space = False

		self.level = Level(LEVEL)
		self.player = Player()



		self.play_button = Button("Play", (40, 160))
		def play_action():
			self.state = Game.STATE_IN_GAME
		self.play_button.mouse_up = play_action


		self.creatures = []
		for i in range(10):
			dude = Creature()
			self.creatures.append(dude)


	def run(self):
		done = False

		while not done:
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()

				if event.type == KEYDOWN:
					if event.key == K_RIGHT: 
						self.key_right = True				
					if event.key == K_LEFT:
						self.key_left = True
					if event.key == K_UP: 
						self.key_up = True				
					if event.key == K_DOWN:
						self.key_down = True			
					if event.key == K_SPACE:
						self.key_down = True
						self.player.shoot()

				if event.type == KEYUP:
					if event.key == K_RIGHT: 
						self.key_right = False
					if event.key == K_LEFT:
						self.key_left = False
					if event.key == K_UP: 
						self.key_up = False				
					if event.key == K_DOWN:
						self.key_down = False		
					if event.key == K_SPACE:
						self.key_down = False

			if self.state == Game.STATE_MAIN_MENU:
				header_font = pygame.font.SysFont("Corbel", 50)
				header_image = header_font.render("Darwin", False, (255,255,255))

				screen.blit(header_image, (40, 40))

				self.play_button.add(screen)


			if self.state == Game.STATE_IN_GAME:
				screen.fill((0,0,0))

				for dude in self.creatures:
					dude.display()
				
				self.player.display()
				#self.level.display()


				if self.key_right:
					self.player.direction -= 2.5
					print self.player.direction
				if self.key_left:
					self.player.direction += 2.5
					print self.player.direction

				if self.key_up:
					self.player.vel = 2
				else:
					self.player.vel = 0




			pygame.display.update()



c = []
for i in range(10):
	dude = Creature()
	c.append(dude)

game = Game()
game.run()
l = Level(LEVEL)





'''

INPUTS

bias_unit    left_distance2player    right_distance2player     left_distance2wall    right_distance2wall


HIDDEN LAYER (4)


OUTPUTS     

turn (0-left 0.5-straight 1-right)      shoot      


ideas
------
the creatures have limited energy and moving uses up their energy
parameter of how close it is to wall
overall timer (20s)


use the sensors like eyes, only detect player/wall if its in a specific angle range
fitness: do damage to player'''


'''
	#pygame.draw.line(screen, (255,255,255), (p.x, p.y), (c[0].x, c[0].y))
	a = math.radians(c[0].direction)
	#print (cos(a)*29 + sin(a)*32, cos(a)*32 + sin(a)*29)
	#pygame.draw.line(screen, (200,200,255), (p.x, p.y), (c[0].x + sin(a)*29 + cos(a)*32, c[0].y + cos(a)*20) )
	#pygame.draw.line(screen, (200,200,255), (p.x, p.y), (c[0].x - sin(a)*20, c[0].y - cos(a)*20) )
	#
	l = 80
	print c[0].image.get_rect()
	
	#pygame.draw.line(screen, (200,200,255), (p.x, p.y), ( width/2,  c[0].rect.topleft[1] + sin(a)*29/2 + cos(a)*32/2) )
	pygame.draw.line(screen, (200,200,255), (p.x, p.y), (  c[0].rect.topleft[0],  c[0].rect.topleft[1]) )

	pygame.draw.line(screen, (200,200,255), (0, c[0].rect.topleft[1]), (width, c[0].rect.topleft[1]) )

	pygame.draw.polygon(screen, (255,200,200), (c[0].rect.topleft, c[0].rect.topright, c[0].rect.bottomright, c[0].rect.bottomleft), 1 )
	pygame.draw.ellipse(screen, (200,255,200), (width/2-32/2, height/2-29/2, 32, 32), 1 )'''
		   	
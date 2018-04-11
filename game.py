import pygame 
import sys
import numpy as np
import math
from math import pi, e
from random import randint 
from pygame.locals import *

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width,height))

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

def dist(a, b):
	return math.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

def g(z):
	try:
		result = (1 / (1 + e**-z)) 
	except:
		print("ph shoot:)")

	return result


class Player:
	def __init__(self):
		self.og_image = pygame.image.load(PLAYER_SPRITE).convert()
		self.image = self.og_image

		self.x = width/2
		self.y = height-30

		self.vel = 2
		self.direction = 0

	def display(self):
		a = math.radians(self.direction) % pi

		self.image = pygame.transform.rotate(self.og_image, self.direction)
		screen.blit(self.image, (self.x, self.y))

	def move_by(self, dx, dy):
		self.x += dx
		self.y += dy


class Creature:
	def __init__(self):
		self.og_image = pygame.image.load(MUTANT_SPRITE).convert()
		self.image = self.og_image
		self.rect = self.image.get_rect()
		self.x = width/2#randint(20,width-20)
		self.y = height/2#randint(20,height-20)
		self.direction = randint(0, 359)

		self.left_sensor = (self.x + cos(135-self.direction)*20.5, self.y + sin(135-self.direction)*20.5) 
		self.right_sensor = (self.x + cos(45-self.direction)*20.5, self.y + sin(45-self.direction)*20.5)

		# Numbers of neurons in each layer
		self.s = (None, 2, 4, 2)

		# Theta values
		self.T1 = np.random.random((self.s[2], self.s[1]+1)) * 4 - 2
		self.T2 = np.random.random((self.s[3], self.s[2]+1)) * 4 - 2


	def display(self):
		global p

		#move direction

		# inputs to NN including bias unit
		inupts = np.array((1, dist(self.left_sensor, (p.x, p.y) ), dist(self.right_sensor, (p.x, p.y) ) ) )

		decision = self.make_decision(inupts, self.T1, self.T2)  #randint(-200,100)/100.

		'''if decision[0] > decision[1]:
			rand = -1
		elif decision[2] > decision[0] and decision[2] > decision[1]:
			rand = 0
		else:
			rand = 1'''
		rand = decision[0]*2-1

		self.direction += rand*1 % 360

		# move

		collided_x = True#(self.x < 0 or self.x > width)
		collided_y = True#(self.y < 0 or self.y > height)

		if self.x < 0:
			self.x = 1
		if not collided_x:
			self.x += 0.8*sin(self.direction)
		if not collided_y:
			self.y += 0.8*cos(self.direction)

		# rotate
		self.image = pygame.transform.rotate(self.og_image, self.direction)
		
		# position
		self.rect = self.image.get_rect()  # Replace old rect with new rect.
		self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.




		screen.blit(self.image, self.rect)

		self.left_sensor = (self.x + cos(135-self.direction)*20.5, self.y + sin(135-self.direction)*20.5) 
		self.right_sensor = (self.x + cos(45-self.direction)*20.5, self.y + sin(45-self.direction)*20.5)


		# draw sensors
		'''pygame.draw.line(screen, (200,200,255), (self.x + cos(115-self.direction)*100, self.y + sin(115-self.direction)*100), (self.x + cos(135-self.direction)*20.5, self.y + sin(135-self.direction)*20.5) ) 
		pygame.draw.line(screen, (200,200,255), (self.x + cos(65-self.direction)*100, self.y + sin(65-self.direction)*100), (self.x + cos(45-self.direction)*20.5, self.y + sin(45-self.direction)*20.5) ) 
		'''


		#pygame.draw.line(screen, (200,200,255), (self.left_sensor[0] + cos(195-self.direction)*100, self.left_sensor[1] + sin(195-self.direction)*100), self.left_sensor ) 
		#pygame.draw.line(screen, (200,200,255), (self.left_sensor[0] + cos(75-self.direction)*100, self.left_sensor[1] + sin(75-self.direction)*100), self.left_sensor ) 

		pygame.draw.polygon(screen, (100,2,2),   ( (self.left_sensor[0] + cos(195-self.direction)*1000, self.left_sensor[1] + sin(195-self.direction)*1000), self.left_sensor, (self.left_sensor[0] + cos(75-self.direction)*1000, self.left_sensor[1] + sin(75-self.direction)*1000)), 2  ) 
		pygame.draw.polygon(screen, (100,2,2),   ( (self.right_sensor[0] + cos(-15-self.direction)*1000, self.right_sensor[1] + sin(-15-self.direction)*1000), self.right_sensor, (self.right_sensor[0] + cos(105-self.direction)*1000, self.right_sensor[1] + sin(105-self.direction)*1000)), 2  ) 
		
		#print dist(self.left_sensor, (width/2, height-30) )



	def make_decision(self, inputs, T1, T2):

		# LAYER 1 (input layer)		
		# Add bias units 
									

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
	def __init__(self):
		self.key_right = False
		self.key_left = False
		self.key_up = False


c = []
for i in range(1):
	dude = Creature()
	c.append(dude)

p = Player()
G = Game()
l = Level(LEVEL)


while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == KEYDOWN:
			if event.key == K_RIGHT: 
				G.key_right = True				

			if event.key == K_LEFT:
				G.key_left = True

		if event.type == KEYUP:
			if event.key == K_RIGHT: 
				G.key_right = False
			if event.key == K_LEFT:
				G.key_left = False

	
	screen.fill((0,0,0))

	for dude in c:
		dude.display()
	p.display()


	#l.display()


	if G.key_right:
		p.move_by(p.vel*cos(math.radians(p.direction)), 0)
	if G.key_left:
		p.move_by(-p.vel*cos(math.radians(p.direction)), 0)


	#pygame.draw.polygon(screen, (255,200,200), (c[0].rect.topleft, c[0].rect.topright, c[0].rect.bottomright, c[0].rect.bottomleft), 1 )

	pygame.display.update()




'''

INPUTS

bias_unit    left_distance2player    right_distance2player     left_distance2wall    right_distance2wall


HIDDEN LAYER (4)


OUTPUTS     

turn (0-left 0.5-straight 1-right)      shoot      



use the sensors like eyes, only detect player/wall if its in a specific angle range

'''




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
		   	
import pygame 
import sys
import numpy as np
import math
from button import Button
from math import pi, e
from random import randint, random
from pygame.locals import *

pygame.init()
width = 1000
height = 600
screen = pygame.display.set_mode((width,height))

# time of last frame in milliseconds
frame_time = 0.0
#gameplay_time = 0.0

# number of frames
frame = 1

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
GAME_SONG = "resources/abnormal.ogg"

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

def angle_between(a, b):
	''' Angle between point a and b 

		  135			   45
	 	  b *			  * b 

				  * a     * b 0

		    
			* b   * b   
			225   270
	'''
	return -atan2( a[0]-b[0], a[1]-b[1] )+180

def wall_proximity(x,y):
	''' Returns a number proportional to the square distance to wall '''
	_x = _y = 0
	if x < 60:
		_x = (x-60)**2 / 1000
	if x > width-60:
		_x = (x-(width-60))**2 / 1000
	if y < 60:
		_y = (y-60)**2 / 1000
	if y > height-60:
		_y = (y-(height-60))**2 / 1000
	return (_x + _y)/2

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
		self.health = 100

		self.vel = 0
		self.direction = 180

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

		# draw health bar
		pygame.draw.rect(screen, (60,190,100), (self.x-30, self.y-20, self.health*60/100, 6), 0)
		pygame.draw.rect(screen, (255,255,255), (self.x-30, self.y-20, 60, 6), 1)


		for index, b in enumerate(self.bullets):
			if b.outside_screen():
				self.bullets.remove(b)
			b.display()


	def shoot(self):
		self.bullets.append(Bullet( self.x+12*sin(self.direction), self.y+12*cos(self.direction), self.direction%360))

	def reset(self):
		self.x = width/2
		self.y = height-30
		self.bullets = []
		self.health = 100

		self.vel = 0
		self.direction = 180


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

	def outside_screen(self):
		return (self.x < 0 or self.x > width) or (self.y < 0 or self.y > height)


class Creature:
	def __init__(self, _id, T1=None, T2=None):
		self.og_image = pygame.image.load(MUTANT_SPRITE).convert()
		self.image = self.og_image
		self.rect = self.image.get_rect()
		self.x = randint(40,width-40)     #width/2#randint(20,width-20)
		self.y = randint(80,140)   #20#height/2#randint(20,height-20)
		self.direction = randint(0, 359)

		self.id = _id
		self.periphery = 108 # degree of vision
		self.health = 100
		self.alive = True

		self.fitness = 0
		self.fitness_rewards = 0
		self.fitness_punish = 0
		self.avg_distance2player = 0
		self.frame_since_last_attack = 0


		self.distance2player = 9999

		# Numbers of neurons in each layer
		self.s = (None, 6, 4, 2)

		''' Theta values
		bias_unit 					10	-5
		left_sensor_detect 			10	-5
		right_sensor_detect 		10	-5
		distance2player  			16	-8
		left_sensor_detect_bullet 	20	-10	
		right_sensor_detect_bullet 	20	-10
		wall_proximity 				20	-10
		'''
		if T1 is None:
			weights = [10,10,10,16,20,20,20] #10 #[10,10,10,16,20,20,20]
			bias = [-5,-5,-5,-8,-10,-10,-10] #-5 #[-5,-5,-5,-8,-10,10,10]
			self.T1 = np.random.random((self.s[2], self.s[1]+1)) * weights + bias
		else:
			self.T1 = T1

		if T2 is None:
			self.T2 = np.random.random((self.s[3], self.s[2]+1)) * 10 - 5
		else:
			self.T2 = T2


	def display(self):
		# parameters
		left_sensor_detect = 0
		right_sensor_detect = 0
		left_sensor_detect_bullet = 0
		right_sensor_detect_bullet = 0
		wall_proximity_ = 0

		p = game.player



		screen.blit(self.image, self.rect)

		left_sensor_pos = (self.x + cos(self.direction-45)*10, self.y + sin(self.direction+45+90)*10) 
		right_sensor_pos = (self.x + cos(self.direction-45-90)*10, self.y + sin(self.direction+45)*10)


		#angle = atan2( (self.x - p.x), (self.y - p.y) )+180
		angle = angle_between((self.x, self.y), (p.x, p.y))
		#print angle

		# check sensor detects player
		if 360-self.periphery+90 < (-angle + self.direction)%360 or (-angle + self.direction)%360 < self.periphery:
			left_sensor_detect = 1
		else:
			left_sensor_detect = 0


		if self.periphery+90 > (-angle + self.direction)%360 > 180-self.periphery :
			right_sensor_detect = 1
		else:
			right_sensor_detect = 0

		# check sensor detects bullets
		left_sensor_detect_bullet = 0
		right_sensor_detect_bullet = 0
		hit_by_bullet = 0
		for b in p.bullets:
			angle = angle_between( (self.x, self.y), (b.x, b.y) )

			# if bullet is moving in direction of creature
			if -45 > p.direction - angle > -135:
				if 360-self.periphery+90 < (-angle + self.direction)%360 or (-angle + self.direction)%360 < self.periphery:
					left_sensor_detect_bullet = 1
				else:
					left_sensor_detect_bullet = 0


				if self.periphery+90 > (-angle + self.direction)%360 > 180-self.periphery :
					right_sensor_detect_bullet = 1
				else:
					right_sensor_detect_bullet = 0

			if dist((b.x, b.y), (self.x, self.y)) < 20:
				self.health -= randint(20,50)
				hit_by_bullet = 1
				p.bullets.remove(b)


		wall_proximity_ = wall_proximity(self.x, self.y)



		# draw sensors to player
		#pygame.draw.polygon(screen, (100,2,2),   ( (left_sensor_pos[0] + cos(-self.periphery+90-self.direction)*20, left_sensor_pos[1] + sin(-self.periphery+90-self.direction)*20), left_sensor_pos, (left_sensor_pos[0] + cos(self.periphery-self.direction)*20, left_sensor_pos[1] + sin(self.periphery-self.direction)*20)), 0 if left_sensor_detect else 2  ) 
		#pygame.draw.polygon(screen, (100,2,2),   ( (right_sensor_pos[0] + cos(self.periphery+90-self.direction)*20, right_sensor_pos[1] + sin(self.periphery+90-self.direction)*20), right_sensor_pos, (right_sensor_pos[0] + cos(180-self.periphery-self.direction)*20, right_sensor_pos[1] + sin(180-self.periphery-self.direction)*20)), 0 if right_sensor_detect else 2  ) 

		pygame.draw.ellipse(screen, (20,130,220), (left_sensor_pos[0]-8, left_sensor_pos[1]-8, 16, 16))
		pygame.draw.ellipse(screen, (20,130,220), (right_sensor_pos[0]-8, right_sensor_pos[1]-8, 16, 16))

		if left_sensor_detect_bullet:
			pygame.draw.ellipse(screen, (230,130,130), (left_sensor_pos[0]-6, left_sensor_pos[1]-6, 12, 12))
		if right_sensor_detect_bullet:
			pygame.draw.ellipse(screen, (230,130,130), (right_sensor_pos[0]-6, right_sensor_pos[1]-6, 12, 12))
		
		if left_sensor_detect:
			pygame.draw.ellipse(screen, (100,230,20), (left_sensor_pos[0]-4, left_sensor_pos[1]-4, 8, 8))
		if right_sensor_detect:
			pygame.draw.ellipse(screen, (100,230,20), (right_sensor_pos[0]-4, right_sensor_pos[1]-4, 8, 8))

		# draw sensors to bullets
		#pygame.draw.polygon(screen, (2,180,2),   ( (left_sensor_pos[0] + cos(-self.periphery+90-self.direction)*20, left_sensor_pos[1] + sin(-self.periphery+90-self.direction)*20), left_sensor_pos, (left_sensor_pos[0] + cos(self.periphery-self.direction)*20, left_sensor_pos[1] + sin(self.periphery-self.direction)*20)), 0 if left_sensor_detect_bullet else 2  ) 
		#pygame.draw.polygon(screen, (2,180,2),   ( (right_sensor_pos[0] + cos(self.periphery+90-self.direction)*20, right_sensor_pos[1] + sin(self.periphery+90-self.direction)*20), right_sensor_pos, (right_sensor_pos[0] + cos(180-self.periphery-self.direction)*20, right_sensor_pos[1] + sin(180-self.periphery-self.direction)*20)), 0 if right_sensor_detect_bullet else 2  ) 
		

		# draw health
		#pygame.draw.rect(screen, (255,100,70), (self.x-30, self.y-20, 60, 6))
		pygame.draw.rect(screen, (60,190,100), (self.x-30, self.y-20, self.health*60/100, 6), 0)
		pygame.draw.rect(screen, (255,255,255), (self.x-30, self.y-20, 60, 6), 1)

		#pygame.draw.line(screen, (2,100,2),   ( p.x , p.y ),  ( self.x, self.y), 2  ) 
		
		# draw id
		font = pygame.font.SysFont("Corbel", 20)
		screen.blit(font.render(str(self.id), True, (255,255,255)), (self.x-5, self.y-8))

		does_damage_to_player = 0
		if self.distance2player < 26:
			# cant do damage with one touch
			if frame - self.frame_since_last_attack > 20:
				self.frame_since_last_attack = frame
				p.health -= 4
				does_damage_to_player = 1

		if self.health < 0:
			self.die()


		#move direction

		# inputs to NN including bias unit
		inupts = np.array((1, left_sensor_detect, right_sensor_detect, self.distance2player / dist((0,0), (width, height)), left_sensor_detect_bullet, right_sensor_detect_bullet, wall_proximity_ ) )

		[output_direction, output_velocity] = self.make_decision(inupts, self.T1, self.T2)  #randint(-200,100)/100.

		# move
		collided_x = (self.x < 0 or self.x > width)
		collided_y = (self.y < 0 or self.y > height)

		hit_wall = 0
		if (collided_x or collided_y):
			hit_wall = 1
			self.die()
		else:
			self.direction += output_direction*6-3
			self.x += 1.6*output_velocity*sin(self.direction)
			self.y += 1.6*output_velocity*cos(self.direction)
			self.health -= output_velocity*0.04

		# rotate
		self.image = pygame.transform.rotate(self.og_image, self.direction)
		
		# position
		self.rect = self.image.get_rect()  # Replace old rect with new rect.
		self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.

		# calculate average distance to player
		# could use timestep to do this
		self.distance2player = dist((self.x, self.y), (p.x, p.y))
		if game.play_time == 0:
			self.avg_distance2player = self.distance2player
		else:
			self.avg_distance2player = (self.distance2player + self.avg_distance2player*(frame-1) ) / (frame)

		# detects if stationary
		stationary = 0
		if output_velocity < 0.1:
			stationary = 1


		self.fitness = ( (dist((0,0), (width, height)) - self.avg_distance2player) / 100. )**2
		''' rewards:
		damage done on player
		velocity
		average distance to player
		time with player in sight
		--ability to sense bullets and dodge them--
		'''
		self.fitness_rewards += does_damage_to_player*40 + left_sensor_detect/200. + right_sensor_detect/200. + output_velocity/40.

		''' punishes:
		being stationary
		running into walls
		hitting bullets
		'''
		self.fitness_punish += stationary/10. + hit_by_bullet*10 + hit_wall*10

		self.fitness += (self.fitness_rewards - self.fitness_punish)

		#print self.distance2player, self.fitness


	def make_decision(self, inputs, T1, T2):

		# LAYER 1 (input layer)		
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

	def die(self):
		# TODO add animation
		self.alive = False

	def mutated_child(self, _id, mutability=0.07):
		# new theta values (chromosomes) come from multiplying current theta values by random amount
		T1 = self.T1 * (1 + np.random.random((self.s[2], self.s[1]+1))*mutability)
		T2 = self.T2 * (1 + np.random.random((self.s[3], self.s[2]+1))*mutability)

		return Creature(_id, T1, T2)

'''class Level:
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
'''

class Game:
	STATE_MAIN_MENU = 0
	STATE_GAMEPLAY = 1

	def __init__(self):

		self.state = Game.STATE_MAIN_MENU

		self.key_right = False
		self.key_left = False
		self.key_up = False
		self.key_down = False
		self.key_space = False

		self.player = Player()

		# time that gameplay started
		self.play_start = 0
		self.play_time = 0

		self.creatures = []
		self.generation = 0

		self.play_button = Button("Play", (40, 160))
		def play_action():
			self.state = Game.STATE_GAMEPLAY
			self.new_generation()
			self.play_start = pygame.time.get_ticks()
			pygame.mixer.music.play(-1)
		self.play_button.mouse_up = play_action

		

	def new_generation(self, population=20):
		# if first generation create new creatures
		if self.generation == 0:
			for i in range(population):
				c = Creature(i)
				self.creatures.append(c)
		# otherwise mutate and create new creatures
		else:
			# fitnesses of all creatures
			fitnesses = np.array([dude.fitness for dude in self.creatures])
			# convert fitnesses into weighted probabilities
			_weights = (fitnesses - min(fitnesses)) / sum(fitnesses - min(fitnesses))
			# choose half of generation to survive and mutate
			parents = np.random.choice(self.creatures, size=population/2, p=_weights, replace=False)
			# creates offspring
			offspring = []
			for _id, parent in enumerate(parents):
				offspring.append(parent.mutated_child(_id))

			# sets first half of creature generation as offspring
			self.creatures = offspring
			# sets second half of creature generation as random
			for i in range(population/2, population):
				c = Creature(i)
				self.creatures.append(c)

		self.generation += 1

	def run(self):
		global frame_time, frame

		last_frame_time = 0

		pygame.mixer.music.load(GAME_SONG)

		done = False
		while not done:

			# event handling
			for event in pygame.event.get():
				if event.type == QUIT:
					done = True
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


			if self.state == Game.STATE_GAMEPLAY:
				screen.fill((0,0,0))

				for dude in self.creatures:
					if dude.alive:
						dude.display()
					else:
						pass
				
				self.player.display()
				#self.level.display()


				if self.key_right:
					self.player.direction -= 2.5
				if self.key_left:
					self.player.direction += 2.5

				if self.key_up:
					self.player.vel = 2
				else:
					self.player.vel = 0


				self.play_time = pygame.time.get_ticks() - self.play_start

				# show fitness of creatures
				thefont = pygame.font.SysFont("Arial", 20)
				i = 0
				for dude in self.creatures:
					mage = thefont.render("%s - %.2f" % (dude.id, dude.fitness), False, (255,255,255))
					screen.blit(mage, (width-120, 40*i+40))
					i+=1

				# show time
				mage = thefont.render("%.1f" % (20-self.play_time/1000.), False, (255,255,255))
				pygame.draw.rect(screen, (240,100,100), (0,0,width-(width*self.play_time/20000.), 10)  )
				screen.blit(mage, (20,20))


			self.creatures.sort(key=lambda x: x.fitness, reverse=True)

			# parent selection
			if self.play_time/1000. >= 20:
				self.new_generation()
				self.play_time = 0
				self.play_start = pygame.time.get_ticks()
				self.player.reset()


			pygame.display.update()

			frame_time = pygame.time.get_ticks() - last_frame_time
			last_frame_time = pygame.time.get_ticks()
			frame += 1



game = Game()
game.run()


pygame.quit()
sys.exit()





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
		   	
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

MUTANT_IMAGE = "resources/mutant.bmp"
PLAYER_IMAGE = "resources/player_.bmp"

DARWIN_IMAGE = "resources/darwin.bmp"
DARWIN_DROP_IMAGE = ["resources/darwin_dropping1.bmp", "resources/darwin_dropping2.bmp", "resources/darwin_dropping3.bmp"]

GAMEPLAY_SONG = "resources/abnormal.ogg"

HEADER_FONT = pygame.font.SysFont("Corbel", 50)
NORMAL_FONT = pygame.font.SysFont("Arial", 20)

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

'''class Movable:
	def __init__(self, image_path=None, pos=(0,0)):
		self.x = pos[0]
		self.y = pos[1]
		self.direction = 0
		self.vel = 0

		# if movable object has an image
		self.has_image = (image_path is not None) 
		if self.has_image:
			self.original_image = pygame.image.load(image_path).convert_alpha()
			self.image = self.original_image
			self.rect = self.image.get_rect()


	def display(self):
		# move
		self.x += self.vel * sin(self.direction)
		self.y += self.vel * cos(self.direction)
		if self.has_image:

			# rotate
			self.image = pygame.transform.rotate(self.original_image, self.direction)
			
			# position
			self.rect = self.image.get_rect()  # Replace old rect with new rect.
			self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.

			screen.blit(self.image, self.rect)'''

class Darwin:
	def __init__(self):

		self.image = pygame.image.load(DARWIN_IMAGE).convert_alpha()
		self.rect = self.image.get_rect()

		# centre of image
		self.x = width/2
		self.y = 40
		self.vel = 0


	def display(self, hover_timer=None):
		if hover_timer is not None:
			self.y = 40 + 10*sin(hover_timer/100.)
		screen.blit(self.image, (self.x - self.rect.width/2, self.y - self.rect.height/2))



class Player:
	def __init__(self):

		# prepare image
		self.og_image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
		self.image = self.og_image
		self.rect = self.image.get_rect()

		self.x = width/2
		self.y = height-90
		self.bullets = []
		self.health = 100
		self.shot_last_bullet = -9999

		self.max_vel = 2.2
		self.vel = 0
		self.direction = 180

	def display(self):

		# move
		self.x += self.vel * sin(self.direction)
		self.y += self.vel * cos(self.direction)

		# rotate
		self.image = pygame.transform.rotate(self.og_image, self.direction+180)
		
		# position
		self.rect = self.image.get_rect()  # Replace old rect with new rect.
		self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.

		screen.blit(self.image, self.rect)

		#pygame.draw.line(screen, (2,100,2),   ( self.x , self.y ),  ( self.x+40*sin(self.direction), self.y+40*cos(self.direction)), 2  ) 

		# draw health bar
		pygame.draw.rect(screen, (60,190,100), (self.x-30, self.y-20, self.health*60/100, 6), 0)
		pygame.draw.rect(screen, (255,255,255), (self.x-30, self.y-20, 60, 6), 1)

		# TODO cant hit wall

		for index, b in enumerate(self.bullets):
			if b.outside_screen():
				self.bullets.remove(b)
			b.display()


	def shoot(self):
		if pygame.time.get_ticks() - self.shot_last_bullet > 500:
			self.bullets.append(Bullet( self.x+12*sin(self.direction), self.y+12*cos(self.direction), self.direction%360))
			self.health -= 4
			self.shot_last_bullet = pygame.time.get_ticks()

	def reset(self):
		self.x = width/2
		self.y = height-90
		self.bullets = []
		self.health = 100

		self.vel = 0
		self.direction = 180


class Bullet:
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.direction = direction
		self.speed = 3.4

	def display(self):
		self.x += self.speed*sin(self.direction)
		self.y += self.speed*cos(self.direction)
		pygame.draw.circle(screen, (255,60,60), (int(self.x), int(self.y)), 5)

	def outside_screen(self):
		return (self.x < 0 or self.x > width) or (self.y < 0 or self.y > height)


class Creature:
	def __init__(self, _id, T1=None, T2=None):
		self.og_image = pygame.image.load(MUTANT_IMAGE).convert_alpha()
		self.image = self.og_image
		self.rect = self.image.get_rect()
		self.x = randint(40,width-40)     #width/2#randint(20,width-20)
		self.y = randint(80,140)   #20#height/2#randint(20,height-20)
		self.direction = randint(0, 359)
		self.max_vel = 2
		self.rotation_vel = 6

		self.id = _id
		# degree of vision
		self.periphery = 108 
		self.health = 100
		self.alive = True
		# if in process of dying
		self.dying = False
		# time that dying animation started
		self.dying_start = 0

		self.fitness = 0
		self.fitness_rewards = 0
		self.fitness_punish = 0
		self.avg_distance2player = 0
		self.frame_since_last_attack = 0

		self.left_sensor_detect = 0		
		self.right_sensor_detect = 0	
		self.left_sensor_detect_bullet = 0
		self.right_sensor_detect_bullet = 0


		self.distance2player = 9999

		# Numbers of neurons in each layer
		self.s = (None, 6, 4, 2)

		''' Theta values are weighted to make some sensors more sensitive
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
		#screen.blit(self.image, self.rect)

		# positions of left and right sensors
		left_sensor_pos = (self.x + cos(self.direction-45)*10, self.y + sin(self.direction+45+90)*10) 
		right_sensor_pos = (self.x + cos(self.direction-45-90)*10, self.y + sin(self.direction+45)*10)

		# creature radius
		r = 32
		if self.dying:
			# dying_time starts at 1000 and goes down to 0
			dying_time = 1000 - (pygame.time.get_ticks() - self.dying_start)
			if dying_time > 0:
				r = dying_time * 32/1000
			else:
				self.dying = False

		# draws body
		pygame.draw.ellipse(screen, (251,121,0), (self.x-r/2, self.y-r/2, r, r) )

		if self.alive:
			# draws eyes
			pygame.draw.ellipse(screen, (20,130,220), (left_sensor_pos[0]-8, left_sensor_pos[1]-8, 16, 16))
			pygame.draw.ellipse(screen, (20,130,220), (right_sensor_pos[0]-8, right_sensor_pos[1]-8, 16, 16))

			# draws bullet sensors
			if self.left_sensor_detect_bullet:
				pygame.draw.ellipse(screen, (230,130,130), (left_sensor_pos[0]-6, left_sensor_pos[1]-6, 12, 12))
			if self.right_sensor_detect_bullet:
				pygame.draw.ellipse(screen, (230,130,130), (right_sensor_pos[0]-6, right_sensor_pos[1]-6, 12, 12))
			# draws player sensors
			if self.left_sensor_detect:
				pygame.draw.ellipse(screen, (100,230,20), (left_sensor_pos[0]-4, left_sensor_pos[1]-4, 8, 8))
			if self.right_sensor_detect:
				pygame.draw.ellipse(screen, (100,230,20), (right_sensor_pos[0]-4, right_sensor_pos[1]-4, 8, 8))


			# draw health bar
			#pygame.draw.rect(screen, (215,30,70), (self.x-30, self.y-20, 60, 6))
			pygame.draw.rect(screen, (60,190,100), (self.x-30, self.y-20, self.health*60/100, 6), 0)
			pygame.draw.rect(screen, (255,255,255), (self.x-30, self.y-20, 60, 6), 1)
			

		# draw sensors to player
		#pygame.draw.polygon(screen, (100,2,2),   ( (left_sensor_pos[0] + cos(-self.periphery+90-self.direction)*20, left_sensor_pos[1] + sin(-self.periphery+90-self.direction)*20), left_sensor_pos, (left_sensor_pos[0] + cos(self.periphery-self.direction)*20, left_sensor_pos[1] + sin(self.periphery-self.direction)*20)), 0 if left_sensor_detect else 2  ) 
		#pygame.draw.polygon(screen, (100,2,2),   ( (right_sensor_pos[0] + cos(self.periphery+90-self.direction)*20, right_sensor_pos[1] + sin(self.periphery+90-self.direction)*20), right_sensor_pos, (right_sensor_pos[0] + cos(180-self.periphery-self.direction)*20, right_sensor_pos[1] + sin(180-self.periphery-self.direction)*20)), 0 if right_sensor_detect else 2  ) 

		# draw sensors to bullets
		#pygame.draw.polygon(screen, (2,180,2),   ( (left_sensor_pos[0] + cos(-self.periphery+90-self.direction)*20, left_sensor_pos[1] + sin(-self.periphery+90-self.direction)*20), left_sensor_pos, (left_sensor_pos[0] + cos(self.periphery-self.direction)*20, left_sensor_pos[1] + sin(self.periphery-self.direction)*20)), 0 if left_sensor_detect_bullet else 2  ) 
		#pygame.draw.polygon(screen, (2,180,2),   ( (right_sensor_pos[0] + cos(self.periphery+90-self.direction)*20, right_sensor_pos[1] + sin(self.periphery+90-self.direction)*20), right_sensor_pos, (right_sensor_pos[0] + cos(180-self.periphery-self.direction)*20, right_sensor_pos[1] + sin(180-self.periphery-self.direction)*20)), 0 if right_sensor_detect_bullet else 2  ) 
		
		#pygame.draw.line(screen, (2,100,2),   ( p.x , p.y ),  ( self.x, self.y), 2  ) 


	def update(self):
		# parameters
		self.left_sensor_detect = 0
		self.right_sensor_detect = 0
		self.left_sensor_detect_bullet = 0
		self.right_sensor_detect_bullet = 0
		wall_proximity_ = 0

		p = game.player

		#angle = atan2( (self.x - p.x), (self.y - p.y) )+180
		angle = angle_between((self.x, self.y), (p.x, p.y))
		#print angle

		# check sensor detects player
		if 360-self.periphery+90 < (-angle + self.direction)%360 or (-angle + self.direction)%360 < self.periphery:
			self.left_sensor_detect = 1
		else:
			self.left_sensor_detect = 0


		if self.periphery+90 > (-angle + self.direction)%360 > 180-self.periphery :
			self.right_sensor_detect = 1
		else:
			self.right_sensor_detect = 0

		# check sensor detects bullets
		self.left_sensor_detect_bullet = 0
		self.right_sensor_detect_bullet = 0
		hit_by_bullet = 0
		for b in p.bullets:
			angle = angle_between( (self.x, self.y), (b.x, b.y) )

			# if bullet is moving in direction of creature
			if -45 > p.direction - angle > -135:
				if 360-self.periphery+90 < (-angle + self.direction)%360 or (-angle + self.direction)%360 < self.periphery:
					self.left_sensor_detect_bullet = 1
				else:
					self.left_sensor_detect_bullet = 0


				if self.periphery+90 > (-angle + self.direction)%360 > 180-self.periphery :
					self.right_sensor_detect_bullet = 1
				else:
					self.right_sensor_detect_bullet = 0

			if dist((b.x, b.y), (self.x, self.y)) < 20:
				self.health -= randint(30,75)
				hit_by_bullet = 1
				p.bullets.remove(b)


		wall_proximity_ = wall_proximity(self.x, self.y)


		
		# draw id
		#font = pygame.font.SysFont("Corbel", 20)
		#screen.blit(font.render(str(self.id), True, (255,255,255)), (self.x-5, self.y-8))

		does_damage_to_player = 0
		if self.distance2player < 26:
			# cant do damage with one touch
			if frame - self.frame_since_last_attack > 20:
				self.frame_since_last_attack = frame
				p.health -= 5
				does_damage_to_player = 1

		if self.health < 0:
			if hit_by_bullet:
				# if player kills creature, health increases
				p.health += 3
			self.die()


		#move direction

		# inputs to NN including bias unit
		inupts = np.array((1, self.left_sensor_detect, self.right_sensor_detect, self.distance2player / dist((0,0), (width, height)), self.left_sensor_detect_bullet, self.right_sensor_detect_bullet, wall_proximity_ ) )

		[output_direction, output_velocity] = self.make_decision(inupts, self.T1, self.T2)  #randint(-200,100)/100.

		# move
		collided_x = (self.x < 0 or self.x > width)
		collided_y = (self.y < 0 or self.y > height)

		hit_wall = 0
		if (collided_x or collided_y):
			hit_wall = 1
			self.die()
		else:
			self.direction += self.rotation_vel*(output_direction-0.5)
			self.x += self.max_vel*output_velocity*sin(self.direction)
			self.y += self.max_vel*output_velocity*cos(self.direction)
			self.health -= output_velocity*0.04*(1 + game.generation/5)

		# rotate
		self.image = pygame.transform.rotate(self.og_image, self.direction)
		
		# position
		self.rect = self.image.get_rect()  # Replace old rect with new rect.
		self.rect.center = (self.x, self.y)  # Put the new rect's center at old center.

		# calculate average distance to player
		# could use timestep to do this
		self.distance2player = dist((self.x, self.y), (p.x, p.y))

		# could also use game.GAMEPLAY.time
		if game.scene.time == 0:
			self.avg_distance2player = self.distance2player
		else:
			self.avg_distance2player = (self.distance2player + self.avg_distance2player*(game.scene.time-1) ) / (game.scene.time)

		# detects if stationary
		stationary = 0
		if output_velocity < 0.1:
			stationary = 1



		# REWARDS
		# average distance to player
		self.fitness = ( (dist((0,0), (width, height)) - self.avg_distance2player) / 100. )**2
		# damage done on player
		self.fitness_rewards += does_damage_to_player*40 
		# time with player in sight
		self.fitness_rewards += self.left_sensor_detect/200. + self.right_sensor_detect/200.
		# time with player in both sensors
		self.fitness_rewards += 0.1 if (self.left_sensor_detect and self.right_sensor_detect) else 0
		# veloctiy
		self.fitness_rewards += output_velocity/40.

		# PUNISHMENTS
		# being stationary
		self.fitness_punish += stationary/10.
		# running into walls
		self.fitness_punish += hit_wall*10
		# hitting bullets
		self.fitness_punish += hit_by_bullet*10

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
		self.dying = True
		self.dying_start = pygame.time.get_ticks()

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

class Scene:
	def __init__(self):
		# since scene began
		self.start = 0
		self.frame = 0
		self.time = 0

	def update(self):
		self.time = pygame.time.get_ticks() - self.start
		self.frame += 1

	def render(self):
		pass

	def begin(self):
		pass

	def go_to(self, new_scene):
		game.scene = new_scene
		# time when scene began
		new_scene.start = pygame.time.get_ticks()
		new_scene.frame = 0
		new_scene.time = 0
		new_scene.begin()

class MainMenuScene(Scene):
	def __init__(self):
		Scene.__init__(self)

		self.play_button = Button("Play", (40, 160))
		def play_action():
			game.new_generation()
			self.go_to(game.GAMEINTRO)
		self.play_button.mouse_up = play_action

		# how to play button
		self.htp_button = Button("How to play", (40, 260))
		def htp_action():
			self.go_to(game.HOW_TO_PLAY)
		self.htp_button.mouse_up = htp_action
		
		self.header_image = HEADER_FONT.render("Darwin", False, (255,255,255))

	def render(self):
		screen.fill((0,0,0))
		self.play_button.add(screen)
		self.htp_button.add(screen)
		screen.blit(self.header_image, (40, 40))

class GamePlayScene(Scene):
	def __init__(self):
		Scene.__init__(self)

	def begin(self):
		pygame.mixer.music.load(GAMEPLAY_SONG)
		pygame.mixer.music.play(-1)

	def render(self):
		screen.fill((0,0,0))

		for creature in game.creatures:
			# only update if alive
			if creature.alive:
				creature.update()
			# display when alive or dying
			if creature.alive or creature.dying:
				creature.display()
		
		game.player.display()

		if game.key_right:
			game.player.direction -= 3
		if game.key_left:
			game.player.direction += 3

		if game.key_up:
			game.player.vel = game.player.max_vel
		else:
			game.player.vel = 0


		# show fitness of creatures
		'''i = 0
		for dude in self.creatures:
			mage = NORMAL_FONT.render("%s - %.2f" % (dude.id, dude.fitness), False, (255,255,255))
			screen.blit(mage, (width-120, 40*i+40))
			i+=1'''

		# show time
		pygame.draw.rect(screen, (240,100,100), (0,0,width-(width*self.time/20000.), 10)  )
		'''mage = thefont.render("%.1f" % (20-self.play_time/1000.), False, (255,255,255))
		screen.blit(mage, (width/2,4))'''

		# show generation
		mage = NORMAL_FONT.render("Generation %s" % (game.generation), False, (255,255,255))
		screen.blit(mage, (width/2-mage.get_rect().width/2, 1))


		game.creatures.sort(key=lambda x: x.fitness, reverse=True)

		# parent selection
		if self.time/1000. >= 20:
			game.new_generation()
			self.time = 0
			self.start = pygame.time.get_ticks()
			self.frame = 0
			game.player.reset()


class GameIntroScene(Scene):
	''' Parts of this scene:
	1. Darwin appears, is hovering, "Skip intro" button at bottom right (go to part 4), "Press space to continue"
	2. "Evil Dr Darwin is trying to breed the ultimate killing creature"
	2. "Every generation the best killer creatures survive"
	3. "Kill the creatures by leading them into walls or shooting them"
	4. Creatures move directly down from Darwin, Darwin dropping sprite
	5. Creatures move to their positions
	6. 
	'''
	def __init__(self):
		Scene.__init__(self)
		self.creature_init_pos = None
		self.darwin = Darwin()
		self.part = 1
		# time since part started
		self.part_start = 0

	def begin(self):
		self.creature_init_pos = [ (creature.x, creature.y) for creature in game.creatures ]
		self.part_start = pygame.time.get_ticks()

	def render(self):
		screen.fill((0,0,0))
		if self.part == 1:

			self.darwin.display(hover_timer=self.part_start)

			for creature in game.creatures:
				creature.display()

		# creature animation
		if self.part == 5:
			duration = 1200
			# move from darwin to positions
			for index, creature in enumerate(game.creatures):
				creature.x = self.creature_init_pos[index][0] + (self.darwin.x - self.creature_init_pos[index][0]) * (pygame.time.get_ticks() - self.part_start) / duratiom
				creature.y = self.creature_init_pos[index][1] + (self.darwin.y + 60 - self.creature_init_pos[index][1]) * (pygame.time.get_ticks() - self.part_start) / duration
			if pygame.time.get_ticks() - self.part_start == duration:
				self.part += 1
		if self.part == 6:
			self.go_to(game.GAMEPLAY)

class HowToPlayScene(Scene):
	def __init__(self):
		Scene.__init__(self)
		self.back_button = Button("Back", (40, height-60))
		def back_action():
			self.go_to(game.MAIN_MENU)
		self.back_button.mouse_up = back_action

	def render(self):
		screen.fill((0,0,0))

		self.back_button.add(screen)

		header_image = HEADER_FONT.render("Darwin", False, (255,255,255))
		screen.blit(header_image, (40, 40))

class Game:
	MAIN_MENU = MainMenuScene()
	GAMEPLAY = GamePlayScene()
	GAMEINTRO = GameIntroScene()
	HOW_TO_PLAY = HowToPlayScene()

	def __init__(self):

		self.scene = Game.MAIN_MENU

		self.key_right = False
		self.key_left = False
		self.key_up = False
		self.key_down = False
		self.key_space = False

		self.player = Player()

		self.creatures = []
		self.generation = 0



		

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
		global frame

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

			self.scene.update()
			self.scene.render()
			# why is all time scenes updating??

			pygame.display.update()

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
		   	
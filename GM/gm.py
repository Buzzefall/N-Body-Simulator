import os
import pygame
import numpy
import random

from Quick import *

from random import randrange, randint
from pygame.locals import *
from math import pi, sqrt, log, exp, cos, sin, tan

WIN_WIDTH, WIN_HEIGTH = 1920, 1080

pygame.init()
display = pygame.display
#os.environ['SDL_VIDEO_CENTERED'] = '1'
win = display.set_mode( (WIN_WIDTH, WIN_HEIGTH), HWSURFACE|DOUBLEBUF|FULLSCREEN, 32)

VIEW_POINT = {'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2, 'z': WIN_WIDTH}
CENTER = { 'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2, 'z': 0}


RED = (0xFF, 0, 0)
BLUE = (0, 0, 0xFF)
GREEN = (0, 0xFF, 0)

G = 6.67*10**(-11)
DELTA = 10**(-6.25)
class Image:
	def __init__(self, x, y, color):
		self.x, self.y = x, y
		self.precolor = color
		self.lifetime = 110

	def reduce(self):
		if (self.lifetime <= 10):
			return 0
		else:
			self.lifetime -= 10
			self.color = (self.lifetime, 0, 0)
			return 1

def gaussian_blur():
	pass

def rangeS(a, b):
	return sqrt ( (a['x']-b['x'])**2 + (a['y']-b['y'])**2 + (a['z']-b['z'])**2 ) 

def putPoint(window, point, color):
	window.set_at( (round(point[0]), round(point[1])), color )

	window.set_at( (round(point[0]) +1, round(point[1]) +2), color )
	window.set_at( (round(point[0]) -1, round(point[1]) +2), color )
	window.set_at( (round(point[0]) -1, round(point[1]) -2), color )
	window.set_at( (round(point[0]) +1, round(point[1]) -2), color )
	window.set_at( (round(point[0]) +2, round(point[1])), color )
	window.set_at( (round(point[0]) -2, round(point[1])), color )

def apply_forces(bodies):
	quantity = len(bodies)
	RangeFactor = 0
	accel_ij = [0, 0]
	R = {'x': 0, 'y': 0, 'z': 0}
	velocity = ([ 
				{'x': 0, 'y': 0, 'z': 0 }
				for i in range(quantity) ] )
	boost = [{'x': 0, 'y': 0, 'z': 0} for i in range(quantity)]
	fadings = []

	bodies[0]['mass'] = 10**SUPERMASS
	bodies[0]['radius'] = round(bodies[0]['radius']*1.2)

	time = 0
	color = (255, 0, 0)
	fade_color = (color[0]//1.75, 0, 0)
	win.fill(0)

	for i in range(1, quantity):
		R['x'] = (bodies[i]['x'] - bodies[0]['x'])	# Радиус-векторы частиц
		R['y'] = (bodies[i]['y'] - bodies[0]['y']) 	
		R['z'] = (bodies[i]['z'] - bodies[0]['z'])

		RangeFactor = ( R['x']**2 + R['y']**2 + R['z']**2 + Limiter )**(-1.5)

		accel_ij[0] = RangeFactor * bodies[0]['mass']
		accel_ij[1] = RangeFactor * bodies[i]['mass']

		boost[i]['x'] += -G * accel_ij[0] * R['x'] 	# Подсчет взаимодействий тел в виде 
		boost[i]['y'] += -G * accel_ij[0] * R['y']	# накопления ускорения
		boost[i]['z'] += -G * accel_ij[0] * R['z']

		boost[0]['x'] -= -G * accel_ij[1] * R['x'] 
		boost[0]['y'] -= -G * accel_ij[1] * R['y']
		boost[0]['z'] -= -G * accel_ij[1] * R['z']

	for i in range(1, quantity):
		R['x'] = (bodies[i]['x'] - bodies[0]['x'])	
		R['y'] = (bodies[i]['y'] - bodies[0]['y']) 	
		R['z'] = (bodies[i]['z'] - bodies[0]['z'])
		Range = sqrt(R['x']**2 + R['y']**2 + R['z']**2)

		V = sqrt( (boost[i]['x']**2 + boost[i]['y']**2 + boost[i]['z']**2)*Range )

		velocity[i]['x'] = sqrt(V)*cos(i)
		velocity[i]['y'] = sqrt(V)*sin(i)
		velocity[i]['z'] = sqrt(V)*cos(i)
		boost[i]['x'], boost[i]['y'], boost[i]['z'] = 0, 0, 0

	while (1):
		win.fill((10,10,10))
		
		time += 0.05
		for event in pygame.event.get():
			if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
				display.quit()

		bodies[0]['x'] = pygame.mouse.get_pos()[0]
		bodies[0]['y'] = pygame.mouse.get_pos()[1]
		for i in range(quantity - 1):
			for j in range (i+1, quantity):

				R['x'] = (bodies[i]['x'] - bodies[j]['x'])	# Радиус-векторы частиц
				R['y'] = (bodies[i]['y'] - bodies[j]['y']) 	
				R['z'] = (bodies[i]['z'] - bodies[j]['z'])

				RangeFactor = (R['x']**2 + R['y']**2 + R['z']**2 + Limiter)**(-1.5)

				accel_ij[0] = RangeFactor * bodies[j]['mass']
				accel_ij[1] = RangeFactor * bodies[i]['mass']

				boost[i]['x'] += -G * accel_ij[0] * R['x'] 	# Подсчет взаимодействий тел в виде 
				boost[i]['y'] += -G * accel_ij[0] * R['y']	# накопления ускорения
				boost[i]['z'] += -G * accel_ij[0] * R['z']

				boost[j]['x'] -= -G * accel_ij[1] * R['x'] 
				boost[j]['y'] -= -G * accel_ij[1] * R['y']
				boost[j]['z'] -= -G * accel_ij[1] * R['z']
 
				#pygame.draw.line(win, (255,255,255), (bodies[i]['x'], bodies[i]['y']), (bodies[j]['x'], bodies[j]['y']))
		
										# Затухающие следы частиц																		
		for i in range(1, quantity):
			fadings.append( Image(bodies[i]['x'], bodies[i]['y'], color) )

		iterations = len(fadings)
		toDel = []

		for k in range(iterations):
			if fadings[k].reduce():
				putPoint(win, (fadings[k].x, fadings[k].y), fadings[k].color)
			else:
				toDel.append(k)

		for k in toDel:
			del fadings[k]

		for i in range(1, quantity):
			velocity[i]['x'] += boost[i]['x']*DELTA   
			velocity[i]['y'] += boost[i]['y']*DELTA 
			velocity[i]['z'] += boost[i]['z']*DELTA 
			bodies[i]['x'] +=  velocity[i]['x']*DELTA
			bodies[i]['y'] +=  velocity[i]['y']*DELTA
			bodies[i]['z'] +=  velocity[i]['z']*DELTA
			boost[i]['x'], boost[i]['y'], boost[i]['z'] = 0, 0, 0

			#Range = rangeS(bodies[i], VIEW_POINT)
			#bodies[i]['radius'] = 500 // sqrt(Range)
			
			putPoint(win, (bodies[i]['x'], bodies[i]['y']), color)

			#if (i>0) and (i % 15 == 0) and (i + 2 < quantity):
			#	points = [(bodies[i+j]['x'], bodies[i+j]['y']) for j in range(3)]
			#	pygame.draw.polygon(win, (255,255,255), points, 1)

			#pygame.draw.line(win, (255,255,255), (bodies[i]['x'], bodies[i]['y']), (bodies[0]['x'], bodies[0]['y']))
			
		putPoint(win, (bodies[0]['x'], bodies[0]['y']), color)

		#qs(bodies, velocity) 					# Сортировка по очереди прорисовки(по расстоянию)
		"""
		for i in range(quantity):
			pygame.draw.circle(
				win, 
				0, 
				(round(bodies[i]['x']), round(bodies[i]['y'])),
				round(bodies[i]['radius']), 0)
			pygame.draw.circle(
				win, 
				color, 
				(round(bodies[i]['x']), round(bodies[i]['y'])),
				round(bodies[i]['radius']), 1)
		"""
		#points = [(bodies[j+1]['x'], bodies[j+1]['y']) for j in range(1, quantity-1)]
		#pygame.draw.polygon(win, (255,255,255), points, 1)


		
		display.flip()
		
	return 0
def generate_bodies(place, area, body_amount):
	delta = 0
	bodies = []
	for i in range(body_amount):
		random.seed(i)
		radiusXY = 	(randrange(2*area) - area)*0.05
		radiusZ = 	(randrange(2*area) - area)*0.05
		if (i <= body_amount/4):
			shift = (delta, 0)
		elif (i <= 2*body_amount/4):
			shift = (-delta, 0)
		elif (i <= 3*body_amount/4):
			shift = (0, -delta)
		else:
			shift = (0, delta)
		bodies.append	(
							{															
							'x': place[0] + radiusXY*cos(pi/AMOUNT * i) + shift[0],
							'y': place[1] + radiusXY*sin(pi/AMOUNT * i) + shift[1], 		
							'z': place[0] + radiusZ*sin(pi/AMOUNT * i), 		
							'mass': randrange(10**(SUPERMASS//2), 10**(SUPERMASS-5)), #10**(SUPERMASS-4),
							'radius': 10
							}
						)
	return bodies

SUPERMASS = 28
Limiter = 8**sqrt(SUPERMASS)
AMOUNT = 75

bodies = generate_bodies( (WIN_WIDTH/2, WIN_HEIGTH/2), WIN_HEIGTH/2, AMOUNT)
apply_forces(bodies)




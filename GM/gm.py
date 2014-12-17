import os
import pygame
import numpy
import random

from Quick import *

from random import randrange, randint
from pygame.locals import *
from math import sqrt, cos, sin, tan, pi, log

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
DELTA = 10**(-5.5)

def rangeS(a, b):
	return sqrt((a['x']-b['x'])**2 + (a['y']-b['y'])**2 + (a['z']-b['z'])**2)

def putPoint(window, point, color):
	window.set_at( (round(point['x']), round(point['y'])), color )

	window.set_at( (round(point['x']) +1, round(point['y']) +2), color )
	window.set_at( (round(point['x']) -1, round(point['y']) +2), color )
	window.set_at( (round(point['x']) -1, round(point['y']) -2), color )
	window.set_at( (round(point['x']) +1, round(point['y']) -2), color )
	window.set_at( (round(point['x']) +2, round(point['y'])), color )
	window.set_at( (round(point['x']) -2, round(point['y'])), color )

def apply_forces(bodies):
	quantity = len(bodies)
	RangeFactor = 0
	accel_ij = [0, 0]
	R = {'x': 0, 'y': 0, 'z': 0}
	velocity = ([ 
				{'x': 15, 'y': 20, 'z': 0 }
				for i in range(quantity) ] )
	boost = [{'x': 0, 'y': 0, 'z': 0} for i in range(quantity)]

	center_mass = 10**18

	bodies[0]['mass'] = SUPERMASS
	bodies[0]['radius'] = round(bodies[0]['radius']*1.2)

	time = 0
	color = (255, 0, 255)
	win.fill(0)

	while (1):
		time += 0.05
		for event in pygame.event.get():
			if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
				pygame.quit()
		bodies[0]['x'] = pygame.mouse.get_pos()[0]
		bodies[0]['y'] = pygame.mouse.get_pos()[1]
		win.fill((10,10,10))
		for i in range(quantity - 1):
			for j in range (i+1, quantity):

				R['x'] = (bodies[i]['x'] - bodies[j]['x'])	# Радиус-векторы частиц
				R['y'] = (bodies[i]['y'] - bodies[j]['y']) 	
				R['z'] = (bodies[i]['z'] - bodies[j]['z'])

				RangeFactor = ( R['x']**2 + R['y']**2 + R['z']**2 + Limiter )**(-1.5)

				accel_ij[0] = RangeFactor * bodies[j]['mass']
				accel_ij[1] = RangeFactor * bodies[i]['mass']

				boost[i]['x'] += -G * accel_ij[0] * R['x'] 	# Подсчет взаимодействий тел в виде 
				boost[i]['y'] += -G * accel_ij[0] * R['y']	# накопления ускорения
				boost[i]['z'] += -G * accel_ij[0] * R['z']

				boost[j]['x'] -= -G * accel_ij[1] * R['x'] 
				boost[j]['y'] -= -G * accel_ij[1] * R['y']
				boost[j]['z'] -= -G * accel_ij[1] * R['z']
 
															# Сверхмассивное тело в центре
				#r2 = rangeS(bodies[i], CENTER)
				#RangeFactor = 1/r2
				#temp_force = -G*bodies[i]['mass']*center_mass * RangeFactor
				#cosY = (bodies[i]['y'] - CENTER['y']) / sqrt(RangeFactor) 
				#cosX = (bodies[i]['x'] - CENTER['x']) / sqrt(RangeFactor) 
				#boost[i]['x'] 	+= temp_force * cosX / bodies[i]['mass']
				#boost[i]['y'] 	+= temp_force * cosY / bodies[i]['mass']
				pygame.draw.line(win, (255,255,255), (bodies[i]['x'], bodies[i]['y']), (bodies[j]['x'], bodies[j]['y']))

		for i in range(1, quantity): 
			putPoint(win, bodies[i], (180, 0, 180))
			velocity[i]['x'] += boost[i]['x']*DELTA   
			velocity[i]['y'] += boost[i]['y']*DELTA 
			velocity[i]['z'] += boost[i]['z']*DELTA 
			bodies[i]['x'] +=  velocity[i]['x']*DELTA
			bodies[i]['y'] +=  velocity[i]['y']*DELTA
			bodies[i]['z'] +=  velocity[i]['z']*DELTA
			boost[i]['x'], boost[i]['y'], boost[i]['z'] = 0, 0, 0

			Range = rangeS(bodies[i], VIEW_POINT)
			bodies[i]['radius'] = 15000 // sqrt(Range)
			color = (255, 0, 255)

			putPoint(win, bodies[i], color)
			#pygame.draw.line(win, (255,255,255), (bodies[0]['x'], bodies[0]['y']), (bodies[i]['x'], bodies[i]['y']))
			#if ((bodies[i]['x'] > WIN_WIDTH + 1 or bodies[i]['x'] < -1) or 
			#	(bodies[i]['y'] > WIN_HEIGTH + 1 or bodies[i]['y'] < -1)):
			#	bodies[i]['x'], bodies[i]['y'] = bodies[0]['x'], bodies[0]['y']
			#	velocity[i]['x'], velocity[i]['y'] = cos(velocity[i]['x']), sin(velocity[i]['y'])

		#qs(bodies, velocity) 					# Сортировка по очереди прорисовки(по расстоянию)
		putPoint(win, bodies[0], color)
		#points = [(bodies[j+1]['x'], bodies[j+1]['y']) for j in range(1, quantity-1)]
		#pygame.draw.polygon(win, (255,255,255), points, 1)
		display.flip()
		
	return 0
def generate_bodies(place, area, body_amount):
	bodies = []
	for i in range(body_amount):
		random.seed(i)
		radiusX = (randrange(2*area) - area)*0.75
		radiusY = (randrange(2*area) - area)*0.75
		radiusZ = (randrange(2*area) - area)*0.75
		if i > body_amount/2:
			bodies.append	(
							{															
							'x': place[0] + radiusX*cos(pi/AMOUNT * i),
							'y': place[1] + radiusY*sin(pi/AMOUNT * i), 		
							'z': place[0] + radiusZ*sin(pi/AMOUNT * i), 		
							'mass': randrange(10**(avg_mass_order*1.5), 10**(avg_mass_order*2)),
							'radius': 10
							}
						)

		bodies.append	(
							{															
							'x': place[0] + radiusX*cos(pi/AMOUNT * i),
							'y': place[1] + radiusY*sin(pi/AMOUNT * i), 		
							'z': place[0] + radiusZ*sin(pi/AMOUNT * i), 		
							'mass': randrange(10**(avg_mass_order*1.5), 10**(avg_mass_order*2)),
							'radius': 10
							}
						)
	return bodies

avg_mass_order = 12
Limiter = 10**4
SUPERMASS = 10**25
AMOUNT = 50

bodies = generate_bodies( (WIN_WIDTH/2, WIN_HEIGTH/2), WIN_HEIGTH/2, AMOUNT)
apply_forces(bodies)




import os
import pygame
import numpy

from Quick import *

from pygame.locals import *
from random import randrange
from math import sqrt, cos, sin, tan, pi, log

WIN_WIDTH, WIN_HEIGTH = 1920, 1080

pygame.init()
display = pygame.display
os.environ['SDL_VIDEO_CENTERED'] = '1'
win = display.set_mode( (WIN_WIDTH, WIN_HEIGTH), HWSURFACE|DOUBLEBUF|FULLSCREEN, 32)

VIEW_POINT = {'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2, 'z': WIN_WIDTH}
CENTER = { 'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2, 'z': 0}


RED = (0xFF, 0, 0)
BLUE = (0, 0, 0xFF)
GREEN = (0, 0xFF, 0)

G = 6.67*10**(-11)
DELTA = 10**(-4.5)

#def rangeS(a, b):
	#return ( 	
			#numpy.abs(a['x'], b['x'])**2 + 
			#numpy.abs(a['y'], b['y'])**2 + 
			#numpy.abs(a['z'], b['z'])**2 )

def rangeS(a, b):
	return sqrt ( (a['x']-b['x'])**2 + (a['y']-b['y'])**2 + (a['z']-b['z'])**2 ) 

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
	Rfract = 0
	boost = [{'x': 0, 'y': 0, 'z': 0} for i in range(len(bodies))]
	velocity = ([ 
				{'x': 0, 'y': 0, 'z': 0 }
				for i in range(len(bodies)) ] )

	center_mass = 10**18

	bodies[0]['mass'] = SUPERMASS
	bodies[0]['radius'] = round(bodies[0]['radius']*1.2)

	time = 0
	color = RED
	win.fill(0)
	while (1):
		time += 0.1
		for event in pygame.event.get():
			if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
				pygame.quit()
		bodies[0]['x'] = pygame.mouse.get_pos()[0]
		bodies[0]['y'] = pygame.mouse.get_pos()[1]
		for i in range(quantity - 1):
			for j in range (quantity - i - 1):
				jit = j+i+1
				Rfract = ( rangeS(bodies[i], bodies[jit]) + Limiter )**(-3)
				cosY = (bodies[i]['y'] - bodies[jit]['y'])  						# Радиус-векторы частиц
				cosX = (bodies[i]['x'] - bodies[jit]['x'])
				cosZ = (bodies[i]['z'] - bodies[jit]['z'])
				force = -G * Rfract
				accel_ij = (force * bodies[jit]['mass'], force * bodies[i]['mass']) 
				boost[i]['x'] 	+= accel_ij[0] * cosX										# Подсчет взаимодействий тел в виде 
				boost[i]['y'] 	+= accel_ij[0] * cosY										# накопления ускорения
				boost[i]['z'] 	+= accel_ij[0] * cosZ

				boost[jit]['x'] -= accel_ij[1] * cosX
				boost[jit]['y'] -= accel_ij[1] * cosY
				boost[jit]['z'] -= accel_ij[1] * cosZ
 
																					# Сверхмассивное тело в центре

				#r2 = rangeS(bodies[i], CENTER)
				#Rfract = 1/r2
				#temp_force = -G*bodies[i]['mass']*center_mass * Rfract
				#cosY = (bodies[i]['y'] - CENTER['y']) / sqrt(Rfract) 
				#cosX = (bodies[i]['x'] - CENTER['x']) / sqrt(Rfract) 
				#boost[i]['x'] 	+= temp_force * cosX / bodies[i]['mass']
				#boost[i]['y'] 	+= temp_force * cosY / bodies[i]['mass']

		win.fill((10,10,10))

		for i in range(quantity): 

			velocity[i]['x'] += DELTA*boost[i]['x'] *0
			velocity[i]['y'] += DELTA*boost[i]['y'] *0
			velocity[i]['z'] += DELTA*boost[i]['z'] *0
			bodies[i]['x'] += DELTA*velocity[i]['x']
			bodies[i]['y'] += DELTA*velocity[i]['y']
			bodies[i]['z'] += DELTA*velocity[i]['z']
			boost[i]['x'], boost[i]['y'], boost[i]['z'] = 0, 0, 0

			Range = rangeS(bodies[i], VIEW_POINT)
			bodies[i]['radius'] = int(5 / numpy.sqrt(Range) * 3000)
			color = (255, 0, 255)

		#qs(bodies, velocity) 														# Сортировка по очереди прорисовки(по расстоянию)

		for i in range(1, quantity): #Отрисовка
			#pygame.draw.line(win, (255,255,255), (bodies[0]['x'], bodies[0]['y']), (bodies[i]['x'], bodies[i]['y']))
			rotating = { 
						'x': CENTER['x'] + rangeS(bodies[i], CENTER)*sin(time)*cos(time), 
						'y': bodies[i]['y'],
						'z': bodies[i]['z']
						}
			putPoint(win, rotating, color)
			"""
			pygame.draw.circle(
				win, 
				0, 
				(round(bodies[i]['x']), round(bodies[i]['y'])),
				bodies[i]['radius'], 0)
			pygame.draw.circle(
				win, 
				color, 
				(round(bodies[i]['x']), round(bodies[i]['y'])),
				bodies[i]['radius'], 1)
			"""
			#if (i>0) and (i % 25 == 0) and (i + 2 < quantity):
				#points = [(bodies[i+j]['x'], bodies[i+j]['y']) for j in range(3)]
				#pygame.draw.polygon(win, (255,255,255), points, 1)

		display.flip()
		
	return 0
def generate_bodies(place, area, body_amount):
	bodies = []
	for i in range(body_amount):
		radiusX = (randrange(2*area) - area)*0.75
		radiusY = (randrange(2*area) - area)*0.75
		radiusZ = (randrange(2*area) - area)*0.75
		bodies.append	(
							{															
							'x': place[0] + radiusX*cos(pi/AMOUNT * i),
							'y': place[1] + radiusY*sin(pi/AMOUNT * i), 		
							'z': 0, 		
							'mass': randrange(10**avg_mass_order, 10**(avg_mass_order*2)),
							'radius': 10
							}
						)
	return bodies

avg_mass_order = 12
Limiter = 100*avg_mass_order
SUPERMASS = 10**25.5
AMOUNT = 100

bodies = generate_bodies( (WIN_WIDTH/2, WIN_HEIGTH/2), WIN_HEIGTH/2, AMOUNT)
apply_forces(bodies)




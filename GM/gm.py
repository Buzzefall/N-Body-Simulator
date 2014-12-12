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
	return ( (a['x']-b['x'])**2 + (a['y']-b['y'])**2 + (a['z']-b['z'])**2 )

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
	velocity = ([ 
				{'x': cos(i)*4*pi, 'y': -sin(i)*4*pi, 'z': sin(i)*4*pi }
				for i in range(len(bodies)) ] )

	boost = [{'x': 0, 'y': 0, 'z': 0} for i in range(len(bodies))]

	temp_force = 0
	Rfract = 0
	center = { 'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2}
	center_mass = 10**18

	
	bodies[0]['mass'] = SUPERMASS
	bodies[0]['radius'] = round(bodies[0]['radius']*1.2)

	time = 0
	color = RED
	win.fill(0)
	while (1):
		time += 0.001
		for event in pygame.event.get():
			if (event.type == KEYDOWN) and (event.key == K_ESCAPE):
				pygame.quit()
		bodies[0]['x'] = pygame.mouse.get_pos()[0]
		bodies[0]['y'] = pygame.mouse.get_pos()[1]
		for i in range(quantity - 1):
			for j in range (quantity - i - 1):
				jit = j+i+1
				r2 = rangeS(bodies[i], bodies[jit])
				Rfract = 1/r2
				temp_force = -G*bodies[i]['mass']*bodies[jit]['mass'] * Rfract
				cosY = (bodies[i]['y'] - bodies[jit]['y']) / sqrt(Rfract) # Направляющие косинусы базисов X, Y, Z
				cosX = (bodies[i]['x'] - bodies[jit]['x']) / sqrt(Rfract)
				cosZ = (bodies[i]['z'] - bodies[jit]['z']) / sqrt(Rfract)

				boost[i]['x'] 	+= temp_force * cosX / bodies[i]['mass'] # Подсчет взаимодействий тел в виде 
				boost[i]['y'] 	+= temp_force * cosY / bodies[i]['mass'] # накопления ускорения
				boost[i]['z'] 	+= temp_force * cosZ / bodies[i]['mass']

				boost[jit]['x'] -= temp_force * cosX / bodies[jit]['mass']
				boost[jit]['y'] -= temp_force * cosY / bodies[jit]['mass']
				boost[jit]['z'] -= temp_force * cosZ / bodies[jit]['mass']

				# Сверхмассивное тело в центре

				#r2 = rangeS(bodies[i], center)
				#Rfract = 1/r2
				#temp_force = -G*bodies[i]['mass']*center_mass * Rfract
				#cosY = (bodies[i]['y'] - center['y']) / sqrt(Rfract) 
				#cosX = (bodies[i]['x'] - center['x']) / sqrt(Rfract) 
				#boost[i]['x'] 	+= temp_force * cosX / bodies[i]['mass']
				#boost[i]['y'] 	+= temp_force * cosY / bodies[i]['mass']

		win.fill((10,10,10))

		for i in range(quantity): # for i in range(1, quantity):

			velocity[i]['x'] += DELTA*boost[i]['x']
			velocity[i]['y'] += DELTA*boost[i]['y']
			velocity[i]['z'] += DELTA*boost[i]['z']
			bodies[i]['x'] += DELTA*velocity[i]['x']
			bodies[i]['y'] += DELTA*velocity[i]['y']
			bodies[i]['z'] += DELTA*velocity[i]['z']

			boost[i]['x'], boost[i]['y'], boost[i]['z'] = 0, 0, 0
			bodies[i]['radius'] = int(10 / numpy.sqrt(rangeS(bodies[i], VIEW_POINT)) * 1500)
			#bodies = qs(bodies) # Сортировка по очереди прорисовки(по расстоянию)

			color = (255*abs(cos(rangeS(bodies[i], VIEW_POINT)*0.00000055)), 0, 255*abs(cos(rangeS(bodies[i], VIEW_POINT)*0.00000055)))

			#pygame.draw.line(win, (255,255,255), (bodies[0]['x'], bodies[0]['y']), (bodies[i]['x'], bodies[i]['y']))
			putPoint(win, bodies[i], color)
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
			#if (i>0) and (i % 25 == 0) and (i + 2 < quantity):
				#points = [(bodies[i+j]['x'], bodies[i+j]['y']) for j in range(3)]
				#pygame.draw.polygon(win, (255,255,255), points, 1)

		display.flip()
		
	return 0
def generate_bodies(place, area, body_amount):
	bodies = []
	for i in range(body_amount):
		radiusX = (randrange(2*area) - area)*1.25
		radiusY = (randrange(2*area) - area)*1.25
		radiusZ = (randrange(2*area) - area)*1.25
		bodies.append	(
							{															
							'x': place[0] + radiusX*cos(i*0.1),
							'y': place[1] + radiusY*sin(i*0.1), 		
							'z': place[0] + radiusZ*sin(i*0.1), 		
							'mass': randrange(10**avg_mass_order, 10**(avg_mass_order*2)),
							'radius': 10
							}
						)
	return bodies
avg_mass_order = 6
SUPERMASS = 10**18.5
AMOUNT = 100

bodies = generate_bodies( (WIN_WIDTH/2, WIN_HEIGTH/2), WIN_HEIGTH/2, AMOUNT)
apply_forces(bodies)




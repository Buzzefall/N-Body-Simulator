import os
import pygame
from math import sqrt, cos, sin, tan, pi, log
from random import randrange
from pygame.locals import *

WIN_WIDTH, WIN_HEIGTH = 1920, 1080

pygame.init()
display = pygame.display
os.environ['SDL_VIDEO_CENTERED'] = '1'
win = display.set_mode( (WIN_WIDTH, WIN_HEIGTH), HWSURFACE|DOUBLEBUF|FULLSCREEN, 32)

RED = (0xFF, 0, 0)
BLUE = (0, 0, 0xFF)
GREEN = (0, 0xFF, 0)

G = 6.67*10**(-11)
DELTA = 10**(-4.45)

def rangeS(a, b):
	return ( (a['x']-b['x'])**2 + (a['y']-b['y'])**2 )

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
	velocity = [{'x': cos(i)*4*pi, 'y': -sin(i)*4*pi} for i in range(len(bodies))]
	boost = [{'x': 0, 'y': 0} for i in range(len(bodies))]

	temp_force = 0
	Rfract = 0
	center = { 'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2}
	center_mass = 10**18

	
	bodies[0]['mass'] = SUPERMASS
	radius = [int(log(bodies[i]['mass'], 500)*3.0) for i in range(quantity)]	
	radius[0] = round(radius[0]*1.2)

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
				cosY = (bodies[i]['y'] - bodies[jit]['y']) / sqrt(Rfract) 
				cosX = (bodies[i]['x'] - bodies[jit]['x']) / sqrt(Rfract) 
				boost[i]['x'] 	+= temp_force * cosX / bodies[i]['mass']
				boost[i]['y'] 	+= temp_force * cosY / bodies[i]['mass']
				boost[jit]['x'] -= temp_force * cosX / bodies[jit]['mass']
				boost[jit]['y'] -= temp_force * cosY / bodies[jit]['mass']

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
			bodies[i]['x'] += DELTA*velocity[i]['x']
			bodies[i]['y'] += DELTA*velocity[i]['y']
			boost[i]['x'], boost[i]['y'] = 0, 0
			"""
			for j in range(quantity - 1):
				if j == i: continue
				if rangeS(bodies[i], bodies[j]) <= 1:
					bodies[i]['mass'] += bodies[j]['mass']
					velocity[i]['x'] += velocity[j]['x']
					velocity[i]['y'] += velocity[j]['y']
					radius[i] = int(log(bodies[i]['mass'], 200)*3.0)
					quantity -= 1
					if i > j:
						i -= 1
					else:
						j -= 1
					del radius[j]
					del bodies[j]
					del velocity[j]
					del boost[j]
					break
			"""
			color = (255*abs(cos(velocity[i]['x']*0.0000021)), 0, 0)
			#pygame.draw.circle(win, color, (round(bodies[i]['x']), round(bodies[i]['y'])), radius[i], radius[i])
			putPoint(win, bodies[i], color)
			#pygame.draw.line(win, (255,255,255), (bodies[0]['x'], bodies[0]['y']), (bodies[i]['x'], bodies[i]['y']))
			#if (i>0) and (i % 25 == 0) and (i + 2 < quantity):
				#points = [(bodies[i+j]['x'], bodies[i+j]['y']) for j in range(3)]
				#pygame.draw.polygon(win, (255,255,255), points, 1)
				#pygame.draw.line(win, (255,255,255), (bodies[0]['x'], bodies[0]['y']), (bodies[i]['x'], bodies[i]['y']))
		display.flip()
		
	return forces
def generate_bodies(place, area, body_amount):
	bodies = []
	for i in range(body_amount):
		radiusX = (randrange(2*area) - area)*1.25
		radiusY = (randrange(2*area) - area)*1.25
		bodies.append	(
							{															
							'x': place[0] + radiusX*cos(i*0.1), 		
							'y': place[1] - radiusY*sin(i*0.1), 		
							'mass': randrange(10**avg_mass_order, 10**(avg_mass_order*2)) 
							}
						)
	return bodies
avg_mass_order = 6
SUPERMASS = 10**18
AMOUNT = 100

bodies = generate_bodies( (WIN_WIDTH/2, WIN_HEIGTH/2), WIN_HEIGTH/2, AMOUNT)
apply_forces(bodies)



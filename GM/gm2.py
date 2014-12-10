import pygame
from math import sqrt, cos, sin, acos, atan, asin, pi, log
from random import randrange
from pygame.locals import *

pygame.init()
display = pygame.display
win = display.set_mode( (1920, 1080), 0, 32)

RED = (0xFF, 0, 0)
BLUE = (0, 0, 0xFF)
GREEN = (0, 0xFF, 0)

G = 6.67*10**(-11)
DELTA = 10**(-4.5)

WIN_WIDTH, WIN_HEIGTH = 1920, 1080
avg_mass_order = 10
SUPERMASS = 10**18
AMOUNT = 75

def rangeS(a, b):
	return ( (a['x']-b['x'])**2 + (a['y']-b['y'])**2 )

def putPoint(window, point, color):
	window.set_at( (round(point['x']), 		round(point['y'])), color )
	window.set_at( (round(point['x']), 	round(point['y'] + 1)), color )
	window.set_at( (round(point['x'] - 1), round(point['y'])), color )
	window.set_at( (round(point['x']), 	round(point['y'] - 1)), color )




#def blow(bodies):
	#velocity = [0 for i in range(len(bodies))]
	#boost = [0 for i in range(len(bodies))]
	#forces = [0 for i in range(len(bodies))]

	
def apply_forces(bodies):
	quantity = len(bodies)
	velocity = [{'x': cos(i)*4*pi, 'y': -sin(i)*4*pi} for i in range(len(bodies))]
	boost = [{'x': 0, 'y': 0} for i in range(len(bodies))]
	bodies[0]['mass'] = SUPERMASS
	radius = [int(log(bodies[i]['mass'], 10**7)*10) for i in range(quantity)]	

	temp_force = 0
	Rfract = 0

	

	win.fill(0)
	while (1):
		
		for event in pygame.event.get():
			1	
		bodies[0]['x'] = pygame.mouse.get_pos()[0]
		bodies[0]['y'] = pygame.mouse.get_pos()[1]

		for i in range(quantity - 1):
			for j in range (quantity - i - 1):
				jit = j+i+1
				r2 = rangeS(bodies[i], bodies[jit])
				Rfract = 1/r2
				temp_force = -G*bodies[i]['mass']*bodies[jit]['mass'] * Rfract
				sina = (bodies[i]['y'] - bodies[jit]['y']) / sqrt(Rfract) 
				cosa = (bodies[i]['x'] - bodies[jit]['x']) / sqrt(Rfract) 
				boost[i]['x'] 	+= temp_force * cosa / bodies[i]['mass']
				boost[i]['y'] 	+= temp_force * sina / bodies[i]['mass']
				boost[jit]['x'] -= temp_force * cosa / bodies[jit]['mass']
				boost[jit]['y'] -= temp_force * sina / bodies[jit]['mass']

		win.fill(0)

		for i in range(quantity):
			velocity[i]['x'] -= DELTA*boost[i]['x']
			velocity[i]['y'] -= DELTA*boost[i]['y']
			bodies[i]['x'] -= DELTA*velocity[i]['x']
			bodies[i]['y'] -= DELTA*velocity[i]['y']
			boost[i]['x'], boost[i]['y'] = 0, 0

			pygame.draw.circle(win, RED, (round(bodies[i]['x']), round(bodies[i]['y'])), radius[i], radius[i])

		display.update()
		
	return forces

bodies = [ {'x': randrange(WIN_WIDTH/2) + WIN_WIDTH/4, 'y': randrange(WIN_HEIGTH/2) + WIN_HEIGTH/4, 'mass': 10**(randrange(avg_mass_order) + avg_mass_order/2) } for i in range(AMOUNT)]
apply_forces(bodies)


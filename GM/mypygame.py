import pygame, math
from math import sqrt, cos, sin, acos, atan, asin, pi
from random import randrange
from pygame.locals import *

def right_round(CENTER, radius, direction, speed, time, dots = [], phase = []):
	array_length = len(dots)
	awayX = [False for i in range(array_length)]
	awayY = [False for i in range(array_length)]
	for i in range(array_length):
		if ( abs(CENTER[0] - dots[i][0]) > (radius + 1) ): awayX[i] = True
		if ( abs(CENTER[1] - dots[i][1]) > (radius + 1) ): awayY[i] = True
	for i in range(array_length):
		if awayX[i]:
			if (dots[i][0] + radius < CENTER[0]): 
					dots[i] = (dots[i][0] * 1.001, dots[i][1])
			else:	dots[i] = (dots[i][0] * 0.999, dots[i][1])
		if awayY[i]:
			if (dots[i][1] + radius < CENTER[1]): 
					dots[i] = (dots[i][0], dots[i][1] * 1.001)
			else:	dots[i] = (dots[i][0], dots[i][1] * 0.999)
		current_range = sqrt( abs(CENTER[0] - dots[i][0])**2 + abs(CENTER[1] - dots[i][1])**2 )
		dots[i] = (
			CENTER[0] + (-1)**(direction)*current_range*cos(phase[i] + time * speed),
			CENTER[1] - (-1)**(direction)*current_range*sin(phase[i] + time * speed)
			)
	return dots
def whirl(CENTER, radius, direction, speed, time, dots = []):
	phase = [ 1 for i in range(len(dots))]
	for i in range(len(dots)):
		initial_range = sqrt( abs(CENTER[0] - dots[i][0])**2 + abs(CENTER[1] - dots[i][1])**2 )
		phase[i] = asin((dots[i][1] - CENTER[1]) / initial_range)
		if (phase[i] < 0) and (dots[i][0] < CENTER [0]) : phase[i] += pi
		elif (phase[i] > 0) and (dots[i][0] < CENTER [0]) : phase[i] += pi
	color = (WHITE)
	
	for event in pygame.event.get():
		if (event.type == KEYDOWN) and (event.type == QUIT): 
			pygame.quit()
	time += 1
	dots = right_round(CENTER, radius, 0, speed, time, dots, phase)
	for point in dots:
		point = (round(point[0]), round(point[1]))
		win.set_at(point, color)
	pygame.display.update()
	#win.fill(0)	

	#pygame.quit()


#points = [(    
#		(randrange(300)+1)*10 + 1 - center[0], 
#		(randrange(300)+1)*10 + 1 - center[1]
#		) for i in range(3000)]
#for i in range(1000):
#	whirl(center, radius, 0, spd, time = 0, points)

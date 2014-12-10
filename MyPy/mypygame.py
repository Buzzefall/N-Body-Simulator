import pygame, math
from math import sqrt, cos, sin, acos, atan, asin, pi
from random import randrange
from pygame.locals import *

def right_round(center, radius, direction, speed, time, dots = [], phase = []):
	array_length = len(dots)
	awayX = [False for i in range(array_length)]
	awayY = [False for i in range(array_length)]
	for i in range(array_length):
		if ( abs(center[0] - dots[i][0]) > (radius + 1) ): awayX[i] = True
		if ( abs(center[1] - dots[i][1]) > (radius + 1) ): awayY[i] = True
	for i in range(array_length):
		if awayX[i]:
			if (dots[i][0] + radius < center[0]): 
					dots[i] = (dots[i][0] * 1.001, dots[i][1])
			else:	dots[i] = (dots[i][0] * 0.999, dots[i][1])
		if awayY[i]:
			if (dots[i][1] + radius < center[1]): 
					dots[i] = (dots[i][0], dots[i][1] * 1.001)
			else:	dots[i] = (dots[i][0], dots[i][1] * 0.999)
		current_range = sqrt( abs(center[0] - dots[i][0])**2 + abs(center[1] - dots[i][1])**2 )
		dots[i] = (
			center[0] + (-1)**(direction)*current_range*cos(phase[i] + time * speed),
			center[1] - (-1)**(direction)*current_range*sin(phase[i] + time * speed)
			)
	return dots
def whirl(center, radius, direction, speed, dots = []):
	phase = [ 1 for i in range(len(dots))]
	for i in range(len(dots)):
		initial_range = sqrt( abs(center[0] - dots[i][0])**2 + abs(center[1] - dots[i][1])**2 )
		phase[i] = asin((dots[i][1] - center[1]) / initial_range)
		if (phase[i] < 0) and (dots[i][0] < center [0]) : phase[i] += pi
		elif (phase[i] > 0) and (dots[i][0] < center [0]) : phase[i] += pi
	color = red
	i = 0
	pygame.event.get()
	while (1):
		for event in pygame.event.get():
			if event == K_ESCAPE or event == QUIT: 
				break
		i += 1
		dots = right_round(center, radius, 0, speed, i, dots, phase)
		for point in dots:
			point = (round(point[0]), round(point[1]))
			win.set_at(point, color)
		pygame.display.update()
		win.fill(0)		
	pygame.quit()


display = pygame.display
w, h = 1000, 800
win = pygame.display.set_mode( (w,h), 0, 32 )
display.toggle_fullscreen()
drawc = pygame.draw.circle

red = (0xFF, 0, 0)
center = (w//2, h//2)
radius = 200
spd = 0.020

points = [(    
		(randrange(300)+1)*10 + 1 - center[0], 
		(randrange(300)+1)*10 + 1 - center[1]
		) for i in range(3000)]

whirl(center, radius, 0, spd, points)
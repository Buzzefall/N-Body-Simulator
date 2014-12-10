import pygame, math
from math import sqrt, cos, sin
from random import randrange
def right_round(center, radius, direction, phase, speed, time, dots = []):
	array_length = len(dots)
	awayX = [False for i in range(array_length)]
	awayY = [False for i in range(array_length)]
	for i in range(array_length):
		if ( abs(center[0] - dots[i][0]) > (radius + 1) ): awayX[i] = True
		if ( abs(center[1] - dots[i][1]) > (radius + 1) ): awayY[i] = True
	for i in range(array_length):
		if awayX[i]:
			if (dots[i][0] < center[0]): 
					dots[i] = (dots[i][0] * 1.01, dots[i][1])
			else:	dots[i] = (dots[i][0] * 0.99, dots[i][1])
		if awayY[i]:
			if (dots[i][1] < center[1]): 
					dots[i] = (dots[i][0], dots[i][1] * 1.01)
			else:	dots[i] = (dots[i][0], dots[i][1] * 0.99)
		dots[i] = (
			center[0] + (-1)**(direction)*abs(center[0] - dots[i][0])*cos(phase + time * speed),
			center[1] - (-1)**(direction)*abs(center[1] - dots[i][1])*sin(phase + time * speed)
			)
	print(dots)
	return dots
def whirl(center, radius, direction, phase, speed, dots = []):
	color = red
	i = 0
	while True:
		i += 1
		dots = right_round(center, radius, 0, 0, speed, i, dots)
		for point in dots:
			win.fill(0)
			drawc(win, color, point, 5, 15)
			pygame.display.update()

win = pygame.display.set_mode( (1000, 1000), 0, 32 )
drawc = pygame.draw.circle

red = (0xFF, 0, 0)
center = (400, 400)
radius = 200
spd = 0.1

points = [(    
		(randrange(90)+1)*10, 
		(randrange(90)+1)*10
		) for i in range(10)]

whirl(center, radius, 0, 0, spd, points)

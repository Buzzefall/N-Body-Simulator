import os
import pygame
import numpy
import random

from Quick import *

from random import randrange, randint
from pygame.locals import *
from math import sqrt, cos, sin, tan, pi, log, acos, asin, atan

WIN_WIDTH, WIN_HEIGTH = 1920, 1080

RED = (0xFF, 0, 0)
BLUE = (0, 0, 0xFF)
GREEN = (0, 0xFF, 0)
CYAN = (0, 0xFF, 0xFF)

#os.environ['SDL_VIDEO_CENTERED'] = '1'

VIEW_POINT = 	{'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2, 'z': WIN_WIDTH}
CENTER = 		{'x': WIN_WIDTH/2, 'y': WIN_HEIGTH/2, 'z': 0}

G = 6.67*10**(-11)
DELTA = 10**(-6.0)

SUPERMASS = 28
Limiter = 8**sqrt(SUPERMASS)
AMOUNT = 75

class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z

class Image(Point):
	def __init__(self, point, color):
		super().__init__(point.x, point.y, point.z)
		self.color = color

class Body(Image):
	def __init__(self, point, color):
		super().__init__(point, color)
		self.velocity = Point(0,0,0)
		self.accel = Point(0,0,0)
		self.mass = randrange(10**(SUPERMASS//2), 10**(SUPERMASS-5)), #10**(SUPERMASS-4)
		self.radius = 10

class Simulator:
	#def init(self, point, color):
	#	self._bodies.append(Body(point, color))

	def __init__(self, quantity):
		self.quantity = quantity
		self.bodies = []
		for i in range(quantity):
			radius = randrange(100, WIN_HEIGTH/2)
			x = CENTER['x'] + radius*cos(pi/quantity * i)
			y = CENTER['y'] + radius*sin(pi/quantity * i)
			z = CENTER['z'] + radius*sin(pi/quantity * i)
			point = Point(x,y,z)

			self._bodies.append( Body(point, CYAN) )
		print("Simulator has been constructed and initialized!")

	def apply_forces(self):

		for i in range(self.quantity - 1):
			for j in range (i+1, self.quantity):
				R['x'] = (self.bodies[i].x - self.bodies[j].x)	# Радиус-векторы частиц
				R['y'] = (self.bodies[i].y - self.bodies[j].y) 	
				R['z'] = (self.bodies[i].z - self.bodies[j].z)

				RangeFactor = ( R['x']**2 + R['y']**2 + R['z']**2 + Limiter )**(-1.5)

				accel_ij[0] = RangeFactor * self.bodies[j].mass
				accel_ij[1] = RangeFactor * self.bodies[i].mass

				self.bodies[i].accel.x += -G * accel_ij[0] * R['x'] 	# Подсчет взаимодействий тел в виде 
				self.bodies[i].accel.y += -G * accel_ij[0] * R['y']	# накопления ускорения
				self.bodies[i].accel.z += -G * accel_ij[0] * R['z']

				self.bodies[j].accel.x -= -G * accel_ij[1] * R['x'] 
				self.bodies[j].accel.y -= -G * accel_ij[1] * R['y']
				self.bodies[j].accel.z -= -G * accel_ij[1] * R['z']
	def move(self):
		for i in range(self.quantity):
			
			self.bodies[i].velocity.x += self.bodies[i].accel.x*DELTA
			self.bodies[i].velocity.y += self.bodies[i].accel.y*DELTA
			self.bodies[i].velocity.z += self.bodies[i].accel.z*DELTA

			self.bodies[i].x += self.bodies[i].velocity.x*DELTA
			self.bodies[i].y += self.bodies[i].velocity.y*DELTA
			self.bodies[i].z += self.bodies[i].velocity.z*DELTA
			
				
		






pygame.init()
display = pygame.display
win = display.set_mode( (WIN_WIDTH, WIN_HEIGTH), HWSURFACE|DOUBLEBUF|FULLSCREEN, 32)


simula = Simulator(75)

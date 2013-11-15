#!/usr/bin/python

# from Animat import Animat

import random

class Animat:


	def __init__(self,starty,startx):
		self.y = starty
		self.x = startx
		
	@classmethod
	def randomStart(cls,sizey,sizex):
		# Given the size of the environment, start at random location
		#self.y = random.randint(1,sizey-1) - 1
		#self.x = random.randint(1,sizex-1) - 1
		return cls(random.randint(1,sizey-1) - 1,random.randint(1,sizex-1) - 1)
		
	def displayLocation(self):
		print "y is " + str(self.y) + ", x is " + str(self.x)
		
	def moveNorth(self):
		self.y = self.y - 1
		
	def moveSouth(self):
		self.y = self.y + 1
		
	def moveWest(self):
		self.x = self.x - 1
		
	def moveEast(self):
		self.x = self.x + 1

	def goToLocation(self,desty,destx):
		while desty == self.y and destx == self.x:
			if (desty > self.y):
			# Go south
				moveSouth
			elif (desty < self.y):
			# Go north
				moveNorth
			if (destx > self.x):
			# Go east
				moveEast
			elif (destx < self.x):
			# Go west
				moveWest
		
		
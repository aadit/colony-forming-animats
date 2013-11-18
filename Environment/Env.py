#!/usr/bin/python

from numpy import *
import random

class Env:
	
	def __init__(self,sizeOfSquare):
		self.map = zeros((sizeOfSquare,sizeOfSquare));
		self.size = sizeOfSquare;
		
	def displayMap(self):
		print(self.map)
	
	def displaySize(self):
		print 'Size is ' + str(self.size)
	
	# @classmethod
	def canMove(self,origy, origx, newy, newx):
		# Are the starting and ending locations on the map?
		if (origy < 0 or origy > self.size -1
		or origx < 0 or origx > self.size -1
		or newy < 0 or newy > self.size -1
		or newx < 0 or newx > self.size -1):
			#print "Invalid location entered"
			return False;
			
		# Make sure the new location is one spot above, below, left or right
		if (origy == newy and (origx == newx + 1 or origx == newx - 1)):
			return True;
		elif (origx == newx and (origy == newy + 1 or origy == newy - 1)):
			return True;
		return False;
		
	def makeGradient(self):
		# Gradient will be four times as big, twice in y and twice in x
		# Assumes square
		gradientSize = (self.size * 2) - 1
		
		# Enforce that our size is odd number (11x11 or 25x25 or something)
		# UPDATE - our size should now always be odd, this code is deprecated
		if (gradientSize % 2 == 0):
			gradientSize = gradientSize + 1
			# UPDATE - we shouldn't run this code ever
			print 'Error - gradient size was even'
		self.gradient = zeros((gradientSize,gradientSize))
		
		for column in range(0,gradientSize/2):
			self.gradient[:,column] = (							
				concatenate((arange((gradientSize/2)+1,gradientSize,1),
				arange(gradientSize,gradientSize/2,-1)),1) - gradientSize/2 + column)
			
		for column in range(gradientSize/2,gradientSize):
			self.gradient[:,column] = (
				concatenate((arange((gradientSize/2)+1,gradientSize,1),
				arange(gradientSize,gradientSize/2,-1)),1) + gradientSize/2 - column)
				
		# Make it do inverse square
		# Reverse highs and lows
		self.gradient = gradientSize + 1 - self.gradient
		# square
		self.gradient = power(self.gradient,2)
		self.gradient = 1 / self.gradient
				
	def makeFoodRandom(self):
		# Pick a random spot on the map
		# Drop the gradient on top of it
		foody = random.randrange(0,self.size)
		foodx = random.randrange(0,self.size)
		#print 'foody: '+str(foody)
		#print 'foodx: '+str(foodx)
		self.makeFood(foody,foodx)
									   			
	def makeFood(self,foody,foodx):
		gradCenterY = self.size - 1 # zero indexing
		gradCenterX = self.size - 1
		#print 'gradCenterY: '+str(gradCenterY)
		#print 'gradCenterX: '+str(gradCenterX)
		
		gradStartY = gradCenterY - foody
		gradStartX = gradCenterX - foodx
		#print 'gradStartY: '+str(gradStartY)
		#print 'gradStartX: '+str(gradStartX)
		#print 'self.size: '+str(self.size)

		self.map = self.map + (self.gradient[gradStartY:gradStartY + self.size ,
							   			gradStartX:gradStartX + self.size ])						 
#!/usr/bin/python

from numpy import *
import random
from Environment.FoodGenerator import FoodGenerator
from Environment.Food import Food

class Env:
	
	def __init__(self,sizeOfSquare):
		self.map = zeros((sizeOfSquare,sizeOfSquare));
		self.size = sizeOfSquare;
		self.foodGeneratorList = [];
		self.foodList = [];
		self.foodCounter = 0;
		
	def tick(self):
		# the main activator for the environment
		# 1. Tick others
		for fg in self.foodGeneratorList:
			fg.tick(self)
		self.updateMap();
		
	def getScentsCEWNS(self,animaty,animatx,foodType):
		# Given an animat's position, return the 5 "scents" around it.
		# NWSEC stand for North, West, South, East, and Center
		# The values will be returned in this order
		
		inputValues = [];
		mapSize = self.size;
		inputValues.append(self.map[animaty][animatx])

		#Append value sensed at right square
		if animatx + 1 >= mapSize:
			inputValues.append(0)

		else:
			inputValues.append(self.map[animaty][animatx + 1])

		#Append value sensed at left square
		if animatx - 1 < 0:
			inputValues.append(0)

		else:
			inputValues.append(self.map[animaty][animatx - 1])


		#Append value sensed at top square
		if animaty + 1 >= mapSize:
			inputValues.append(0)

		else:
			inputValues.append(self.map[animaty + 1][animatx])

		if animaty- 1 < 0:
			inputValues.append(0)

		else:
			inputValues.append(self.map[animaty - 1][animatx])
		
		return inputValues;
		
	def validPoint(self,y,x):
		return (0 <= y and 0 <= x and y < self.size and x < self.size)
		
	def maxValue(self):
		return self.map.max();
	
	def addGradient(self,foody,foodx):
		gradCenterY = self.size - 1 # zero indexing
		gradCenterX = self.size - 1
		gradStartY = gradCenterY - foody
		gradStartX = gradCenterX - foodx
		#print 'gradCenterY: '+str(gradCenterY)
		#print 'gradCenterX: '+str(gradCenterX)
		#print 'gradStartY: '+str(gradStartY)
		#print 'gradStartX: '+str(gradStartX)
		#print 'self.size: '+str(self.size)
		
		self.map = self.map + (self.gradient[gradStartY:gradStartY + self.size ,
							   			gradStartX:gradStartX + self.size ])
		
	def updateMap(self):
		# This allows us to update the map whenever necessary
		# Iterate through foodList
		# Add to map accordingly
		self.map = zeros((self.size,self.size));
		for food in self.foodList:
			self.addGradient(food.y,food.x);
	
	def displaySize(self):
		print 'Size is ' + str(self.size)

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
		foody = random.randrange(0,self.size)
		foodx = random.randrange(0,self.size)
		self.makeFood(foody,foodx)
									   			
	def makeFood(self,foody,foodx):
		self.foodList.append( Food(self.foodCounter,foody,foodx,10));
						   			
	def removeFood(self,id):
		for index,food in self.foodList:
			if food.id == id:
				del self.foodList[index];
				break;
		
	def addFoodGenerator(self,locy,locx,frequency):
		# Make sure this location resides in our map
		if (locy < 0 or locy > self.size or locx < 0 or locx > self.size):
			# Bad location
			print 'Bad location for food generator! Not on map'
		else:
			#frequency = 25; # random for now
			f = FoodGenerator(locy,locx,frequency)
			self.foodGeneratorList.append(f)
			
	def returnFoodIDAt(self,foody,foodx):
		# Given the input locations, traverse the foodList looking for the food
		# that matches.
		# If found, return the ID
		# else, return -1
		for food in self.foodList:
			if (food.y == foody and food.x == foodx):
				return food.id
				break
		return -1
		
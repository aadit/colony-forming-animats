#!/usr/bin/python

from NNInitializer import NNInitializer
from Environment.Env import Env
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

import random
import copy

class Animat:

	#Class Parameters
	count = 0

	#Animat Parameter Constants
	LIVING_COST 	= 0.1 # Metabolic cost
	MOVEMENT_COST	= 1.0 # Cost to move one unit


	def __init__(self,starty,startx, env, filename):

		#Initialize instance parameters
		self.jaw = 0
		self.y = starty
		self.x = startx
		self.energy  = 10.0 #Maybe change this based on stochastic processes?	
		self.env = env
		self.moved = False

		#Initialize threshold parameters
		self.reproductionThreshold = 40.0 #need 40 energy units to reproduce
		self.foodToEnergyWeights = [0.25, 0.25, 0.25, 0.25]
		self.eatingRateToEnergyWeights = [0.25, 0.25, 0.25, 0.25]

		#Load the Neural Net
		nni = NNInitializer()
		self.neuralNet = nni.readNetwork(filename)

		#Update Class Parameters
		Animat.count += 1


	def tick(self):
		normalizedInputs = self.senseEnvironment() #Sense Environment
		output = self.neuralNet.activate(normalizedInputs) #Propagate Neural Net
		print output
		#performActions
		self.expendEnergy()
		#self.displayLocation()
		#self.printEnergy()
		pass

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
		self.moved = True
		
	def moveSouth(self):
		self.y = self.y + 1
		self.moved = True

	def moveWest(self):
		self.x = self.x - 1
		self.moved = True

		
	def moveEast(self):
		self.x = self.x + 1
		self.moved = True


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

	def jawAction(self,value):
		if value > 0:
			self.jaw = 1
		else:
			selfself.jaw = 0

	def expendEnergy(self):
		if self.moved:
			self.energy -= Animat.MOVEMENT_COST
			self.moved = False #reset variable for next tick

		self.energy -= Animat.LIVING_COST

		if self.energy <= 0:
			self.energy = 0 #can't have negative energy
			self.die()

	def die(self):
		Animat.count -= 1
		pass #replace w/ self.env.removeAnimatFromMap()

	def eat(self,foodItem):
		foodItem.bites += 1
		energy += self.foodToEnergyWeights[foodItem.sourceNumber] #get this much energy from eating this food

	def printEnergy(self):
		print self.energy

	def senseEnvironment(self):

		inputValues = []

		mapSize = self.env.size

		#Append value sensed at current square
		inputValues.append(self.env.map[self.x][self.y])

		#Append value sensed at right square
		if self.x + 1 >= mapSize:
			inputValues.append(0)

		else:
			inputValues.append(self.env.map[self.x + 1][self.y])

		#Append value sensed at left square
		if self.x - 1 < 0:
			inputValues.append(0)

		else:
			inputValues.append(self.env.map[self.x - 1][self.y])


		#Append value sensed at top square
		if self.y + 1 >= mapSize:
			inputValues.append(0)

		else:
			inputValues.append(self.env.map[self.x][self.y + 1])

		if self.y - 1 < 0:
			inputValues.append(0)

		else:
			inputValues.append(self.env.map[self.x][self.y - 1])

		#Normalize with max value in input values
		maxVal = max(inputValues)
		if maxVal != 0:
			normalizedInputValues = [i/maxVal for i in inputValues]

		print "Sensed environment is: "
		print inputValues

		print "Normalized values are: " 
		print normalizedInputValues

		return normalizedInputValues











		
		
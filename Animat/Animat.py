#!/usr/bin/python

from NNInitializer import NNInitializer
from Environment.Env import Env
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

import random
from random import choice
import copy

class Animat:

	#Class Parameters
	count = 0
	ID = -1;

	#Animat Parameter Constants
	LIVING_COST 	= 0.1 # Metabolic cost
	MOVEMENT_COST	= 1.0 # Cost to move one unit


	def __init__(self,starty,startx, env, filename, idnum):

		#Initialize instance parameters
		self.jaw = 0
		self.y = starty
		self.x = startx
		self.energy  = 50.0 #Maybe change this based on stochastic processes?	
		self.env = env
		self.moved = False
		self.ID = idnum;
		self.alive = True;

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
		print "Normalized Inputs are: "
		print normalizedInputs
		print "Output Neuron State is:"
		print output
		self.performActions(output.tolist()) #Perform Actions based on outputs
		self.expendEnergy()
		self.displayLocation()
		#self.printEnergy()
		pass

	def tickStateMachine(self):
		print "Animat ID: "+str(self.ID);
		normalizedInputs = self.senseEnvironment();
		# First attempt, just follow gradient
		canMove = True;
		maxIndeces = [i for i,mymax in enumerate(normalizedInputs) if mymax == 1.0]
		if maxIndeces:
			randomMaxIndex = choice(maxIndeces);
			outputs = [0,0,0,0,0];
			outputs[randomMaxIndex] = 1;
		else:
			canMove = False;
		
		if (canMove):
			self.performActions(outputs);
			self.expendEnergy();

		self.printEnergy();

	@classmethod
	def randomStart(cls,sizey,sizex):
		# Given the size of the environment, start at random location
		#self.y = random.randint(1,sizey-1) - 1
		#self.x = random.randint(1,sizex-1) - 1
		return cls(random.randint(1,sizey-1) - 1,random.randint(1,sizex-1) - 1)
		
	def displayLocation(self):
		print "y is " + str(self.y) + ", x is " + str(self.x)
		
	def move(self,newy,newx):
		if self.env.canMove(self.y,self.x,newy,newx):
			self.y = newy
			self.x = newx
			self.moved = True

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
		self.alive = False;
		pass #replace w/ self.env.removeAnimatFromMap()

	def eat(self,foodItem):
		#foodItem.bites += 1
		foodItem.eat();
		print "Food size is: "+str(foodItem.size);
		if foodItem.size == 0:
			self.env.removeFood(foodItem.id);
			print "Food removed from environment"
		else:
			#get this much energy from eating this food
			self.energy += self.foodToEnergyWeights[foodItem.sourceNumber] 
			print "Ate food";

	def printEnergy(self):
		print "Energy: "+str(self.energy);

	def performActions(self,sensorOutput):
		#Get the max value of the sensor output and move in that direction
		maxVal = max(sensorOutput)
		maxIndex = sensorOutput.index(maxVal)

		#print "Max value is: "
		#print maxVal

		#print "Max index is: "
		#print maxIndex

		if maxIndex == 0:
			print "perform actions says 0"
			if self.isOnFood():
				print "scents tell me I'm on food"
				foodId = self.env.returnFoodIDAt(self.y,self.x)
				print "On food..., id is: "+str(foodId);
				if foodId != -1:
					# Eat!
					self.eat(self.env.returnFood(foodId));
					#print "Food removed from environment"
					#self.env.removeFood(foodId)
					#self.env.updateMap()


		elif maxIndex == 1:
			self.move(self.y, self.x + 1)

		elif maxIndex == 2:
			self.move(self.y, self.x - 1)

		elif maxIndex == 3:
			self.move(self.y - 1, self.x)

		elif maxIndex == 4:
			self.move(self.y + 1, self.x)


	def senseEnvironment(self):

		inputValues = self.env.getScentsCEWNS(self.y,self.x, 4)

		normalizedInputValues = [0] * 5
		#Normalize with max value in input values
		maxVal = max(inputValues)
		if maxVal != 0:
			normalizedInputValues = [i/maxVal for i in inputValues]

		return normalizedInputValues

	def isOnFood(self):
		scents = self.senseEnvironment();
		if (scents[0] > scents[1] and
			scents[0] > scents[2] and
			scents[0] > scents[3] and
			scents[0] > scents[4]):
			return True;
		return False;









		
		
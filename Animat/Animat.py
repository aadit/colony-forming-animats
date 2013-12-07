#!/usr/bin/python

from NNInitializer import NNInitializer
from QLearn import QLearn
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
	energyThreshold = 80
	actions = ['north', 'south', 'east','west','stay','eat','pickup','drop']

	#Animat Parameter Constants
	LIVING_COST 	= 0.1 # Metabolic cost
	MOVEMENT_COST	= 1.0 # Cost to move one unit
	EATING_REWARD   = 10.0 # Reward for eating one food source

	def __init__(self,starty,startx, env, filename, idnum = 1):

		#Initialize instance parameters
		self.y = starty
		self.x = startx
		self.energy  = 50.0 #Maybe change this based on stochastic processes?	
		self.env = env
		self.moved = False
		self.ID = idnum;
		self.alive = True;
		self.energy1 = 50
		self.energy2 = 50
		self.holding = -1
		self.reward = 0

		#Initialize threshold parameters
		self.reproductionThreshold = 40.0 #need 40 energy units to reproduce
		self.foodToEnergyWeights = [0.25, 0.25, 0.25, 0.25]
		self.eatingRateToEnergyWeights = [0.25, 0.25, 0.25, 0.25]

		#Load the Neural Net
		nni = NNInitializer()
		self.neuralNet = nni.readNetwork(filename)

		#Update Class Parameters
		Animat.count += 1

		#Initialize Q-Table (States and Actions)
		self.qLearn = QLearn(Animat.actions)

	def tick(self):
		#qLearn.
		currentState  = self.getState()
		action = self.qLearn.chooseAction(currentState)
		self.performQLearnAction(action)
		nextState = self.getState() #get the new state after performing actions
		self.qLearn.learn(currentState, action, self.reward, nextState) #update the Q Table

		#OLD TICK:
		#normalizedInputs = self.senseEnvironment() #Sense Environment
		#output = self.neuralNet.activate(normalizedInputs) #Propagate Neural Net
		#print "Normalized Inputs are: "
		#print normalizedInputs
		#print "Output Neuron State is:"
		#print output
		#self.performActions(output.tolist()) #Perform Actions based on outputs
		#self.expendEnergy()
		#self.displayLocation()
		#self.printEnergy()
		#pass

	#Perform action based on input action. Should return the integer value
	#of the +/- reward experienced from performing the action
	def performQLearnAction(self,action):

		if action == 'north':
			self.move(self.y - 1, self.x)

		if action == 'south':
			self.move(self.y + 1, self.x)

		if action == 'east':
			self.move(self.y, self.x - 1)

		if action == 'west':
			self.move(self.y,self.x + 1)

		if action == 'stay':
			pass

		if action == 'eat':
			self.eat()

		if action == 'pickup':
			self.pickup()

		if action == 'drop':
			self.drop()


	def getState(self):
		# Pick 1 or 0 for each state, add to total,
		# then shift total << 
		
		foodgradient1 = self.senseEnvironment(1)  
		foodgradient2 = self.senseEnvironment(2) 

		# temp states, just for example
		# in reality, this stuff will come from the animat itself
		total = 0;
		#total += 1 if (self.energy1 < Animat.energyThreshold) else 0;
		#total *= 10;
		#total += 1 if (self.energy2 < Animat.energyThreshold) else 0;
		#total *= 10;
		total += 1 if (self.holding > 0) else 0;
		total *= 10;
		total += 1 if (self.isOnFood()) else 0;
		
		# Food gradient choices are 4, can be represented by 2 bits
		total *= 10;
		total *= 10;
		if (foodgradient1 == 'north'):
			total += 0;
		elif (foodgradient1 == 'south'):
			total += 1;
		elif (foodgradient1 == 'west'):
			total += 10;
		elif (foodgradient1 == 'east'):
			total += 11;
			
		#total *= 10;
		#total *= 10;
		#if (foodgradient2 == 'north'):
		#	total += 0;
		#elif (foodgradient2 == 'south'):
		#	total += 1;
		#elif (foodgradient2 == 'west'):
		#	total += 10;
		#elif (foodgradient2 == 'east'):
		#	total += 11;
			
		return int(str(total),2);


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
			self.reward -= Animat.MOVEMENT_COST
			

	def pickup(self):
		self.holding = self.env.returnFoodIDAt(self.y,self.x)
		#manipulate env to move food @ FoodID on map

	def drop(self):
		self.holding = -1
		#manipulate env to keep food @ FoodID static on map

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

	def eat(self):
		#check spot and get food sources
		#for each food in food list
		foodId = self.env.returnFoodIDAt(self.y, self.x)

		if foodId >= 0:
			foodItem = self.env.returnFood(foodId)
			self.eatFood(foodItem)
			self.reward += Animat.EATING_REWARD


		#set flags for each food source


	def eatFood(self,foodItem):
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
			if self.isOnFood():
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


	def senseEnvironment(self, foodType):

		inputValues = self.env.getScentsCEWNS(self.y,self.x, foodType)

		maxVal = max(inputValues)
		maxIndeces = [i for i, mymax in enumerate(inputValues) if mymax == maxVal]
		if maxIndeces:
			maxIndex = choice(maxIndeces)

		if maxIndex == 0:
			state = 'center'

		if maxIndex == 1:
			state = 'east'

		if maxIndex == 2:
			state = 'west'

		if maxIndex == 3:
			state = 'north'

		if maxIndex == 4:
			state = 'south'

		return state


	def isOnFood(self):
		id = self.env.returnFoodIDAt(self.y,self.x)
		if id != -1:
			return True

		return False









		
		
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
	LIVING_COST 	= 0.01 # Metabolic cost
	MOVEMENT_COST	= 0.01	 # Cost to move one unit
	EATING_REWARD   = 10.0 # Reward for eating one food source

	def __init__(self,starty,startx, env, filename, idnum = 1):

		#Initialize instance parameters
		self.y = starty
		self.x = startx
		self.energy  = 50.0 #Maybe change this based on stochastic processes?	
		self.env = env;
		self.moved = False
		self.ID = idnum;
		self.alive = True;
		self.energy1 = 50
		self.energy2 = 50
		self.holding = [-1, -1];
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
		self.reward = 0
		currentState  = self.getState()
		action = self.qLearn.chooseAction(currentState)
		self.performQLearnAction(action)
		if (self.holding[0] >= 0):
			# move the food I'm holding
			self.env.returnFood(self.holding[0]).y = self.y;
			self.env.returnFood(self.holding[0]).x = self.x;
		elif (self.holding[1] >= 0):
			# move the food I'm holding
			self.env.returnFood(self.holding[1]).y = self.y;
			self.env.returnFood(self.holding[1]).x = self.x;
		self.reward -= Animat.LIVING_COST
		nextState = self.getState() #get the new state after performing actions
		self.qLearn.learn(currentState, action, self.reward, nextState) #update the Q Table

	#Perform action based on input action. Should return the integer value
	#of the +/- reward experienced from performing the action
	def performQLearnAction(self,action):

		if action == 'north':
			self.move(self.y - 1, self.x)

		if action == 'south':
			self.move(self.y + 1, self.x)

		if action == 'east':
			self.move(self.y, self.x + 1)

		if action == 'west':
			self.move(self.y,self.x - 1)

		if action == 'stay':
			pass

		if action == 'eat':
			self.eat()

		if action == 'pickup':
			self.pickup()

		if action == 'drop':
			self.drop()

		if (self.holding[0] >= 0):
			# move the food I'm holding
			self.env[0].returnFood(self.holding[0]).y = self.y;
			self.env[0].returnFood(self.holding[0]).x = self.x;
		elif (self.holding[1] >= 0):
			# move the food I'm holding
			self.env[1].returnFood(self.holding[1]).y = self.y;
			self.env[1].returnFood(self.holding[1]).x = self.x;


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
		total += 1 if (self.holding[0] > 0) else 0;
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

	@classmethod
	def randomStart(cls,sizey,sizex):
		# Given the size of the environment, start at random location
		#self.y = random.randint(1,sizey-1) - 1
		#self.x = random.randint(1,sizex-1) - 1
		return cls(random.randint(1,sizey-1) - 1,random.randint(1,sizex-1) - 1)
		
	def displayLocation(self):
		print "y is " + str(self.y) + ", x is " + str(self.x)
		
	def move(self,newy,newx):
		if self.env[0].canMove(self.y,self.x,newy,newx):
			self.y = newy
			self.x = newx
			self.reward -= Animat.MOVEMENT_COST
			

	def pickup(self,foodType):
		foodID = self.env[foodType].returnFoodIDAt(self.y,self.x);
		if foodID != -1:
			# There is food here. Can we pick it up?
			if self.env[foodType].returnFood(foodID).pickUp():
				# We successfully picked it up
				self.holding[foodType] = self.env[foodType].returnFoodIDAt(self.y,self.x)
		#manipulate env to move food @ FoodID on map

	def drop(self,foodType):
		if self.holding[foodType] != -1:
			self.env[foodType].returnFood(self.holding[foodType]).drop();
			self.holding[foodType] = -1;
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

	def eat(self,foodType):
		foodId = self.env[foodType].returnFoodIDAt(self.y, self.x)
		if foodId >= 0:
			foodItem = self.env[foodType].returnFood(foodId)
			if not foodItem.held:
				self.eatFood(foodItem,foodType)
				self.reward += Animat.EATING_REWARD

	def eatFood(self,foodItem,foodType):
		foodItem.eat();
		if foodItem.size == 0:
			self.env[foodType].removeFood(foodItem.id);
			print "Food removed from environment"
		else:
			self.energy += self.foodToEnergyWeights[foodItem.sourceNumber] 

	def printEnergy(self):
		print "Energy: "+str(self.energy);


	def senseEnvironment(self, foodType):
		inputValues = self.env[foodType].getScentsCEWNS(self.y,self.x)
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


	def isOnFood(self,foodType):
		id = self.env[foodType].returnFoodIDAt(self.y,self.x)
		if id != -1:
			return True

		return False

	def followGradient(self,stateMachine):
		if stateMachine == 'notholding':
			self.performQLearnAction(self.senseEnvironment(0));
			if self.isOnFood(0):
				self.pickup(0);
				return 'holding'
			return 'notholding'
		elif stateMachine == 'holding':
			self.performQLearnAction(self.senseEnvironment(1));
			if self.isOnFood(1):
				self.drop(0);
				return 'eat'
			return 'holding'
		elif stateMachine == 'eat':
			if self.isOnFood(0):
				self.eat(0);
				return 'eat';
			elif self.isOnFood(1):
				self.eat(1);
				return 'eat';
			else:
				return 'notholding';

		
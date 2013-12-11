#!/usr/bin/python

from NNInitializer import NNInitializer
from QLearn import QLearn
from Environment.Env import Env
from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
import numpy

import random
from random import choice
import copy

class Animat:

	#Class Parameters
	energyPerTick = [[]]
	count = 0
	ID = -1;
	allowDeath = False
	energyThreshold = 80
	actions = ['north', 'south', 'east','west','eat','pickup','drop']

	def __init__(self,starty,startx, env, filename, idnum = 1):

		#Initialize instance parameters
		self.y = starty
		self.x = startx
		self.env = env
		self.ID = idnum
		self.foodTypes = [0,1,2,3]
		self.energy = [50.0] * len(self.foodTypes)
		self.maxEnergy = [100.0] * len(self.foodTypes)
		self.previousEnergy = copy.copy(self.energy)
		self.energyUsageRate = [0.5] * len(self.foodTypes)
		self.foodsEaten = [0] * len(self.foodTypes)
		self.holding = [-1] * len(self.foodTypes)

		#Initialize flags
		self.moved = (False, 0) #if animat moved and direction animat moved in
		self.alive = True

		#Initialize threshold parameters
		self.reproductionThreshold = 40.0 #need 40 energy units to reproduce

		#Load the Neural Net (CURRENTLY UNUSED: we are using q learner instead)
		nni = NNInitializer()
		self.neuralNet = nni.readNetwork(filename)

		#Update Class Parameters
		Animat.count += 1

		#Initialize Q-Table (States and Actions)
		self.qLearn = QLearn(Animat.actions)

		#Statistics
		self.multipleFoodEaten = 0;
		self.multipleDrop = 0;

	def tick(self):
		#qLearn.
		currentState  = self.getState()
		targetFood = self.getTargetFoodSource()
		targetFoodDirection = self.senseEnvironment(targetFood)
		action = self.qLearn.chooseAction(currentState)
		self.performQLearnAction(action)
		reward = self.getReward(targetFoodDirection, action) #update energies and get the reward after performing action
		#print "Reward is:", reward
		nextState = self.getState() #get the new state after performing actions
		self.qLearn.learn(currentState, action, reward, nextState) #update the Q Table
		self.resetFlags()
		self.checkDeath()
		return self.alive


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

		if action == 'eat':
			self.eatAll()

		if action == 'pickup':
			self.pickupAnything()

		if action == 'drop':
			self.dropAnything()

	def getState(self):
		# Pick 1 or 0 for each state, add to total,
		# then shift total << 
		
		

		# temp states, just for example
		# in reality, this stuff will come from the animat itself
		total = 0;
		
		# Food gradient choices are 4, can be represented by 2 bits
		for i in self.foodTypes:
			total *= 10;
			total += 1 if (self.holding[self.foodTypes[i]] > 0) else 0;
			total *= 10;
			total += 1 if (self.isOnFood(i)) else 0;
			foodgradient = self.senseEnvironment(i)
			total *= 10;
			total *= 10;
			if (foodgradient == 'north'):
				total += 0;
			elif (foodgradient == 'south'):
				total += 1;
			elif (foodgradient == 'west'):
				total += 10;
			elif (foodgradient == 'east'):
				total += 11;
			
		return int(str(total),2);

	@classmethod
	def randomStart(cls,sizey,sizex):
		# Given the size of the environment, start at random location
		#self.y = random.randint(1,sizey-1) - 1
		#self.x = random.randint(1,sizex-1) - 1
		return cls(random.randint(1,sizey-1) - 1,random.randint(1,sizex-1) - 1)
	
	@classmethod
	def setDeath(death):
		Animat.allowDeath = death

	def displayLocation(self):
		print "y is " + str(self.y) + ", x is " + str(self.x)
		
	def move(self,newy,newx):
		if self.env[0].canMove(self.y,self.x,newy,newx):
			self.y = newy
			self.x = newx
			self.moved = (True,0)
			for f in self.foodTypes:
				if (self.holding[f] >= 0):
					# move the food I'm holding
					self.env[f].returnFood(self.holding[f]).y = self.y;
					self.env[f].returnFood(self.holding[f]).x = self.x;
					break;
			
	def pickupAnything(self):
		# Go through the food types
		for i,foodType in enumerate(self.foodTypes):
			if self.pickup(foodType):
				return;

	def pickup(self,foodType):
		# Check to see if we're holding anything already.
		# Enforce holding one item at a time.
		if max(self.holding) == -1:
			foodID = self.env[foodType].returnFoodIDAt(self.y,self.x);
			if foodID != -1:
				# There is food here. Can we pick it up?
				if self.env[foodType].returnFood(foodID).pickUp():
					# We successfully picked it up
					self.holding[foodType] = self.env[foodType].returnFoodIDAt(self.y,self.x)
					return True;
		return False;

	def dropAnything(self):
		# Drop whatever we're holding
		for i,foodType in enumerate(self.foodTypes):
			if self.drop(foodType):
				return;

	def drop(self,foodType):
		# Check to see
		if self.holding[foodType] != -1:
			# Check to see if we're about to drop one food type on a different food type
			# If so, increment self.multipleDrop
			# def isOnFood(self,foodType):
			for f in self.foodTypes:
				if foodType != f and self.isOnFood(f):
					self.multipleDrop += 1;
					break;

			self.env[foodType].returnFood(self.holding[foodType]).drop();
			self.holding[foodType] = -1;
			return True;
		return False;

	def checkDeath(self):
		if Animat.allowDeath:
			for e in self.energy:
				if e <= 0:
					Animat.count -= 1
					self.alive = False;
					print "Animat died."
					return
	
	def eatAnything(self):
		for i,foodType in enumerate(self.foodTypes):
			if self.eat(foodType):
				return;

	def eatAll(self):
		for i,foodType in enumerate(self.foodTypes):
			if self.eat(foodType):
				self.foodsEaten[i] = 1;
			else:
				self.foodsEaten[i] = 0;
		return self.foodsEaten;

	def eat(self,foodType):
		foodId = self.env[foodType].returnFoodIDAt(self.y, self.x)
		if foodId >= 0:
			foodItem = self.env[foodType].returnFood(foodId)
			if not foodItem.held:
				self.eatFood(foodItem,foodType)
				return True;
		return False;

	def eatFood(self,foodItem,foodType):
		foodItem.eat();
		if foodItem.size == 0:
			self.env[foodType].removeFood(foodItem.id);
			print "Food removed from environment"

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

	def followGradient(self,stateMachine,toEat,toFollow):
		if stateMachine == 'notholding':
			self.dropAnything();
			self.performQLearnAction(self.senseEnvironment(toEat));
			if self.isOnFood(toEat):
				if self.pickup(toEat):
					return 'holding'
				else:
					return 'fail';
			return 'notholding'
		elif stateMachine == 'holding':
			self.performQLearnAction(self.senseEnvironment(toFollow));
			if self.isOnFood(toFollow):
				if self.drop(toEat):
					return 'eat'
			return 'holding'
		elif stateMachine == 'eat':
			#if self.isOnFood(toEat):
			#	self.eat(toEat);
			#	return 'eat';
			#elif self.isOnFood(toFollow):
			#	self.eat(toFollow);
			#	return 'eat';
			if self.isOnFood(toEat) or self.isOnFood(toFollow):
				if not max(self.eatAll()) == 0:
					return 'eat';
				else:
					return 'fail'
			else:
				return 'notholding';

	def replenishEnergy(self):
		self.energy = [50.0] * len(self.foodTypes)

	#reset flags for next iteration
	def resetFlags(self):
		self.moved = (False, 0)
		self.followedGradient = False
		self.foodsEaten = [0] * len(self.foodTypes)

	def getTargetFoodSource(self):
		energyTilMax  = [y - x for x,y in zip(self.energy, self.maxEnergy)] # maxEnergy - currEnergy for each food source
		satiation     = [y * x for x,y in zip(self.energyUsageRate, energyTilMax)] 
		maxFollowValue = max(satiation)
		targetFoodSources = [i for i, mymax in enumerate(satiation) if mymax ==  maxFollowValue]
		if targetFoodSources:
			targetFood = choice(targetFoodSources)

		return targetFood

	def getReward(self, targetDirection, action):

		#Animat Parameter Constants
		LIVING_COST     = 1.0
		MOVEMENT_COST	= 0.01	 # Cost to move one unit
		EATING_REWARD   = 10.0   # Reward for eating one food source
		EATING_MULT_REWARD = 100.0
		GRADIENT_FOLLOW_REWARD = 10.0

		previousEnergy = copy.copy(self.energy)

		#print "Foods eaten: ", self.foodsEaten

		#Reward Gradient
		gradientReward = 0

		if targetDirection == action:
			LIVING_COST = 0
			MOVEMENT_COST = 0
			#print targetDirection, action
		
		#Subtract living cost and movement cost for each energy rate
		self.energy = [ currEnergy + EATING_REWARD * foodEaten - rate * (LIVING_COST  + MOVEMENT_COST * self.moved[0]) for currEnergy, rate, foodEaten in zip(self.energy, self.energyUsageRate, self.foodsEaten)]
		self.energy = [ min(currEnergy, maxEnergy) for currEnergy, maxEnergy in zip(self.energy,self.maxEnergy)] #Limit energy to max energy
		
		#Compute delta energy for each energy bucket
		deltaEnergy = [ currEnergy - prevEnergy for currEnergy, prevEnergy in zip(self.energy, previousEnergy)]
		netDeltaEnergy = sum(deltaEnergy) #sum up all of the delta energies

		#Determine a reward multiplier if eating multiple foods when hungry
		rewardsMultiplier = 1
		numFoodEaten = self.foodsEaten.count(1)
		if numFoodEaten > 1 and netDeltaEnergy > 0:
			rewardsMultiplier += pow(EATING_MULT_REWARD, numFoodEaten - 1)
			print "Ate multiple food sources!"
			self.multipleFoodEaten += 1;

		reward = netDeltaEnergy * rewardsMultiplier + gradientReward

		if targetDirection == action:
			pass
			#print reward

		return reward


		
#!/usr/bin/python

#from numpy import *
import random

class QLearn:

	# Possible states
	# (1. Holding food 1)
	# (2. holding food 2)
	# Maybe condense into one "holding" state?
	# 3. standing on food 1
	# 4. standing on food 2
	# 5. food 1 gradient north (minus y)
	# 6. food 1 gradient south (plus y)
	# 7. food 1 gradient east (plus x)
	# 8. food 1 gradient west (minus x)
	# 9. food 2 north
	# 10. food 2 south
	# 11. food 2 east
	# 12. food 2 west
	
	# Possible actions
	# 1. north
	# 2. south
	# 3. east
	# 4. west
	# 5. stay (maybe not necessary?)
	# 6. eat 
	# 7. pick up
	# 8. drop
	
	#numStates = 11;
	#numActions = 8;
	
	# table = zeros((2**numStates,numActions));
	# also called "self.q" here
	
	def __init__(self, actions, epsilon=0.1, alpha=0.2, gamma=0.9):
		self.q = {}
		
		self.epsilon = epsilon
		self.alpha = alpha
		self.gamma = gamma
		self.actions = actions
        
	def getQ(self, state, action):
		return self.q.get((state, action), 0.0)
        # return self.q.get((state, action), 1.0)

	def learnQ(self, state, action, reward, value):
		oldv = self.q.get((state, action), None)
		if oldv is None:
			self.q[(state, action)] = reward
		else:
			self.q[(state, action)] = oldv + self.alpha * (value - oldv)

	def chooseAction(self, state, return_q=False):
		q = [self.getQ(state, a) for a in self.actions]
		maxQ = max(q)

		if random.random() < self.epsilon:
			#action = random.choice(self.actions)
			minQ = min(q); mag = max(abs(minQ), abs(maxQ))
			q = [q[i] + random.random() * mag - .5 * mag for i in range(len(self.actions))] # add random values to all the actions, recalculate maxQ
			maxQ = max(q)

		count = q.count(maxQ)
		if count > 1:
			best = [i for i in range(len(self.actions)) if q[i] == maxQ]
			i = random.choice(best)
		else:
			i = q.index(maxQ)

		action = self.actions[i]

		if return_q: # if they want it, give it!
			return action, q
		return action

	def learn(self, state1, action1, reward, state2):
		maxqnew = max([self.getQ(state2, a) for a in self.actions])
		self.learnQ(state1, action1, reward, reward + self.gamma*maxqnew)


# Sim 2
# Given a target on the map, have the animat go to it
# When it reaches the target, place a new target somewhere, repeat

import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")

from Environment.Env import Env
from Animat.Animat import Animat
import time
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print 'Running Simulation 2'
mapSize = 15
food = Env(mapSize)
a = Animat.randomStart(mapSize,mapSize)
food.makeGradient()

for iteration in range(1,10):
	# Pick a random spot
	foody = random.randrange(0,mapSize)
	foodx = random.randrange(0,mapSize)
	print str(foody) + ' ' + str(foodx) 
	food.map[foody,foodx] = 5 # random number
	
	
	# pass animat object our map
	# food = a.goToLocation(foody,foodx,food)
	# animat should behave appropriately
	# it should return the map unmodified
	
	# check to see if the animat did the right thing
	
print (food.map)
	
	
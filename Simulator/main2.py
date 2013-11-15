# Sim 2
# Given a target on the map, have the animat go to it
# When it reaches the target, place a new target somewhere, repeat

import matplotlib
matplotlib.use('TKAgg')
from Env import Env
from Animat import Animat
import time
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print 'Running Simulation 2'
mapSize = 50
food = Env(mapSize)
a = Animat.randomStart(mapSize,mapSize)

for iteration in range(1,10):
	# Pick a random spot
	foody = random.randrange(1,mapSize+1)
	foodx = random.randrange(1,mapSize+1)
	food.map[foody,foodx] = 5 # random number
	
	# pass animat object our map
	food = a.goToLocation(foody,foodx,food)
	# animat should behave appropriately
	# it should return the map unmodified
	
	# check to see if the animat did the right thing
	
	
	
	
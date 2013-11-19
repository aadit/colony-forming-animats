# Sim 4 - Food generator
# Place a number of food generators on the map, perhaps spread out
# tick the environment, which should tick the food generators
# maybe tick the environment 1000 times

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

print 'Running Simulation 4 - Food generator test'
mapSize = 100
food = Env(mapSize)
#a = Animat.randomStart(mapSize,mapSize)
food.makeGradient()
print 'Made gradient.'

food.addFoodGenerator(20,20,10)
food.addFoodGenerator(90,50,50)
food.addFoodGenerator(25,88,200)

ims = []
fig = plt.figure()
for iterations in range(0,1000):
	food.tick()
	# animation
	im = plt.imshow(food.map)
	ims.append([im])
	if (iterations % 100 == 0):
		print 'Iteration: '+str(iterations)
	
food.addFoodGenerator(45,75,5)
for iterations in range(1000,2000):
	food.tick()
	# animation
	im = plt.imshow(food.map)
	ims.append([im])
	if (iterations % 100 == 0):
		print 'Iteration: '+str(iterations)

ani = animation.ArtistAnimation(fig, ims, interval=1, blit=True, repeat=False)
plt.show()
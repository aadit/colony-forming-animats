# Sim 4
# Add multiple foods to a map

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

print 'Running Simulation 3 - Gradient maker'
mapSize = 100
food = Env(mapSize)
a = Animat.randomStart(mapSize,mapSize)
food.makeGradient()
print 'Made gradient.'

for count in range(0,20):
	food.makeFoodRandom()

print str(count)+' food made.'

fig2 = plt.figure()
plt.pcolor(food.map)
plt.ion()
plt.show()

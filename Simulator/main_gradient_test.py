# Sim 3
# Make a gradient map four times as big as our environment map
# Place a "food" item somewhere in our environment
# "add" the appropriate gradient to our environment centered on the food
# Be wary of even and odd numbers of columns, rows

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
mapSize = 103
food = Env(mapSize)
a = Animat.randomStart(mapSize,mapSize)
food.makeGradient()


fig1 = plt.figure()
plt.pcolor(food.gradient)
plt.ion()
plt.show()

food.makeFoodRandom()
fig2 = plt.figure()
plt.pcolor(food.map)
plt.ion()
plt.show()

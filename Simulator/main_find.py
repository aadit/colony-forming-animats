# Sim
# Have animat go towards a food in the environment

import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")

from Environment.Env import Env
from Animat.Animat import Animat
from Animat.NNInitializer import NNInitializer
import time
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print 'Running Simulation - Find food'

filename = 'nn_100k.p'
#Init Environment and food sources
env = Env(250)
env.makeGradient()
for i in range (1, 2):
	env.makeFoodRandom()
env.updateMap()

#Create Animat
a = Animat(0,0,env, filename)

ims = []
fig = plt.figure()
for i in range(0,20):#while(500):
	env.tick()
	a.tick()
	#env.map[a.y,a.x] = 10
	im = plt.imshow(env.map)
	ims.append([im])
	
print 'Finished ticking'

ani = animation.ArtistAnimation(fig, ims, interval=1, blit=True, repeat=False)
plt.show()
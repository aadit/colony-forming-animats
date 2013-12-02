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

#filename = 'nn_scents_based.p'
filename = 'nn_precise_100k.p'
#Init Environment and food sources
env = Env(50)
env.makeGradient()
for i in range (0,10):
	env.makeFoodRandom()
	#env.makeFood(20,20);
env.updateMap()

#Create Animat
a = Animat(0,0,env, filename)

fig = plt.figure()
ims = []
for i in range(0,300):
	env.tick()
	a.tickStateMachine()
	env.map[a.y,a.x] = env.map.max();
	im = plt.imshow(env.map)
	im.set_cmap('spectral')
	ims.append([im])

env.tick()
	
print 'Finished ticking'

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
	repeat=False)
plt.colorbar()
plt.show()

print 'Saving animation...'
#ani.save('search_and_destroy.mp4')


print 'Finished!'
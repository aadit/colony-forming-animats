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

print 'Running Simulation - Add food generators to corners'

filename = 'nn_precise_100k.p'
#Init Environment and food sources
foodTypes = [0,1];
env = [Env(100,foodTypes[0]),Env(100,foodTypes[1])];
for e in env:
	e.makeGradient()
	for i in range (0,100):
		e.makeFoodRandom()
	e.updateMap()

#Create Animat
animats = [Animat(25,25,env,filename), 
			Animat(10,40,env,filename), 
			Animat(45,10,env,filename), 
			Animat(30,40,env,filename)]

fig = plt.figure()
ims = []

# Training session
for i in range(0,7000):
	for e in env:
		e.tick()
	for a in animats:
		a.tick()
		for e in env:
			e.map[a.y,a.x] = e.map.max();
	if i % 100 == 0:
		#for e in env:
		im = plt.imshow(env[0].map+env[1].map)
		im.set_cmap('spectral')
		ims.append([im])
	if i % 1000 == 0:
		print 'Tick: '+str(i);
for e in env:
	e.tick()
print 'Finished training'
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
	repeat=False)
plt.colorbar()
plt.show()

fig=plt.figure();
ims=[];

# Two food generators
env[0].addFoodGenerator(35,50,1000,1000);
env[1].addFoodGenerator(65,50,1000,1000);

for i in range(0,30000):
	for e in env:
		e.tick()
	for a in animats:
		a.tick()
		for e in env:
			e.map[a.y,a.x] = e.map.max();
	if i % 10 == 0:
		#for e in env:
		im = plt.imshow(env[0].map+env[1].map)
		im.set_cmap('spectral')
		ims.append([im])
	if i % 100 == 0:
		print 'Tick: '+str(i);

for e in env:
	e.tick()
	
print 'Finished ticking'

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
	repeat=False)
plt.colorbar()
plt.show()

#print 'Saving animation...'
#ani.save('search_and_destroy.mp4')


print 'Finished!'
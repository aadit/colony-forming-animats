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
mapsize = 100;
env = [Env(mapsize,foodTypes[0]),Env(mapsize,foodTypes[1])];
for e in env:
	e.makeGradient()
	for i in range (0,100):
		e.makeFoodRandom()
	e.updateMap()

#Create Animat
#animats = [Animat(25,25,env,filename), 
#			Animat(10,40,env,filename), 
#			Animat(45,10,env,filename), 
#			Animat(30,40,env,filename)]

animats = [];
for a in range(0,20):
	animats.append(Animat(random.randrange(0,mapsize),random.randrange(0,mapsize),env,filename));

fig = plt.figure()
ims = []
toPlot = zeros((mapsize,mapsize));

# Training session
for i in range(0,3000):
	for e in env:
		e.tick()
	for a in animats:
		a.tick()
		#for e in env:
			#e.map[a.y,a.x] = e.map.max() if e.map.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = e.simpleMap.max() if e.simpleMap.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = 10;
			#toPlot[a.y,a.x] = 5;
			#print "e.simpleMap.max() is :"+str(e.simpleMap.max());
	if i % 100 == 0:
		#for e in env:
		#im = plt.imshow(env[0].map+env[1].map)
		toPlot = env[0].simpleMap+env[1].simpleMap;
		for a in animats:
			if toPlot[a.y,a.x] == 0:
				toPlot[a.y,a.x] = 5;
		im = plt.imshow(toPlot)
		im.set_cmap('spectral')
		ims.append([im])
	if i % 1000 == 0:
		print 'Tick: '+str(i);
		#print 'max is: '+str(env[0].simpleMap.max())
for e in env:
	e.tick()
print 'Finished training'
ani = animation.ArtistAnimation(fig, ims, interval=50, #blit=True,
	repeat=False)
plt.colorbar()
plt.show()

fig=plt.figure();
ims=[];

# Two food generators

env[0].addFoodGenerator(10,12,200,5000); #y, x, regeneration rate, food bitsize
env[1].addFoodGenerator(88,90,200,5000);

for i in range(0,10000):
	for e in env:
		e.tick()
	for a in animats:
		a.tick()
		#for e in env:
			#e.map[a.y,a.x] = e.map.max() if e.map.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = e.simpleMap.max() if e.simpleMap.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = 10;
	if i % 10 == 0:
		#for e in env:
		#im = plt.imshow(env[0].map+env[1].map)
		#im = plt.imshow((env[0].simpleMap+env[1].simpleMap)/2)
		toPlot = env[0].simpleMap+env[1].simpleMap;
		#for a in animats:
		#	if toPlot[a.y,a.x] == 0:
		#		toPlot[a.y,a.x] = 5;
		im = plt.imshow(toPlot)
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

fig=plt.figure();
ims=[];


def printStats():
	for i,a in enumerate(animats):
		print i,a.energy
	for i,a in enumerate(animats):
		print i,a.multipleFoodEaten
	for i,a in enumerate(animats):
		print i,a.multipleDrop

#print 'Saving animation...'
#ani.save('search_and_destroy.mp4')


print 'Finished!'
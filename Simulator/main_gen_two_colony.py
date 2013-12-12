# Sim
# Have animat go towards a food in the environment

import matplotlib
matplotlib.use('TKAgg')
import sys
sys.path.append("..")
import time

from Environment.Env import Env
from Animat.Animat import Animat
import time
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import figure
from DataAnalysis.DataAnalysis import Plotter

print 'Running Simulation - Add food generators to form two colonies'

testname = "gen_corners"

#Init Environment and food sources
foodTypes = [0,1,2,3];
mapsize = 100;
env = [Env(mapsize,foodTypes[0]),Env(mapsize,foodTypes[1]),
		Env(mapsize,foodTypes[2]),Env(mapsize,foodTypes[3])];

for e in env:
	e.makeGradient()
	for i in range (0,200):
		e.makeFoodRandom()
	e.updateMap()
	
animats = [];
for a in range(0,20):
	animats.append(Animat(random.randrange(0,mapsize),random.randrange(0,mapsize),env,foodTypes,1500,1000));

fig = plt.figure()
ims = []
toPlot = zeros((mapsize,mapsize));
Animat.foodTargeting = False
Animat.allowDeath = False
trainingTicks = 7000
# Training session
for i in range(0,trainingTicks):
	for e in env:
		e.tick()
	Animat.startTick()
	for a in animats:
		stillAlive = a.tick()
		if not stillAlive:
			print a.energy
		for e in env:
			#e.map[a.y,a.x] = e.map.max() if e.map.max() > 0 else 1;
			e.binaryGradient[a.y,a.x] = e.binaryGradient.max() if e.binaryGradient.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = e.simpleMap.max() if e.simpleMap.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = 10;
			#toPlot[a.y,a.x] = 5;
			#print "e.simpleMap.max() is :"+str(e.simpleMap.max());
	Animat.endTick()
	if i % 100 == 0:
		#for e in env:
		#im = plt.imshow(env[0].map+env[1].map)
		#im = plt.imshow(env[0].binaryGradient+env[1].binaryGradient
			#	+env[2].binaryGradient+env[3].binaryGradient)
		pass
		#toPlot = env[0].simpleMap+env[1].simpleMap;
		#for a in animats:
		#	if toPlot[a.y,a.x] == 0:
		#		toPlot[a.y,a.x] = 5;
		#im = plt.imshow(toPlot)
		#im.set_cmap('spectral')
		#ims.append([im])
	if i % 1000 == 0:
		print 'Tick: '+str(i);
		#print 'max is: '+str(env[0].simpleMap.max())
for e in env:
	e.tick()


for i,a in enumerate(animats):
	print i,a.energy
	a.replenishEnergy(1000)

#ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat=False)
#plt.colorbar()
#plt.show()

fig=plt.figure();
ims=[];

# Two food generators

env[0].addFoodGenerator(50,50,500,1000); #y, x, regeneration rate, food bitsize
env[1].addFoodGenerator(10,90,1000,1000);
env[1].addFoodGenerator(90,90,1000,1000);
env[2].addFoodGenerator(10,50,1000,1000);
env[2].addFoodGenerator(90,50,1000,1000);
env[3].addFoodGenerator(10,10,1000,1000);
env[3].addFoodGenerator(90,10,1000,1000);


Animat.allowDeath = False
Animat.resetStats()
testingTicks = 20000

for i in range(0,testingTicks):
	for e in env:
		e.tick()
	Animat.startTick()
	for a in animats:
		stillAlive = a.tick()
		for e in env:
			#e.map[a.y,a.x] = e.map.max() if e.map.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = e.simpleMap.max() if e.simpleMap.max() > 0 else 1;
			#e.simpleMap[a.y,a.x] = 10;
			e.binaryGradient[a.y,a.x] = e.binaryGradient.max() if e.binaryGradient.max() > 0 else 1;
	Animat.endTick()
	if i % 10 == 0:
		#for e in env:
		#im = plt.imshow(env[0].map+env[1].map)
		im = plt.imshow(env[0].binaryGradient+env[1].binaryGradient
				+env[2].binaryGradient+env[3].binaryGradient)
		#im = plt.imshow((env[0].simpleMap+env[1].simpleMap)/2)
		#toPlot = env[0].simpleMap+env[1].simpleMap;
		#for a in animats:
		#	if toPlot[a.y,a.x] == 0:
		#		toPlot[a.y,a.x] = 5;
		#im = plt.imshow(toPlot)
		im.set_cmap('spectral')
		ims.append([im])
	if i % 100 == 0:
		print 'Tick: '+str(i);

for e in env:
	e.tick()
	
print 'Finished ticking'

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,repeat=False)
plt.colorbar()
plt.show()


plotter = Plotter(Animat, testingTicks)
plotter.plotData()

print 'Finished training'

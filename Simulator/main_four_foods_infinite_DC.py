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

print 'Running Simulation - Four foods, one of each'

#Init Environment and food sources
foodTypes = [0,1,2,3];
mapsize = 100;
env = [Env(mapsize,foodTypes[0]),Env(mapsize,foodTypes[1]),
		Env(mapsize,foodTypes[2]),Env(mapsize,foodTypes[3])];
for e in env:
	e.makeGradient()
	for i in range (0,100):
		e.makeFoodRandom()
	e.updateMap()
	
animats = [];
numAnimats = 20;
for a in range(0,numAnimats):
	animats.append(Animat(random.randrange(0,mapsize),random.randrange(0,mapsize),env,foodTypes));
Animat.allowDeath = False;

fig = plt.figure()
ims = []
toPlot = zeros((mapsize,mapsize));

# Training session
for i in range(0,15000):
	for e in env:
		e.tick()
	Animat.startTick()
	for a in animats:
		a.tick()
		for e in env:
			e.binaryGradient[a.y,a.x] = e.binaryGradient.max() if e.binaryGradient.max() > 0 else 1;
	Animat.endTick()
	if i % 100 == 0:
		im = plt.imshow(env[0].binaryGradient+env[1].binaryGradient
				+env[2].binaryGradient+env[3].binaryGradient)
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
time.sleep(3)

plt.show()

fig=plt.figure();
ims=[];

# Four infinite food generators
Animat.resetStats()
ticks = 30000;
# clear previous food
for e in env:
	e.foodList = [];

env[0].makeFood(45,12,ticks*numAnimats); #y, x, food bitsize
env[1].makeFood(53,90,ticks*numAnimats);
env[2].makeFood(3,53,ticks*numAnimats);
env[3].makeFood(96,49,ticks*numAnimats);

for i in range(0,ticks):
	for e in env:
		e.tick()
	Animat.startTick()
	for a in animats:
		a.tick()
		for e in env:
			e.binaryGradient[a.y,a.x] = e.binaryGradient.max() if e.binaryGradient.max() > 0 else 1;
	Animat.endTick()
	if i % 10 == 0:
		im = plt.imshow(env[0].binaryGradient+env[1].binaryGradient
				+env[2].binaryGradient+env[3].binaryGradient)
		im.set_cmap('spectral')
		ims.append([im])
	if i % 100 == 0:
		print 'Tick: '+str(i);

for e in env:
	e.tick()
	
print 'Finished ticking'

plotter = Plotter(Animat, ticks)
plotter.plotData()

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
	repeat=False)
plt.colorbar()
time.sleep(3)
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

print 'Finished!'
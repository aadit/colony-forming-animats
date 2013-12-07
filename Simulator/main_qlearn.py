# Sim
# Have animat go towards a food in the environment

#import matplotlib
#matplotlib.use('TKAgg')
import sys
sys.path.append("..")

from Environment.Env import Env
#from Animat.Animat import Animat
#from Animat.NNInitializer import NNInitializer
from Animat.QLearn import QLearn
import time
from numpy import zeros
import random
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation

print 'Running Simulation - have q learner give us an action to take'

#Init Environment and food sources
env = Env(50)
env.makeGradient()
for i in range (0,10):
	env.makeFoodRandom()
	#env.makeFood(20,20);
env.updateMap()

#Create Animat
#a = Animat(0,0,env, filename)

# This should really be inside the animat class, since that's the one that'll make
# a decision on what action to take.


actions = ['north','south','east','west','stay','eat','pickup','drop'];
#state = getState();


for i in range(0,300):
	env.tick()
	#a.tick()
	# Show animat on map, which we'll display
	#env.map[a.y,a.x] = env.map.max();

env.tick()

print 'Finished!'

def getState(self):
	# Pick 1 or 0 for each state, add to total,
	# then shift total << 
	
	# temp states, just for example
	# in reality, this stuff will come from the animat itself
	energyThreshold = 80;
	energy1 = 75;
	energy2 = 82;
	holding1 = true;
	holding2 = false;
	standing1 = true;
	standing2 = true;
	total = 0;
	total += 1 if (energy1 < threshold) else 0;
	total *= 10;
	total += 1 if (energy2 < threshold) else 0;
	total *= 10;
	total += 1 if (holding1) else 0;
	total *= 10;
	total += 1 if (holding2) else 0;
	total *= 10;
	total += 1 if (standing1) else 0;
	total *= 10;
	total += 1 if (standing2) else 0;
	
	# Food gradient choices are 4, can be represented by 2 bits
	total *= 10;
	total *= 10;
	if (food1gradient == 'north'):
		total += 0;
	elif (food1gradient == 'south'):
		total += 1;
	elif (food1gradient == 'south'):
		total += 10;
	elif (food1gradient == 'south'):
		total += 11;
		
	total *= 10;
	total *= 10;
	if (food2gradient == 'north'):
		total += 0;
	elif (food2gradient == 'south'):
		total += 1;
	elif (food2gradient == 'south'):
		total += 10;
	elif (food2gradient == 'south'):
		total += 11;
		
	return int(str(total),2);
	
	
	
	
	
	
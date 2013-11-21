# Sim - Produce test data for animat to train on
# Create an environment, fill it will a bunch of random food.
# Then, iterate across the whole map, saving off the quintiple values surrounding each
# tile. For the edge cases, we'll want to use ZERO for the out of bounds tiles

import sys
sys.path.append("..")

from Environment.Env import Env
import matplotlib.pyplot as plt
from random import choice
import cPickle as pickle
import time

print 'Running Simulation - Make scents'

#Init Environment and food sources
envSize = 1000;
env = Env(envSize)
env.makeGradient()
for i in range (0,70):
	env.makeFoodRandom()
env.updateMap()

fig = plt.figure()
im = plt.imshow(env.map)
im.set_cmap('spectral')
plt.ion()
plt.show()

print 'Making training data...'
t0 = time.clock();
# Traverse
inputTraining = [];
outputTraining = [];
# CEWNS
for y in range(0,envSize):
	for x in range(0,envSize):
		if y == 0:
			north = 0;
		else:
			north = env.map[y-1,x];
		if y == envSize - 1:
			south = 0;
		else:
			south = env.map[y+1,x];
		if x == 0:
			west = 0
		else:
			west = env.map[y,x-1];
		if x == envSize - 1:
			east = 0
		else:
			east = env.map[y,x+1];
		
		center = env.map[y,x];
		
		inputs = [center,east,west,north,south];
		maxVal = max(inputs)
		maxIndex = inputs.index(maxVal)
		inputs = [i/maxVal for i in inputs]
		
		# If more than one direction has the same value, we'll want to randomize how that
		# translate to the output. 
		maxIndeces = [i for i,mymax in enumerate(inputs) if mymax == 1.0]
		randomMaxIndex = choice(maxIndeces);
		outputs = [0,0,0,0,0];
		outputs[randomMaxIndex] = 1;
		
		inputTraining.append(tuple(inputs))
		outputTraining.append(tuple(outputs))
print 'Making data took '+ str(time.clock() - t0) +  'seconds'

# Save to files
print 'Saving to files'
TRAINING_SET_OBJECT_PATH = "../PickledObjects/TrainingSets/"
file_path = TRAINING_SET_OBJECT_PATH + 'scents_based_input'
fd = open(file_path,"wb")
pickle.dump(inputTraining,fd)
fd.close()
file_path = TRAINING_SET_OBJECT_PATH + 'scents_based_output'
fd = open(file_path,"wb")
pickle.dump(outputTraining,fd)
fd.close()
print "Training data  saved at: " + file_path
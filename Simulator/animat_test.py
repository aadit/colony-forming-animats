# Simulation 1
# Create an environment, create an animat
# Have the animat walk around the environment randomly, staying in bounds

# Use a plot tool to show this in real time...?
import matplotlib
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

if len(sys.argv) < 2:
	print "Filename required for neural net"
	exit()

print 'Running Animat Simulations'
#Load initial Neural Net
filename = sys.argv[1] 

#Init Environment and food sources
env = Env(250)
env.makeGradient()
for i in range (1, 2):
	env.makeFoodRandom()
env.updateMap()

#Create Animat
a = Animat(0,0,env, filename)

while(1):
	a.tick()



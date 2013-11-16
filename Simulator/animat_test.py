# Simulation 1
# Create an environment, create an animat
# Have the animat walk around the environment randomly, staying in bounds

# Use a plot tool to show this in real time...?
import matplotlib
import sys
sys.path.append("..")

from Environment.Env import Env
from Animat.Animat import Animat
import time
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print 'Running Animat Simulations'

#Global Environment
env = Env(1000)
animatList = [] #init to empty list

#create a few animats
for x in range(1,100):
	animatList.append(Animat(0,0,env))


while(1):
	for a in animatList:
		a.tick()

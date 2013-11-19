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

print 'Running Animat Simulations'

#Global Environment
env = Env(1000)
animatList = [] #init to empty list

#create a few animats
#for x in range(1,100):
	#animatList.append(Animat(0,0,env))

#print "Added 100 animats"

nni = NNInitializer()
nni.initNetwork()
nni.saveNetwork('nn1.p')

a = Animat(0,0,env)


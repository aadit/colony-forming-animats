# Simulation 1
# Create an environment, create an animat
# Have the animat walk around the environment randomly, staying in bounds

# Use a plot tool to show this in real time...?
import matplotlib
matplotlib.use('TKAgg')

from Env import Env
from Animat import Animat
import time
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

print 'Running Simulation 1'
mapSize = 20
env = Env(mapSize)
a = Animat.randomStart(mapSize,mapSize)

# Create figure for plotting our environment
fig = plt.figure()
ims = []

# Walk around the map randomly, for 100 iterations
for t in range(1,100):
	#time.sleep(.05)
	#print 'Time: '+str(t)
	
	# Pick a random spot to move to
	randomSpot = random.randrange(1,4+1)
	if randomSpot == 1:
		# north
		if env.canMove(a.y,a.x,a.y-1,a.x):
			a.moveNorth()
	elif randomSpot == 2:
		# south
		if env.canMove(a.y,a.x,a.y+1,a.x):
			a.moveSouth()
	elif randomSpot == 3:
		# west
		if env.canMove(a.y,a.x,a.y,a.x-1):
			a.moveWest()
	elif randomSpot == 4:
		# east
		if env.canMove(a.y,a.x,a.y,a.x+1):
			a.moveEast()
			
	# Update the evironment's map with animat's new location
	env.map = zeros((mapSize,mapSize));
	env.map[a.y,a.x] = 1
	
	# animation
	im = plt.imshow(env.map)
	ims.append([im])

# animation
ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True, repeat=False)
plt.show()

print 'Done!'

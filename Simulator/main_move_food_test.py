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

print 'Running Simulation - Moving food around, picking up, dropping'

# Deprecated
filename = 'nn_precise_100k.p'

size = 50;
env1 = Env(size,0)
env2 = Env(size,1);
for i in range (0,20):
	env1.makeFoodRandom();
	env2.makeFoodRandom();
env1.updateMap()
env2.updateMap()

animats = [Animat(25,25,[env1,env2],filename),Animat(10,40,[env1,env2],filename)];

stateMachine = ['notholding','notholding'];

fig = plt.figure()
ims = []

toEat = [random.randrange(0,2),random.randrange(0,2)];
toFollow = [0 if toEat == 1 else 1,0 if toEat == 1 else 1];
for i in range(0,1000):
	env1.tick()
	env2.tick()
	for index,a in enumerate(animats):
		if stateMachine[index] == 'fail':
			toEat[index] = random.randrange(0,2);
			toFollow[index] = 0 if toEat == 1 else 1;
			stateMachine[index] = 'notholding';
		stateMachine[index] = a.followGradient(stateMachine[index],
			toEat[index],toFollow[index]);
		#print str(stateMachine)
		env1.map[a.y,a.x] = env1.map.max();
		env2.map[a.y,a.x] = env2.map.max();
	#if i % 100 == 0:
	print 'Tick: '+str(i);
	im = plt.imshow(env1.map+env2.map)
	im.set_cmap('spectral');
	ims.append([im])

env1.tick()
env2.tick()
	
print 'Finished ticking'

ani = animation.ArtistAnimation(fig, ims, interval=50, blit=True,
	repeat=False)
plt.colorbar()
plt.show()

#print 'Saving animation...'
#ani.save('search_and_destroy.mp4')


print 'Finished!'
import sys
sys.path.append("..")

from Animat.NNInitializer import NNInitializer


if len(sys.argv) < 2:
	print "Need filename for neural net"
	exit()


filename = sys.argv[1] #get filename to save the Neural Network as

nni = NNInitializer()
nni.initNetwork()
nni.saveNetwork(filename)

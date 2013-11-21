from pybrain.structure import FeedForwardNetwork, LinearLayer, SigmoidLayer, FullConnection
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer

import random
import cPickle as pickle


class NNInitializer:

	#A few constants for this function....
	NEURAL_NET_OBJECT_PATH = "../PickledObjects/NeuralNets/"
	TRAINING_SET_OBJECT_PATH = "../PickledObjects/TrainingSets/"
	NUMBER_OF_DATA_SETS = 100000
	NUMBER_OF_INPUTS    = 5
	NUMBER_OF_OUTPUTS   = 5

	def __init__(self):
		pass

	def initNetwork(self):
		#Intiailize Neural Nets
		self.neuralNet = FeedForwardNetwork()

		#Define and add each set of layers
		inLayer = LinearLayer(5)
		hiddenLayer = SigmoidLayer(15)
		outLayer = LinearLayer(5)

		self.neuralNet.addInputModule(inLayer)
		self.neuralNet.addModule(hiddenLayer)
		self.neuralNet.addOutputModule(outLayer)

		#Create conenctions
		in_to_hidden = FullConnection(inLayer, hiddenLayer)
		hidden_to_out = FullConnection(hiddenLayer, outLayer)
		self.neuralNet.addConnection(in_to_hidden)
		self.neuralNet.addConnection(hidden_to_out)

		#Sort the NeuralNet
		self.neuralNet.sortModules()
		
		#Add supervised data sets
		ds = SupervisedDataSet(NNInitializer.NUMBER_OF_INPUTS, NNInitializer.NUMBER_OF_OUTPUTS)
		inputSet, outputSet = self.loadTrainingSet('scents_based_input',
													'scents_based_output')
		#inputSet, outputSet = self.generateTrainingSet()

		print "Adding samples to data set...."
		for i,val  in enumerate(inputSet):
		#	print "Input Set: "
		#	print inputSet[i]
		#	print "Output Set: "
		#	print outputSet[i]
			ds.addSample(inputSet[i], outputSet[i])
		print "Done."

		print "Starting training...."
		#Perform Training
		trainer = BackpropTrainer(self.neuralNet, ds)
		trainer.train()
		print "Done."

	#Generate a training set for the neural net
	def generateTrainingSet(self):
		print "Generating random training samples...."
		
		inputSet = []
		outputSet = []

		for i in range (0, NNInitializer.NUMBER_OF_DATA_SETS):
			trainingInput = [] #start w/ an empty list
			trainingOutput = [0] * NNInitializer.NUMBER_OF_OUTPUTS #start w/ list of all 0's

			for j in range (0, NNInitializer.NUMBER_OF_INPUTS):
				trainingInput.append(random.triangular(0.0, 1.0,0.985)) #add randomInputs between 0 -> 1, inclusive

			#print trainingInput
			maxVal = max(trainingInput)
			maxIndex = trainingInput.index(maxVal)
			trainingInput = [i/maxVal for i in trainingInput]
			trainingOutput[maxIndex] = 1 #the max sense should be the correct movement output

			inputSet.append(tuple(trainingInput))
			outputSet.append(tuple(trainingOutput))

		print "Done."
		return (inputSet, outputSet)

	def loadTrainingSet(self,inputFilename,outputFilename):
		file_path = NNInitializer.TRAINING_SET_OBJECT_PATH + inputFilename
		fd = open(file_path,"rb")
		inputSet = pickle.load(fd)
		fd.close()
		
		file_path = NNInitializer.TRAINING_SET_OBJECT_PATH + outputFilename
		fd = open(file_path,"rb")
		outputSet = pickle.load(fd)
		fd.close()
		
		return (inputSet,outputSet)
	
	def saveNetwork(self,filename):
		file_path = NNInitializer.NEURAL_NET_OBJECT_PATH + filename
		fd = open(file_path,"wb")
		pickle.dump(self.neuralNet,fd)
		fd.close()
		print "Neural net saved at: " + file_path

	def readNetwork(self,filename):
		file_path = NNInitializer.NEURAL_NET_OBJECT_PATH + filename
		fd = open(file_path,"rb")
		self.neuralNet = pickle.load(fd)
		fd.close()
		return self.neuralNet


from Environment.Env import Env
from Animat.Animat import Animat
import time
from numpy import zeros
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from pylab import figure

class Plotter:

	def __init__(self, Animat, plottingIterations):
		self.Animat = Animat
		self.plottingIterations = plottingIterations
		pass


	def plotData(self):
		time = [i for i in range(0,self.plottingIterations)]
		f1 = plt.figure()
		f2 = plt.figure()
		f3 = plt.figure()
		ax1 = f1.add_subplot(111)
		ax1.set_xlabel("Iterations")
		ax1.set_ylabel("Total # of Multiple Foods Eaten")
		ax1.set_title("Cumulative Multiple Food Sources Eaten")
		ax1.plot(time,self.Animat.multipleFoodEaten)
		ax2 = f2.add_subplot(111)
		ax2.set_xlabel("Iterations")
		ax2.set_ylabel("Total # Single Foods Eaten")
		ax2.set_title("Cumulative Single Food Sources Eaten")
		ax2.plot(time,self.Animat.singleFoodEaten)
		ax3 = f3.add_subplot(111)
		ax3.set_xlabel("Iterations")
		ax3.set_ylabel("Net Energy Change (Summed over All Animats)")
		ax3.set_title("Net Energy Change per Tick (Over all Animats)")
		ax3.plot(time,self.Animat.energyPerTick)
		plt.show()


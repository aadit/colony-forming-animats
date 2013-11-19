# Food Generator class
# Has a location
# Has a frequency
# Has a tick function
# When it ticks, it checks to see if its time to generate food.

from numpy import *
import random

class FoodGenerator:

	def __init__(self,y,x,frequency):
		self.y = y;
		self.x = x;
		self.frequency = frequency;
		self.counter = 0;
		
	def tick(self,food):
		if (self.counter == self.frequency):
			self.counter = 0;
			# make food
			food.makeFood(self.y,self.x);
		else:
			self.counter += 1;
			
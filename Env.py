#!/usr/bin/python

from numpy import *

class Env:
	
	def __init__(self,sizeOfSquare):
		self.map = zeros((sizeOfSquare,sizeOfSquare));
		self.size = sizeOfSquare;
		
	def displayMap(self):
		print(self.map)
	
	def displaySize(self):
		print 'Size is ' + str(self.size)
	
	# @classmethod
	def canMove(self,origy, origx, newy, newx):
		# Are the starting and ending locations on the map?
		if (origy < 0 or origy > self.size -1
		or origx < 0 or origx > self.size -1
		or newy < 0 or newy > self.size -1
		or newx < 0 or newx > self.size -1):
			#print "Invalid location entered"
			return False;
			
		# Make sure the new location is one spot above, below, left or right
		if (origy == newy and (origx == newx + 1 or origx == newx - 1)):
			return True;
		elif (origx == newx and (origy == newy + 1 or origy == newy - 1)):
			return True;
		return False;
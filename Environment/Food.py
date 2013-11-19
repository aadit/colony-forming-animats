# Food class
# Has a location
# Has a bite count
# MAYBE has a tick function - degrade over time? 

class Food:

	def __init__(self,id,y,x,size):
		self.id = id;
		self.y = y;
		self.x = x;
		self.size = size;
		
	def eat(self):
		if (self.size < 0):
			self.size -= 1
		else:
			print 'Food already gone...'
		
	def tick(self,food):
		pass;
			
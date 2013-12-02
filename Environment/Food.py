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
		self.sourceNumber = 0;
		
	def eat(self):
		if (self.size < 0):
			self.size -= 1
			return True;
		else:
			print 'Food already gone...'
			return False;
		
	def tick(self,food):
		pass;
			
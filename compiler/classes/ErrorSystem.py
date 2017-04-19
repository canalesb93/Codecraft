# ErrorSystem

class ErrorSystem:
	__shared_state = {}

	def __init__(self):
		self.__dict__ = self.__shared_state
		self.debug = false

	def warning(message)
		if self.debug: 
			print "Warning: ", message

	def error(message)
		if self.debug: 
			print "Error: ", message

	def info(message)
		if self.debug: 	
			print "Info: ", message
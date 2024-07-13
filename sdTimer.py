# Completed : 03-December-2021

import threading as objLibThreading

# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-objFunction-every-x-seconds
class clTimer:
	def __init__(self, iInterval, objFunction, *args, **kwargs):
		self.Timer = None
		self.iInterval = iInterval
		self.objFunction = objFunction
		self.args = args
		self.kwargs = kwargs
		self.bRunning = False
	# End of __init__()
	
	def LaunchCallbackFunction(self):
		objThread = objLibThreading.Thread(target=self.objFunction, args=self.args, kwargs=self.kwargs)
		objThread.start()
	# End of LaunchCallbackFunction()

	def Run(self):
		self.bRunning = False
		if self.iInterval > 0:
			self.Start()
		# End of if
		self.LaunchCallbackFunction()		
	# End of Run()
	
	def SetInterval(self, iInterval):
		self.Stop()
		if iInterval >= 0:
			self.iInterval = iInterval
			self.Start()
		# End of if
	# End of SetInterval()

	def Start(self):
		if not self.bRunning:
			self.Timer = objLibThreading.Timer(self.iInterval, self.Run)
			self.Timer.start()
			self.bRunning = True
		# End of if
	# End of start()

	def Stop(self):
		if self.bRunning:
			self.Timer.cancel()
			self.bRunning = False
		 # End of if
	# End of Stop()
# End of class clTimer

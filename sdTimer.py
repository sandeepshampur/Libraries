#
# Completed : 03-December-2021
#
# Enhancement	: 30-Jul-2024 : Revamped logic
#

import threading as objLibThreading

# https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-objFunction-every-x-seconds
class clTimer:
	def __init__(self, objFunction, iInterval=0, *args):
		self.objFunction = objFunction
		self.iInterval = iInterval
		self.args = args

		self.Timer = None
		self.bTimerOn = False
		self.objLock = objLibThreading.Lock()
	# End of __init__()

	def GetArgs(self):
		return self.args
	# End of GetArgs()

	def Run(self):
		self.objLock.acquire() # Lock
		self.bTimerOn = False
		self.objLock.release() # Unlock
		self.objFunction(*self.args)
	# End of Run()

	def SetArgs(self, *args):
		self.args = args
	# End of SetArgs()

	def SetInterval(self, iInterval):
		if self.iInterval != iInterval:
			self.Stop()
			self.iInterval = iInterval
			self.Start()
		# End of if
	# End of SetInterval()

	def Start(self):
		if not self.bTimerOn:
			self.objLock.acquire() # Lock
			self.Timer = objLibThreading.Timer(self.iInterval, self.Run)
			self.bTimerOn = True
			self.Timer.start()
			self.objLock.release() # Unlock
		# End of if
	# End of start()

	def Stop(self):
		self.objLock.acquire() # Lock
		if self.Timer is not None:
			self.Timer.cancel()
			self.bTimerOn = False
		# End of if
		self.objLock.release() # Unlock
	# End of Stop()
# End of class clTimer

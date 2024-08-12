#
# Completed: 14-December-2021
#
# Enhancement : 27-Mar-2022 : Added class clPipe
#
# Ubuntu Porting
# Started 	: 26-June-2024
# Completed : 26-June-2024
#
# Enhancement : 27-Jun-2024 : 1. Redesigned to ensure reading and writing is non-blocking
#							  2. Added code to ensure that Read() returns exactly the same chunk of data written by each Write()
# Enhancement : 12-Aug-2025 : 1. Revamped logic
# 							  2. Added blocking and non-blocking read and write calls
#							  3. Added logging
#

import os as objLibOS
import queue as objLibQueue
import threading as objLibThreading
import time as objLibTime

class clNamedPipe:
	def __init__(self, strConnectionMode, strIOMode, strPipeName, objLoggerLog):
		'''
		strConnectionMode = "Client"|"Server"
		strIOMode = "Blocking"|"NonBlocking"
		'''
		self.strConnectionMode = strConnectionMode
		self.strIOMode = strIOMode
		self.strPipeName = strPipeName
		self.iDataQCount = 0
		self.objLock = objLibThreading.Lock()
		self.objLoggerLog = objLoggerLog

		# Create pipe if not present
		try:
			objLibOS.mkfifo(self.strPipeName)
		except:
			pass
		# End of try / except

		# Queue
		self.objPipeQueue = objLibQueue.Queue()
		self.objDataQueue = objLibQueue.Queue()

		# Thread
		objLibThreading.Thread(target=self.PipeThread, daemon=True).start()
	# End of __init__()

	def CleanUp(self):
		# Remove pipe file if present
		if objLibOS.path.exists(self.strPipeName):
			objLibOS.remove(self.strPipeName)
		# End of if
	# End of CleanUp()

	def Peek(self):
		if self.objLoggerLog is not None:
			self.objLoggerLog("self.iDataQCount:", self.iDataQCount)
		# End of if
		return self.iDataQCount
	# End of Client()

	def Read(self):
		for x in range(1):
			strData = ""

			if self.strConnectionMode.find("Server") == 0:
				strData = "ERROR: Server cannot read from pipe"
				if self.objLoggerLog is not None:
					self.objLoggerLog("ERROR: Server cannot read from pipe")
				# End of if
				break
			# End of if

			if self.strIOMode.find("Blocking") == 0:
				strData = self.objDataQueue.get()
				self.objDataQueue.task_done()

				self.objLock.acquire()
				self.iDataQCount -= 1
				self.objLock.release()

				if self.objLoggerLog is not None:
					self.objLoggerLog("Blocking: self.iDataQCount", self.iDataQCount)
				# End of if
				break
			# End of if

			# Non-blocking
			if self.iDataQCount > 0:
				strData = self.objDataQueue.get()
				self.objDataQueue.task_done()

				self.objLock.acquire()
				self.iDataQCount -= 1
				self.objLock.release()

				if self.objLoggerLog is not None:
					self.objLoggerLog("Non-Blocking: self.iDataQCount", self.iDataQCount)
				# End of if
			# End of if
		# End of for loop

		if self.objLoggerLog is not None:
			self.objLoggerLog("Data length: ", len(strData))
		# End of if
		return strData
	# End of ReadBlocking()

	def PipeThread(self):
		while 1:
			match self.strConnectionMode:
				case "Client":
					with open(self.strPipeName, "r") as objPipe:
						strData = objPipe.read()
					# End of with

					self.objLock.acquire()
					self.iDataQCount += 1
					self.objLock.release()

					self.objDataQueue.put(strData)
					if self.objLoggerLog is not None:
						self.objLoggerLog("Thread Client: self.iDataQCount:", self.iDataQCount, "Data length: ", len(strData))
					# End of if
				# End of case

				case "Server":
					strData = self.objPipeQueue.get()
					self.objPipeQueue.task_done()

					with open(self.strPipeName, "w") as objPipe:
						strMessage = objPipe.write(strData)
					# End of with

					self.objLock.acquire()
					self.iDataQCount -= 1
					self.objLock.release()

					if self.strIOMode.find("Blocking") == 0:
						self.objDataQueue.put("Done")
					# End of if

					if self.objLoggerLog is not None:
						self.objLoggerLog("Thread Server: self.iDataQCount:", self.iDataQCount, "Data length: ", len(strData))
					# End of if
				# End of case
			# End of match
		# End of while
	# End of ThreadPipeIO()

	def Write(self, strMessage):
		for x in range(1):
			strError = ""

			if self.strConnectionMode.find("Client") == 0:
				strData = "ERROR: Client cannot write to pipe"
				if self.objLoggerLog is not None:
					self.objLoggerLog("ERROR: Client cannot write to pipe")
				# End of if
				break
			# End of if

			self.objLock.acquire()
			self.iDataQCount += 1
			self.objLock.release()

			self.objPipeQueue.put(strMessage)

			if self.strIOMode.find("Blocking") == 0:
				self.objDataQueue.get()
				self.objDataQueue.task_done()
			# End of if
		# End of for loop

		if self.objLoggerLog is not None:
			self.objLoggerLog("Data length: ", len(strData))
		# End of if
		return strError
	# End of WriteBlocking()
# End of class clPipe

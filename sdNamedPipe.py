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
#

import os as objLibOS
import queue as objLibQueue
import threading as objLibThreading

class clNamedPipe:
	def __init__(self, strPipeName="sdNamedPipe"):
		self.strPipeName = strPipeName
		self.strBuffer = ""
		self.iCount = 0
		self.strType = ""
		self.strSignature = "|!@#$%|"

		# Create queues abd thread
		self.objMessageQ = objLibQueue.Queue()
		self.objPipeQ = objLibQueue.Queue()
		objLibThreading.Thread(target=self.ThreadPipeIO, daemon=True).start()
	# End of __init__()

	def CleanUp(self):
		# Remove pipe file if present
		if objLibOS.path.exists(self.strPipeName):
			objLibOS.remove(self.strPipeName)
		# End of if
	# End of CleanUp()

	def Client(self):
		self.strType = "Client"
	# End of Client()

	def GetData(self):
		for x in range(1):
			strResult = ""
			strData = ""
			if self.iCount != 0:
				strData = self.objMessageQ.get()
				self.objMessageQ.task_done()
				self.iCount -= 1
			# End of if

			# Add data to previously read data if any
			self.strBuffer = "".join([self.strBuffer, strData])

			# Get location of first and second signature
			iStartSig = self.strBuffer.find(self.strSignature)
			if iStartSig == -1:
				break
			# End of if

			iEndSig = self.strBuffer.find(self.strSignature, iStartSig+1)
			if iEndSig == -1:
				break
			# End of if

			# Get resulting string between signatures
			strResult = self.strBuffer[iStartSig+len(self.strSignature):iEndSig]

			# Add left over data to buffer
			self.strBuffer = self.strBuffer[iEndSig+len(self.strSignature):]
		# End of for loop

		return strResult
	# End of Client()

	def Peek(self):
		bResult = False
		if len(self.strBuffer) > 0 or self.iCount > 0:
			bResult = True
		# End of if

		return bResult
	# End of Client()

	def Read(self):
		strResult = ""
		for x in range(1):
			if self.strType == "Server":
				strResult = "Error : Only clients can read from the pipe"
				break
			# End of if

			self.objPipeQ.put(["Read", strResult])
			if self.iCount == 0 and len(self.strBuffer) == 0:
				break
			# End of if

			strResult = self.GetData()
		# End of for loop

		return strResult
	# End of Read()

	def Server(self):
		self.strType = "Server"
		self.CleanUp()

		# Create pipe
		objLibOS.mkfifo(self.strPipeName)
	# End of Server()

	def ThreadPipeIO(self):
		while 1:
			arrValue = self.objPipeQ.get()
			self.objPipeQ.task_done()

			if arrValue[0] == "Read":
				try:
					with open(self.strPipeName, "r") as objPipe:
						strMessage = objPipe.read()
						self.iCount += 1
					# End of with
				except:
					pass
				# End of try / except
				self.objMessageQ.put(strMessage)
			# End of if

			if arrValue[0] == "Write":
				try:
					with open(self.strPipeName, "w") as objPipe:
						objPipe.write(arrValue[1])
						objPipe.flush()
					# End of with
				except:
					pass
				# End of try / except
			# End of if
		# End of while loop
	# End of ThreadPipeIO()

	def Write(self, strMessage):
		for x in range(1):
			if self.strType == "Client":
				strResult = "Error : Only servers can write to the pipe"
			# End of if

			# Add signature to message so that read sends back exactly the same amount of data to reader
			strMessage = "".join([self.strSignature, strMessage, self.strSignature])

			self.objMessageQ.put(strMessage)
			self.objPipeQ.put(["Write", strMessage])
			strResult = "Success"
		# Emd of for loop

		return strResult
	# End of Write()
# End of class clPipe

#
# Completed : 20-December-2021
#
# Fix : 22-Mar-2022 : Fixed code in "Dump()" where log file was being overwritten though size was within limit
#

import datetime as objLibDateTime
import os as objLibOS
import queue as objLibQueue
from tempfile import gettempdir as objLibTempDir
import threading as objLibThreading
from time import time as objLibCurrentTime
from traceback import extract_stack as objLibTBGetStack

class clLogger:
	def __init__(self, iLogLevel=0, iFileSize=67108864, strPath="", strFileName=""):
		self.strPath = ""
		self.strFileName = ""
		self.strFilePath = ""
		self.iFileSize = int(67108864)
				
		# Log level
		self.LogLevel = int(iLogLevel)
		
		# File size
		if int(iFileSize) > 0:
			self.iFileSize = int(iFileSize)
		# End of if
		
		# Path
		self.SetPath(strPath)
		
		# File name
		self.SetFileName(strFileName)

		# Initialise queue
		self.LogQueue = objLibQueue.Queue()		
		
		self.arrLogs = []
		
		# Start thread
		objLibThreading.Thread(target=self.Thread, daemon=True).start()
	# End of __init__()
	
	def ClearLogs(self):
		self.arrLogs.clear()
	# End of ClearLogs()
	
	def Dump(self):
		if self.LogLevel == 0:
			return
		# End of if
		
		# Form string
		self.arrLogs.append("")
		strLogs = "\n".join(self.arrLogs)		
		self.arrLogs.clear()
		
		# Check log file size
		bOverwrite = False
		try:
			iFileSize = objLibOS.path.getsize(self.strFilePath) + len(strLogs)
			if iFileSize > self.iFileSize:
				bOverwrite = True
			# End of if
		except:
			pass
		# End of try / except
		if bOverwrite:
			cFileMode = "w"
		else:
			cFileMode = "a"
		# End of if

		with open(self.strFilePath, cFileMode) as objFile:
			objFile.write(strLogs)
	# End of Dump()

	def Log(self, *args):
		if self.LogLevel == 0:
			return
		# End of if
		
		# Get caller function name
		objStack = objLibTBGetStack(limit=2)
		arrFunction = objStack.format()
		strFunction = arrFunction[0]
		iPosEnd = strFunction.find("\n")
		iPos = strFunction.rfind(" in ", 0, iPosEnd)
		strFunction = strFunction[iPos+4:iPosEnd]

		# Get time stamp
		fDtTm = objLibCurrentTime()
		strTimeStamp = "*".join([str(fDtTm), objLibDateTime.datetime.fromtimestamp(fDtTm).strftime("%Y-%m-%d %H:%M:%S.%f")])
		
		# Get arguments
		strArguments = " ".join(map(str, args))
		
		# Add to list
		strLog = "*".join([strTimeStamp, strFunction, strArguments])
		self.LogQueue.put(strLog)		
		
		# Print if required
		if self.LogLevel == 2:
			print(strTimeStamp, strFunction, *args)
		# End of if
	# End of Log()

	def SetFileName(self, strFile):
		if len(strFile) != 0:
			self.strFileName = strFile
		else:
			self.strFileName = "DebugLogs.txt"
		# End of if
		
		self.SetFullPath()
	# End of SetFileName()	
	
	def SetFullPath(self):
		self.strFilePath = "".join([self.strPath, self.strFileName])		
	# End of SetFullPath()
	
	def SetLevel(self, iLogLevel):
		self.LogLevel = int(iLogLevel)
	# End of SetLevel()
	
	def SetFileSize(self, iFileSize):
		self.iFileSize = int(iFileSize)
	# End of SetFileSize()

	def SetPath(self, strPath):
		# Path
		if (len(strPath) != 0) and objLibOS.path.isdir(strPath):
			self.strPath = strPath
		else:
			# Temp directory
			self.strPath = objLibTempDir()
		# End of if
		if self.strPath[-1:] != objLibOS.sep:
			self.strPath = "".join([self.strPath, objLibOS.sep])
		# End of if
		
		self.SetFullPath()
	# End of SetPath()	

	def Thread(self):
		while 1:
			arrValues = self.LogQueue.get()

			self.arrLogs.append(arrValues)
			
			self.LogQueue.task_done()
		# End of while loop
	# End of Thread()	
# End of class clLogger

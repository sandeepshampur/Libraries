#
# Completed : 20-December-2021
#
# Fix 		  : 22-Mar-2022 : Fixed code in "Dump()" where log file was being overwritten though size was within limit
#
# Enhancement : 28-Jul-2024 : 1. Added default values to function parameters
#							  2. Moved code to get current log file size out of "Dump()" to "__init__()"
#							  3. Moved code to form log line from "Log()" to "Thread()"
#

import datetime as objLibDateTime
import os as objLibOS
from os.path import join as objLibOSPathJoin
import queue as objLibQueue
from tempfile import gettempdir as objLibTempDir
import threading as objLibThreading
from time import time as objLibCurrentTime
from traceback import extract_stack as objLibTBGetStack

class clLogger:
	def __init__(self, iLogLevel=0, iFileSize=-1, strPath="", strFileName=""):
		self.strPath = ""
		self.strFileName = ""
		self.strFilePath = ""

		self.LogLevel = int(iLogLevel)
		self.SetFileSize(iFileSize)
		self.SetPath(strPath, True)
		self.SetFileName(strFileName, True)
		self.SetFullPath()

		self.LogQueue = objLibQueue.Queue()
		self.arrLogs = []

		# Check log file size
		self.iCurrentLogFileSize = 0
		if objLibOS.path.isfile(self.strFilePath):
			self.iCurrentLogFileSize = objLibOS.path.getsize(self.strFilePath)
		# End of if

		# Thread
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
		cFileMode = "a"
		if (self.iCurrentLogFileSize + len(strLogs)) > self.iFileSize:
			cFileMode = "w"
		# End of if

		with open(self.strFilePath, cFileMode) as objFile:
			objFile.write(strLogs)
			objFile.flush()
		# End of with
	# End of Dump()

	def Log(self, *args):
		for x in range(1):
			if self.LogLevel == 0:
				break
			# End of if

			# Get caller function name
			objStack = objLibTBGetStack(limit=2)
			self.LogQueue.put([objStack, args])
		# End of for loop
	# End of Log()

	def SetFileName(self, strFile="", bInit=False):
		if len(strFile) != 0:
			self.strFileName = strFile
		else:
			self.strFileName = "DebugLogs.txt"
		# End of if

		if not bInit:
			self.SetFullPath()
		# End of if
	# End of SetFileName()

	def SetFileSize(self, iFileSize=-1):
		if iFileSize == -1:
			self.iFileSize = int(67108864)
		else:
			self.iFileSize = int(iFileSize)
		# End of if
	# End of SetFileSize()

	def SetFullPath(self):
		self.strFilePath = objLibOSPathJoin(self.strPath, self.strFileName)
	# End of SetFullPath()
	
	def SetLevel(self, iLogLevel=0):
		self.LogLevel = int(iLogLevel)
	# End of SetLevel()
	
	def SetPath(self, strPath="", bInit=False):
		# Path
		if (len(strPath) != 0) and objLibOS.path.isdir(strPath):
			self.strPath = strPath
		else:
			# Temp directory
			self.strPath = objLibTempDir()
		# End of if

		self.strPath = objLibOSPathJoin(self.strPath, "")

		if not bInit:
			self.SetFullPath()
		# End of if
	# End of SetPath()	

	def Thread(self):
		while 1:
			arrValues = self.LogQueue.get()
			self.LogQueue.task_done()

			# Get function name
			arrFunction = arrValues[0].format()
			strFunction = arrFunction[0]
			iPosEnd = strFunction.find("\n")
			iPos = strFunction.rfind(" in ", 0, iPosEnd)
			strFunction = strFunction[iPos+4:iPosEnd]

			# Get time stamp
			fDtTm = objLibCurrentTime()
			strTimeStamp = "*".join([str(fDtTm), objLibDateTime.datetime.fromtimestamp(fDtTm).strftime("%Y-%m-%d %H:%M:%S.%f")])

			# Get arguments
			strArguments = " ".join(map(str, arrValues[1]))

			# Add to list
			strLog = "*".join([strTimeStamp, strFunction, strArguments])

			# Print if required
			if self.LogLevel == 2:
				print(strLog)
			# End of if

			self.arrLogs.append(strLog)
		# End of while loop
	# End of Thread()	
# End of class clLogger

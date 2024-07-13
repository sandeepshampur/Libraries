#
# Completed : 20-December-2021
#
# Fix : 23-Mar-2022 : Added "WriteQ" to allow time to write to file
#

from configparser import ConfigParser as objLibConfigParser
import os as objLibOS
import queue as objLibQueue
import threading as objLibThreading

class clIniParser:
	def __init__(self, strIniFile):
		self.strIniFile = strIniFile
		self.bReplaceSection = True		
		
		# Read ini file
		self.objIniParser = objLibConfigParser()
		self.objIniParser.optionxform = str
		self.objIniParser.read(self.strIniFile)
		
		# Initialise queues
		self.IniQ = objLibQueue.Queue()
		self.WriteQ = objLibQueue.Queue()
		
		# Start writer daemon thread
		objLibThreading.Thread(target=self.Thread, daemon=True).start()
	# End of __init__()

	def GetItem(self, strSection, strKey=""):
		for x in range(1):
			if len(strKey) == 0:
				try:
					strValue = self.objIniParser.items(strSection)
				except:
					strValue = []
				# End of try / except
				break
			# End of if

			try:
				strValue = self.objIniParser.get(strSection, strKey)
			except:
				strValue = ""
			# End of try / except
		
		return strValue
	# End of Read()
	
	def ParseValue(self, strValue, strDelimeter="|-|"):
		dictValue = {}
		arrValue = strValue.split(strDelimeter)
		
		for strItem in arrValue:
			iPos = strItem.find("=")
			strKey = strItem[:iPos]
			dictValue[strKey] = strItem[iPos+1:]
		# End of for loop
		
		return dictValue
	# End of ParseValue()

	def SetItems(self, arrValues=[], bReplaceSection=True):
		self.bReplaceSection = bReplaceSection
		self.IniQ.put(arrValues)
	# End of WriteItems()
	
	def SaveToFile(self):
		self.IniQ.put([[""]])
		self.WriteQ.get()
		self.WriteQ.task_done()
	# End of SaveToFile()
	
	def Thread(self):
		while 1:
			arrValues = self.IniQ.get()
			self.IniQ.task_done()
			strSection = arrValues[0][0]
			
			for x in range(1):
				# Check if this is to write to file
				if len(strSection) == 0:
					objFile = open(self.strIniFile, "w")
					self.objIniParser.write(objFile, space_around_delimiters=False)
					objFile.close()
					self.WriteQ.put("Done")
					break
				# End of if

				# Delete section if required
				if self.bReplaceSection and (self.objIniParser.has_section(strSection)):
					self.objIniParser.remove_section(strSection)
				# End of if
				
				# Add section if not prsent
				if not self.objIniParser.has_section(strSection):
					self.objIniParser.add_section(str(strSection))
				# End of if

				for arrValue in arrValues:
					self.objIniParser.set(str(arrValue[0]), str(arrValue[1]), str(arrValue[2]))
				# End of for loop			
			# End of for loop
		# End of while loop
	# End of Thread()
# End of class clIniParser

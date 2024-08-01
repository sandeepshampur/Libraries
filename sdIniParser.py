#
# Completed : 20-December-2021
#
# Fix 		  : 23-Mar-2022 : Added "WriteQ" to allow time to write to file
# Enhancement : 01-Aug-2024 : 1. Added "ExtendedInterpolation" feature for reading INI file
#							  2. Revamped logic
#

from configparser import ConfigParser as objLibConfigParser
from configparser import ExtendedInterpolation as optExtendedInterpolation
import os as objLibOS
import queue as objLibQueue
import threading as objLibThreading

class clIniParser:
	def __init__(self, strIniFile):
		self.strIniFile = strIniFile

		# Read ini file
		self.objIniParser = objLibConfigParser(interpolation=optExtendedInterpolation())
		self.objIniParser.optionxform = str
		self.objIniParser.read(self.strIniFile)
	# End of __init__()

	def GetItem(self, strSection, strKey=""):
		for x in range(1):
			# Get enitre section ------------------------------------------
			if len(strKey) == 0:
				try:
					objValue = self.objIniParser.items(strSection)
					break
				except:
					pass
				# End of try / except

				# Get raw data if present
				try:
					objValue = self.objIniParser.items(strSection, raw=True)
				except:
					objValue = []
					break
				# End of try / except

				objValue = self.ReplaceInterpolationValues(objValue)
				break
			# End of if

			# Get only key / value pair ------------------------------------
			try:
				objValue = self.objIniParser.get(strSection, strKey)
				break
			except:
				pass
			# End of try / except

			# Get raw data if present
			try:
				objValue = self.objIniParser.get(strSection, strKey, raw=True)
			except:
				objValue = []
				break
			# End of try / except

			objValue = self.ReplaceInterpolationValues(objValue)
		# End of for loop

		return objValue
	# End of GetItem()
	
	def ParseValue(self, strValue, strDelimeter="|-|"):
		'''
		Creates dictionary based on delimeter
		E.g. INI entry: "img=Notepad.png|-|type=shell|-|check=no|-|path=gedit"
			 dictionary : {
			 	"img": "Notepad.png",
			 	"type": "shell",
			 	"check": "no",
			 	"path": "gedit"
			 }
		'''
		dictValue = {}
		arrValue = strValue.split(strDelimeter)
		
		for strItem in arrValue:
			iPos = strItem.find("=")
			strKey = strItem[:iPos]
			dictValue[strKey] = strItem[iPos+1:]
		# End of for loop
		
		return dictValue
	# End of ParseValue()

	def ReplaceInterpolationValues(self, objRaw):
		for x in range(1):
			# Handle string
			if isinstance(objRaw, str):
				objRaw = self.ReplaceInterpolationValuesInString(objRaw)
				break
			# End of if

			# Handle list (array)
			arrRaw = []
			for tRaw in objRaw:
				strKey = tRaw[0]
				strValue = tRaw[1]
				strValue = self.ReplaceInterpolationValuesInString(strValue)

				arrRaw.append([strKey, strValue])
			# End of for loop

			objRaw.clear()
			objRaw = arrRaw
		# End of for loop

		return objRaw
	# End of ReplaceInterpolationValues()

	def ReplaceInterpolationValuesInString(self, strValue):
		while(1):
			iStartPos = strValue.find("${")
			iEndPos = strValue.find("}", iStartPos+1)

			if (iStartPos == -1) or (iEndPos == -1):
				break
			# End of if

			strValue = "".join([str(strValue[:iStartPos]), "<Missing>", str(strValue[iEndPos+1:])])
		# End of while loop

		return strValue
	# End of ReplaceInterpolationValuesInString()

	def SaveToFile(self):
		objFile = open(self.strIniFile, "w")
		self.objIniParser.write(objFile, space_around_delimiters=False)
		objFile.flush()
		objFile.close()
	# End of SaveToFile()

	def SetItem(self, strSection, strKey, strValue):
		# Add section if not prsent
		if not self.objIniParser.has_section(strSection):
			self.objIniParser.add_section(str(strSection))
		# End of if

		self.objIniParser.set(str(strSection), str(strKey), str(strValue))
	# End of SetItem()

	def SetItems(self, strSection, arrKeyValuePairs, bReplaceSection=False):
		'''
		arrKeyValuePairs = [
						["Key", "Value"],
						...
					]
		'''
		# Delete section if required
		if bReplaceSection and (self.objIniParser.has_section(strSection)):
			self.objIniParser.remove_section(strSection)
		# End of if

		# Add section if not prsent
		if not self.objIniParser.has_section(strSection):
			self.objIniParser.add_section(str(strSection))
		# End of if

		for arrKeyValuePair in arrKeyValuePairs:
			self.objIniParser.set(str(strSection), str(arrKeyValuePair[0]), str(arrKeyValuePair[1]))
		# End of for loop
	# End of SetItems()
# End of class clIniParser

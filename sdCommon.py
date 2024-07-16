#
# Completed: 16-July-2024
#

import os as objLibOS
from os.path import isfile as objLibOSIsFile
from os.path import join as objLibOSPathJoin
import sdDatabase as objLibDatabase
import sdIniParser as objLibIniParser
import sdLogger as objLibLogger
from tkinter import font as objLibTkFont
from tkinter import ttk as objLibTTK

class clCommon:
	def __init__(self):
			self.dictInfo = {
				"Font": {},
				"Functions": {},
				"Screen": {
					"Width": 0,
					"Height": 0
				},
			}
	# End of __init__()

	def CheckEnvironment(self):
		# Initialise working directory
		strPath = objLibOS.path.abspath(self.dictParam["strPath"])
		arrPath = objLibOS.path.split(strPath)
		strPath = objLibOSPathJoin(arrPath[0], "")
		self.strWorkingDir = strPath
		self.dictInfo["WorkingDir"] = strPath

		arrError = []
		if "Environment" in self.dictParam:
			for strDir in self.dictParam["Environment"]:
				arrFiles = self.dictParam["Environment"][strDir]

				for strFile in arrFiles:
					strFilePath = objLibOSPathJoin(self.strWorkingDir, strDir, strFile)
					if not objLibOSIsFile(strFilePath):
						strMsg = "".join([strDir, "/", strFile])
						arrError.append(strMsg)
					# End of if
				# End of for loop
			# End of for loop

			if len(arrError) > 0:
				arrError.insert(0, "Missing Files:")
			# End of if
		# End of if
		strError = "\n".join(arrError)

		return strError
	# End of Check()

	def CreateFunctions(self):
		if "Functions" not in self.dictParam:
			return
		# End of if

		if "INI" in self.dictParam["Functions"]:
			arrEntry = self.dictParam["Functions"]["INI"]
			strPath = objLibOSPathJoin(self.strWorkingDir, arrEntry[0], arrEntry[1])
			objIniParser = objLibIniParser.clIniParser(strPath)
			self.dictInfo["Functions"]["INI"] = objIniParser
		# End of if

		if "Logger" in self.dictParam["Functions"]:
			arrEntry = self.dictParam["Functions"]["Logger"]
			strPath = objLibOSPathJoin(self.strWorkingDir, arrEntry[0])
			iLogLevel = objIniParser.GetItem("Logger", "Level")
			if len(iLogLevel) == 0:
				iLogLevel = 0
			else:
				iLogLevel = int(iLogLevel)
			# End of if
			iFileSize = objIniParser.GetItem("Logger", "Size")
			if len(iFileSize) == 0:
				iFileSize = 0
			else:
				iFileSize = int(iFileSize)
			# End of if

			objFunction = objLibLogger.clLogger(iLogLevel=iLogLevel, strPath=strPath, strFileName=arrEntry[1], iFileSize=iFileSize)
			self.dictInfo["Functions"]["Logger"] = objFunction
		# End of if

		if "Database" in self.dictParam["Functions"]:
			arrEntry = self.dictParam["Functions"]["Database"]
			strPath = objLibOSPathJoin(self.strWorkingDir, arrEntry[0], arrEntry[1])
			objFunction = objLibDatabase.clDatabase(strPath, self.strWorkingDir, objLogger.Log)
			self.dictInfo["Functions"]["Logger"] = objFunction
		# End of if
	# End of CreateFunctions()

	def GetFontInfo(self, strKey="", strText="", strFamily="", iSize=0, strWeight="normal"):
		strValue = "Error"
		bNewFont = False
		if iSize == 0:
			iSize = self.iFontSize
		# End of if

		if len(strFamily) == 0:
			objFont = self.objDefaultFont
		else:
			objFont = objLibTkFont.Font(family=strFamily, size=iSize, weight=strWeight)
		# End of if

		match strKey:
			case "FontSize":
				strValue = self.iFontSize
			# End of case

			case "TextHeight":
				strValue = objFont.metrics("linespace")
			# End of case

			case "TextWidth":
				if len(strText) == 0:
					strValue = objFont.measure("W")
				else:
					strValue = objFont.measure(strText)
				# End of if
			# End of case
		# End of match

		return strValue
	# End of ScreenInfo()

	def GetFunctionInfo(self, strKey):
		objValue = None

		if strKey in self.dictInfo["Functions"]:
			objValue = self.dictInfo["Functions"][strKey]
		# End of if

		return objValue
	# End of GetFunctionInfo()

	def GetScreenInfo(self, strKey):
		strValue = "Error"

		if strKey in self.dictInfo["Screen"]:
			strValue = self.dictInfo["Screen"][strKey]
		# End of if

		return strValue
	# End of ScreenInfo()

	def GetWorkingDir(self):
		return self.dictInfo["WorkingDir"]
	# End of GetWorkingDir()

	def Initialise(self, dictParam):
		'''
		dictParam = {
			"Environment": {
				"Data": ["ControlPanel.ini"],
				"Icons": ["About.xbm"],
				"Img": ["About.png"],
				"Sound": ["Battery.mp3"]
			},
			"FontSize": 10,
			"Functions": {
				"INI": ["Data", "ControlPanel.ini"],
				"Logger": ["Data", "ControlPanelLogs.txt"],
				"Database": ["Data", "ControlPanel.db"]
			},
			"strPath": __file__
		}
		'''
		for x in range(1):
			self.dictParam = dictParam

			# Check environment
			strError = self.CheckEnvironment()
			if len(strError) > 0:
				break
			# End of if

			# Variables
			self.dictParam = dictParam
			self.iFontSize = dictParam["FontSize"]
			self.CreateFunctions()
		# End of for loop

		return strError
	# End of Initialise()

	def InitialiseScreenInfo(self, objWindow, bSetTheme=True):
		# Screen dimensions
		self.dictInfo["Screen"]["Width"] = objWindow.winfo_screenwidth()
		self.dictInfo["Screen"]["Height"] = objWindow.winfo_screenheight()

		# Screen ratios
		self.fScrRatioW = float(self.dictInfo["Screen"]["Width"] / 1920)
		self.fScrRatioH = float(self.dictInfo["Screen"]["Height"] / 1080)

		# Font size
		iMappedFontSize = round(self.iFontSize * self.fScrRatioW)
		objFont = objLibTkFont.nametofont("TkDefaultFont")
		objFont.config(size=iMappedFontSize)
		objFont = objLibTkFont.nametofont("TkTextFont")
		objFont.config(size=iMappedFontSize)
		objFont = objLibTkFont.nametofont("TkHeadingFont")
		objFont.config(size=iMappedFontSize)
		self.objDefaultFont = objLibTkFont.Font(font="TkDefaultFont")

		if bSetTheme:
			self.SetTheme()
		# End of if
	# End of Initialise()

	def MapToScreenRatioH(self, iH):
		return round(iH * self.fScrRatioH)
	# End of ScrRatioH()

	def MapToScreenRatioW(self, iW):
		return round(iW * self.fScrRatioW)
	# End of ScrRatioW()

	def SetTheme(self):
		objStyle = objLibTTK.Style()
		objStyle.theme_use("clam")
		objStyle.map("TCombobox", selectforeground=[('readonly', '!focus', 'black'), ('readonly', 'focus', 'white')],
					 selectbackground=[('readonly', '!focus', 'white')], fieldbackground=[('readonly', '!focus', 'white'),
					('disabled', '#DCDAD5')], foreground=[('readonly', '!focus', 'black')])
	# End of SetTheme()
# End of class clCommon

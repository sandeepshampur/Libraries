#
# Completed: 13-August-2024
#


#											IMPORTANT
# Below naming convention has to be used to import "sd*" libraries to avoid failure of "GetLibrary()" function
# E.g. sdCanvas as objLibSDCanvas ie, add "objLib" to the beginning and capitalise "sd" to "SD"
#

import ast as objLibAST
import os as objLibOS
from os.path import join as objLibOSPathJoin
import sdCanvas as objLibSDCanvas
import sdCharts as objLibSDCharts
import sdCheckbutton as objLibSDCheckbutton
import sdChecksum as objLibSDChecksum
import sdDatabase as objLibSDDatabase
import sdDatePicker as objLibSDDatePicker
import sdEntryWidget as objLibSDEntryWidget
import sdIniParser as objLibSDIniParser
import sdInput as objLibSDInput
import sdListBoxMultiColumn as objLibSDListBoxMultiColumn
import sdLogger as objLibSDLogger
import sdMessageBox as objLibSDMessageBox
import sdNamedPipe as objLibSDNamedPipe
import sdNotification as objLibSDNotification
import sdNumberRange as objLibSDNumberRange
import sdProgressBar as objLibSDProgressBar
import sdTimePicker as objLibSDTimePicker
import sdTimer as objLibSDTimer
import sdTooltip as objLibSDTooltip
import tkinter as objLibTK
from tkinter import font as objLibTkFont
from tkinter import messagebox as objLibTKMessageBox
from tkinter import ttk as objLibTTK

class clCommon:
	def __init__(self, strFile):
		# StrFile should be __file__
		'''
		Structure of self.dictInfo
		self.dictInfo = {
			"Screen": {
				"Height": <value>
				"Width": <value>
			}
			"WorkingDir": <str>
		}
		'''
		self.dictInfo = {}
		self.bFatalError = False
		self.arrError = []

		for x in range(1):
			# Initialise working directory
			strPath = objLibOS.path.abspath(strFile)
			arrPath = objLibOS.path.split(strPath)
			strPath = objLibOSPathJoin(arrPath[0], "")

			if not objLibOS.path.isdir(strPath):
				strMsg = "".join(["Invalid path: ", strPath])
				objLibTKMessageBox.showerror(title="Fatal Error", message=strMsg)
				self.bFatalError = True
				break
			# End of if

			self.strWorkingDir = strPath
			self.dictInfo["WorkingDir"] = strPath

			# Read INI file
			strPath = objLibOSPathJoin(self.strWorkingDir, "Data/sdCommon.ini")
			if not objLibOS.path.isfile(strPath):
				strMsg = "".join(["File not found: ", strPath])
				objLibTKMessageBox.showerror(title="Fatal Error", message=strMsg)
				self.bFatalError = True
				break
			# End of if
			self.objIniParser = objLibSDIniParser.clIniParser(strPath)

			# Update INI
			self.objIniParser.SetItem("Paths", "WorkingDir", self.strWorkingDir)

			# Initialise font information
			self.strFontFamily = self.objIniParser.GetItem("Font", "Family")
			self.iFontSize = int(self.objIniParser.GetItem("Font", "Size"))
			self.strFontWeight = self.objIniParser.GetItem("Font", "Weight")
			self.strFontString = self.objIniParser.GetItem("Font", "strFont")

			# Check environment
			self._CheckEnvironment()
			if len(self.arrError) > 0:
				self.bFatalError = True
			# End of if
		# End of for loop
	# End of __init__()

	def _CheckEnvironment(self):
		self.arrError = []
		tIniEntries = self.objIniParser.GetItem("Environment")
		for tIniEntry in tIniEntries:
			strValue = tIniEntry[1]
			if not objLibOS.path.isfile(strValue):
				self.arrError.append(strValue)
			# End of if
		# End of for loop

		if len(self.arrError) > 0:
			self.arrError.insert(0, "The following are missing:")
		# End of if
	# End of CheckEnvironment()

	def GetError(self):
		return self.arrError
	# End of GetError()

	def GetFontInfo(self, strKey="", strText="", strFamily="", iSize=0, strWeight=""):
		strValue = "Error"

		# Form font object
		if len(strFamily) == 0:
			strFamily = self.strFontFamily
		# End of if
		if iSize == 0:
			iSize = self.iFontSize
		# End of if
		if len(strWeight) == 0:
			strWeight = self.strFontWeight
		# End of if
		objFont = objLibTkFont.Font(family=strFamily, size=iSize, weight=strWeight)

		match strKey:
			case "FontFamily":
				strValue = self.strFontFamily
			# End of case

			case "FontSize":
				strValue = self.iFontSize
			# End of case

			case "FontString":
				strValue = self.strFontString
			# End of case

			case "FontWeight":
				strValue = self.strFontWeight
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

	def GetLibrary(self, strLibrary, **dictParameters):
		'''
		Structure of dictParameters
		dictParameters = {
			"Parameter name": <value>
		}
		'''
		for x in range(1):
			objLibrary = None
			if self.bFatalError:
				break
			# End of Get()

			# Get parameter names for library
			strValue = self.objIniParser.GetItem(strLibrary, "InitParameters")
			arrParameters = strValue.split(",")
			for strParameter in arrParameters:
				if len(strParameter) == 0:
					continue
				# End of if

				# Parameter passed overrides that present in INI file
				if strParameter in dictParameters:
					continue
				# End of if

				# Check for special parameter
				strParameterValue = self.objIniParser.GetItem(strLibrary, strParameter)
				arrParameterValue = strParameterValue.split("|-|")

				if len(arrParameterValue) == 1:
					dictParameters[strParameter] = arrParameterValue[0]
					continue
				# End of if

				# Type cast paramter. Avoid "eval" as it is a security risk.
				dictParameters[strParameter] = objLibAST.literal_eval(arrParameterValue[1])
			# End of for loop

			# Get class name
			strClassName = self.objIniParser.GetItem(strLibrary, "ClassName")

			# Get library object
			strLibraryImport = "".join(["objLibSD", strClassName[2:]])
			objLibraryImport = globals()[strLibraryImport]

			# Initialise library
			objClass = getattr(objLibraryImport, strClassName)
			objLibrary = objClass(**dictParameters)
		# End of for loop

		return objLibrary
	# End of GetLibrary()

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

	def InitialiseScreenInfo(self, objWindow, iDesignedScrW, iDesignedScrH):
		# Screen dimensions
		self.dictInfo["Screen"] = {}
		self.dictInfo["Screen"]["Width"] = objWindow.winfo_screenwidth()
		self.dictInfo["Screen"]["Height"] = objWindow.winfo_screenheight()

		# Screen ratios
		self.fScrRatioW = float(self.dictInfo["Screen"]["Width"] / iDesignedScrW)
		self.fScrRatioH = float(self.dictInfo["Screen"]["Height"] / iDesignedScrH)

		# Set named fonts
		tNamedFonts = objLibTkFont.names()
		for tNamedFont in tNamedFonts:
			objFont = objLibTkFont.nametofont(tNamedFont)
			objFont.config(family=self.strFontFamily, size=self.iFontSize, weight=self.strFontWeight, slant="roman", underline=0, overstrike=0)
		# End of for loop

		objStyle = objLibTTK.Style()
		objStyle.theme_use("clam")
		objStyle.map("TCombobox", selectforeground=[('readonly', '!focus', 'black'), ('readonly', 'focus', 'white')],
					 selectbackground=[('readonly', '!focus', 'white')], fieldbackground=[('readonly', '!focus', 'white'),
					('disabled', '#DCDAD5')], foreground=[('readonly', '!focus', 'black')])
		objWindow.option_add('*TCombobox*Listbox.font', self.strFontString)
	# End of InitialiseScreenInfo()

	def MapToScreenRatioH(self, iH):
		return round(iH * self.fScrRatioH)
	# End of ScrRatioH()

	def MapToScreenRatioW(self, iW):
		return round(iW * self.fScrRatioW)
	# End of ScrRatioW()
# End of class clCommon

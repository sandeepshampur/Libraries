#
# Completed: ??-July-2024
#

import os as objLibOS
import tkinter as objLibTK
from tkinter import font as objLibTkFont
from tkinter import ttk as objLibTTK

class clCommon:
	def __init__(self, iFontSize=10):
		self.iFontSize = iFontSize
		self.dictInfo = {
			"Screen": {
				"Width": 0,
				"Height": 0
			},
			"Font": {}
		}
	# End of __init__()

	def Initialise(self, objWindow, bSetTheme=True):
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

	def GetScreenInfo(self, strKey):
		strValue = "Error"

		if strKey in self.dictInfo["Screen"]:
			strValue = self.dictInfo["Screen"][strKey]
		# End of if

		return strValue
	# End of ScreenInfo()

	def GetWorkingDir(self, strPath):
		strPath = objLibOS.path.abspath(strPath)
		arrPath = objLibOS.path.split(strPath)
		strPath = objLibOS.path.join(arrPath[0], "")

		return strPath
	# End of GetWorkingDir()

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

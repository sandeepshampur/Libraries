#
# Started	: 12-Sep-2024
# Completed	: 12-Sep-2024
#

from os.path import join as objLibPathJoin
import tkinter as objLibTK

class clTime:
	def __init__(self, dictDefault, dictImage, arrFont, dictColours, objCommon):
		'''
		Structure of dictDefault
		dictDefault = {
			"Hour": 0,
			"Minute": 0,
			"Period": "AM"
		}
		'''
		self.dictDefaultTime = dictDefault
		self.dictImage = dictImage
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon

		# Class
		dictParams = { "objCommon": self.objCommon }
		self.objTimePicker = self.objCommon.GetLibrary("sdTimePicker", **dictParams)

		self.strCurrentPeriod = dictDefault["Period"]
		self.dictWidgets = {}
		'''
		Structure of self.dictWidgets
		self.dictWidgets = {
			"Buttons": {
				"AM"|"PM": None
			}
			"Image": None
			"Texts": {
				"Hour": None
				"Minute": None
			}
		}
		'''
	# End of __init__()

	def Display(self, objParentWindow, objParentFrame, iX, iY, strHeader="Time", dictTime={}, bAllowPastTime=True):
		'''
		Structure of dictTime is same as dictDefaultTime
		'''
		self.objParentWindow = objParentWindow
		if len(dictTime) == 0:
			self.dictTime = self.dictDefaultTime
		else:
			self.dictTime = dictTime
		# End of if
		self.strCurrentPeriod = self.dictTime["Period"]
		self.bAllowPastTime = bAllowPastTime

		# Initialise
		iPad = 10
		iHalfPad = int(iPad / 2)
		ilbH = self.objCommon.GetFontInfo("TextHeight") + iHalfPad

		# Frame
		objFrame = objLibTK.LabelFrame(objParentFrame, text=strHeader)

		# Hour
		ilbX = iPad
		itxtW = self.objCommon.GetFontInfo("TextWidth", "888")
		self.dictWidgets["Texts"] = {}

		dictParams = { "strValue": self.dictTime["Hour"], "maxChars": 2, "charsAllowed": "\d+", "emptyAllowed": "no", "iMin": 0,
					   "iMax": 12, "objCommon": self.objCommon }
		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objFrame, ilbX, iPad, itxtW, ilbH, "center")
		self.dictWidgets["Texts"]["Hour"] = objWidget

		# Separator
		ilbX += itxtW + iHalfPad
		iSepW = self.objCommon.GetFontInfo("TextWidth", "::")
		objWidget = objLibTK.Label(master=objFrame, text=":", anchor="center")
		objWidget.place(x=ilbX, y=iPad, width=iSepW, height=ilbH)

		# Minute
		ilbX += iSepW + iHalfPad
		dictParams["strValue"] = self.dictTime["Minute"]
		dictParams["iMax"] = 59
		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objFrame, ilbX, iPad, itxtW, ilbH, "center")
		self.dictWidgets["Texts"]["Minute"] = objWidget

		# AM
		ilbX += itxtW + iPad
		ibtnW = self.objCommon.GetFontInfo("TextWidth", "PM") + iPad
		self.dictWidgets["Buttons"] = {}

		objWidget = objLibTK.Button(objFrame, text="AM", command=lambda: self._ToggleAMPM("AM"))
		objWidget.place(x=ilbX, y=iPad, width=ibtnW, height=ilbH)
		self.dictWidgets["Buttons"]["AM"] = objWidget
		if self.dictTime["Period"].find("AM") == 0:
			objWidget.config(relief="sunken")
		# End of if

		# PM
		ilbX += ibtnW + iHalfPad
		objWidget = objLibTK.Button(objFrame, text="PM", command=lambda: self._ToggleAMPM("PM"))
		objWidget.place(x=ilbX, y=iPad, width=ibtnW, height=ilbH)
		self.dictWidgets["Buttons"]["PM"] = objWidget
		if self.dictTime["Period"].find("PM") == 0:
			objWidget.config(relief="sunken")
		# End of if

		# Pick button
		ilbX += ibtnW + iHalfPad
		ibtnW = self.objCommon.GetFontInfo("TextWidth", "WWWW") + iHalfPad
		iImgH = ilbH - iHalfPad
		objDateImage = self.GetImage(-1, iImgH)

		objWidget = objLibTK.Button(objFrame, text="Pick", command=self._HandlerbtnTimePicker, image=objDateImage, compound="right", padx=5, anchor="w")
		objWidget.place(x=ilbX, y=iPad, width=ibtnW, height=ilbH)

		# Frame
		ifrTimeW = ilbX + ibtnW + iPad
		ifrTimeH = ilbH + (iPad * 4)
		objFrame.place(x=iX, y=iY, width=ifrTimeW, height=ifrTimeH)

		return [ifrTimeW, ifrTimeH]
	# End of Display()

	def Exit(self):
		self.strCurrentPeriod = dictDefault["Period"]
		self.dictWidgets.clear()
	# End of Exit()

	def GetImage(self, iImgW, iImgH):
		for x in range(1):
			if "Image" in self.dictWidgets:
				objImage = self.dictWidgets["Image"]
				break
			# End of if

			# Create image
			dictParams = { "objCommon": self.objCommon }
			objCanvas = self.objCommon.GetLibrary("sdCanvas", **dictParams)

			strImgPath = objLibPathJoin(self.dictImage["Path"], self.dictImage["File"])
			objCanvas.CreateImage(strImgPath, iImgW, iImgH)
			dictDim = objCanvas.GetDimensions()

			self.dictWidgets["Image"] = dictDim["Image"]
			objImage = dictDim["Image"]
		# End of for loop

		return objImage
	# End of GetImage()

	def GetTime(self):
		for x in range(1):
			strTime = ""

			arrError = self.Validate()
			if len(arrError) > 0:
				break
			# End of if

			iHour = self.dictWidgets["Texts"]["Hour"].GetValue()
			strHour = str(f'{iHour:02}')

			iMinute = self.dictWidgets["Texts"]["Minute"].GetValue()
			strMinute = str(f'{iMinute:02}')

			strTime = "".join([strHour, ":", strMinute, " ", self.strCurrentPeriod])
		# End of for loop

		return strTime
	# End of GetTime()

	def Reset(self):
		iHour = self.dictDefaultTime["Hour"]
		self.dictWidgets["Texts"]["Hour"].SetValue(iHour)

		iMinute = self.dictDefaultTime["Minute"]
		self.dictWidgets["Texts"]["Minute"].SetValue(iHour)

		strPeriod = self.dictDefaultTime["Period"]
		self._ToggleAMPM(strPeriod)
	# End of _Reset()

	def Validate(self):
		arrError = []

		iStatus = self.dictDefaultTime["Hour"].GetStatus()
		if iStatus != 0:
			arrError.append("    - Hour is not valid")
		# End of if

		iStatus = self.dictDefaultTime["Minute"].GetStatus()
		if iStatus != 0:
			arrError.append("    - Minute is not valid")
		# End of if

		return arrError
	# End of Validate()

	def _HandlerbtnTimePicker(self):
		strPickedTime = self.objTimePicker.Show(self.objParentWindow, -1, -1, self.bAllowPastTime)
		if len(strPickedTime) > 0:
			iHour = int(strPickedTime[:2])
			self.dictWidgets["Texts"]["Hour"].SetValue(iHour)

			iHour = int(strPickedTime[3:5])
			self.dictWidgets["Texts"]["Minute"].SetValue(iHour)

			strPeriod = strPickedTime[6:]
			self._ToggleAMPM(strPeriod)
		# End of if
		print(strPickedTime)
	# End of _CallbackTimePicker()

	def _ToggleAMPM(self, strPeriod):
		for x in range(1):
			# Ignore if toggle is already done
			if self.strCurrentPeriod.find(strPeriod) == 0:
				break
			# End of if

			if strPeriod.find("AM") == 0:
				objWidget = self.dictWidgets["Buttons"]["AM"]
				objWidget.config(relief="sunken")
				objWidget = self.dictWidgets["Buttons"]["PM"]
				objWidget.config(relief="raised")
				self.strCurrentPeriod = "AM"
			else:
				objWidget = self.dictWidgets["Buttons"]["PM"]
				objWidget.config(relief="sunken")
				objWidget = self.dictWidgets["Buttons"]["AM"]
				objWidget.config(relief="raised")
				self.strCurrentPeriod = "PM"
			# End of if
		# End of for loop
	# End of _ToggleAMPM()
# End of class clTime

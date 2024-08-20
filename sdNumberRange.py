#
# Completed : 20-August--2024
#

import tkinter as objLibTK
from tkinter import font as objLibTkFont
from tkinter import ttk as objLibTTK

class clNumberRange:
	def __init__(self, dictDefault, objCommon, arrFont, dictColours):
		'''
		Structure of dictDefault
		dictDefault = {
			"ComboboxSelection": 0,
			"LeftEditBox": {
				"iMin": 0,
				"iMax": 99999,
				"maxChars": 5,
				"Value": 0
			},
			"RightEditBox": {
				"iMin": 0,
				"iMax": 99999,
				"maxChars": 5,
				"Value": 0
			}
		}
		'''
		self.dictDefault = dictDefault
		self.objCommon = objCommon
		self.arrFont = arrFont
		self.dictColours = dictColours

		self.ComboOptions = ["=", "!=", ">", ">=", "<", "<=", "<>"]
		self.iPad = 10
		self.iHalfPad = int(self.iPad / 2)
	# End of __init__()

	def Display(self, objWindow, strHeading, iX, iY, dictValues={}):
		'''
		Structure of dictValues
		dictValues = {
			"ComboboxSelection": 0,
			"LeftEditBoxValue": 0,
			"RightEditBoxValue": 0
		}
		'''

		# Initialise
		if len(dictValues) == 0:
			dictValues["ComboboxSelection"] = self.dictDefault["ComboboxSelection"]
			dictValues["LeftEditBoxValue"] = self.dictDefault["LeftEditBox"]["Value"]
			dictValues["RightEditBoxValue"] = self.dictDefault["RightEditBox"]["Value"]
		# End of if
		iComboW = self.objCommon.GetFontInfo("TextWidth", "WWW")
		iComboH = self.objCommon.GetFontInfo("TextHeight") + self.iHalfPad

		# Frame
		objFrame = objLibTK.LabelFrame(objWindow, text=strHeading)

		# Combobox ----------------------------------------------------------------------------------------------------------------------

		self.cbComboBox = objLibTTK.Combobox(master=objFrame, state="readonly", values=self.ComboOptions)
		self.cbComboBox.place(x=self.iPad, y=self.iPad, width=iComboW, height=iComboH)
		self.cbComboBox.current(dictValues["ComboboxSelection"])
		self.cbComboBox.bind("<<ComboboxSelected>>", self._HandlerCombobox)

		# Left Entry Widget --------------------------------------------------------------------------------------------------------------
		iEntryX = iComboW + (self.iPad * 2)
		iMaxChars = self.dictDefault["LeftEditBox"]["maxChars"]
		if iMaxChars < self.dictDefault["RightEditBox"]["maxChars"]:
			iMaxChars = self.dictDefault["RightEditBox"]["maxChars"]
		# End of if
		strChars = "".join("8" * (iMaxChars+1))
		iEntryW = self.objCommon.GetFontInfo("TextWidth", strChars)

		dictParams = { "strValue": dictValues["LeftEditBoxValue"], "maxChars": self.dictDefault["LeftEditBox"]["maxChars"], "charsAllowed": "\d+", "emptyAllowed": "no",
					   "callback": self._HandlerEntryWidget, "callbackargs": ("Left", ), "iMin": self.dictDefault["LeftEditBox"]["iMin"],
					   "iMax": self.dictDefault["LeftEditBox"]["iMax"], "objCommon": self.objCommon }
		self.objLeftEntry = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		self.objLeftEntry.Display(objFrame, iX=iEntryX, iY=self.iPad, iW=iEntryW, iH=iComboH, justify="center")

		# Right Entry Widget --------------------------------------------------------------------------------------------------------------
		iEntryX += iEntryW + self.iPad


		dictParams = { "strValue": dictValues["RightEditBoxValue"], "maxChars": self.dictDefault["RightEditBox"]["maxChars"], "charsAllowed": "\d+", "emptyAllowed": "no",
					   "callback": self._HandlerEntryWidget, "callbackargs": ("Right", ), "iMin": self.dictDefault["RightEditBox"]["iMin"],
					   "iMax": self.dictDefault["RightEditBox"]["iMax"], "objCommon": self.objCommon }
		self.objRightEntry = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		self.objRightEntry.Display(objFrame, iX=iEntryX, iY=self.iPad, iW=iEntryW, iH=iComboH, justify="center")

		# Set state for right entry widget
		if dictValues["ComboboxSelection"] != 6:
			self.objRightEntry.SetValueDisabled("")
		# End of if

		iWidth = iEntryX + iEntryW + self.iPad
		iHeight = iComboH + (self.iPad * 4)
		objFrame.place(x=iX, y=iY, width=iWidth, height=iHeight)

		return [iWidth, iHeight]
	# End of Show()

	def GetValues(self):
		# arrValues = [">", 1, 1] or [">", "", ""]
		arrValues = []

		arrValues.append(self.cbComboBox.get())
		arrValues.append(self.objLeftEntry.GetValue())
		arrValues.append(self.objRightEntry.GetValue())

		return arrValues
	# End of GetValues()

	def IsInRange(self, iValue):
		bFlag = False

		for x in range(1):
			strCombobox = self.cbComboBox.get()
			match strCombobox:
				case "=":
					iEntry = int(self.objLeftEntry.GetValue() or 0)
					if iValue == iEntry:
						bFlag = True
					# End of if
				# End of case

				case "!=":
					iEntry = int(self.objLeftEntry.GetValue() or 0)
					if iValue != iEntry:
						bFlag = True
					# End of if
				# End of case

				case ">":
					iEntry = int(self.objLeftEntry.GetValue() or 0)
					if iValue > iEntry:
						bFlag = True
					# End of if
				# End of case

				case ">=":
					iEntry = int(self.objLeftEntry.GetValue() or 0)
					if iValue >= iEntry:
						bFlag = True
					# End of if
				# End of case

				case "<":
					iEntry = int(self.objLeftEntry.GetValue() or 0)
					if iValue < iEntry:
						bFlag = True
					# End of if
				# End of case

				case "<=":
					iEntry = int(self.objLeftEntry.GetValue() or 0)
					if iValue <= iEntry:
						bFlag = True
					# End of if
				# End of case

				case "<>":
					iLeftEntry = int(self.objLeftEntry.GetValue() or 0)
					iRightEntry = int(self.objRightEntry.GetValue() or 0)
					if (iValue >= iLeftEntry) or (iValue <= iRightEntry):
						bFlag = True
					# End of if
				# End of case
			# End of match
		# End of for loop

		return bFlag
	# End of IsInRange()

	def Reset(self):
		self.cbComboBox.current(self.dictDefault["ComboboxSelection"])
		self._HandlerCombobox()
	# End of Reset()

	def Validate(self):
		bValid = True

		return bValid
	# End of Validate()

	def _HandlerCombobox(self, objEvent=None):
		strSelection = self.cbComboBox.get()
		iIndex = self.ComboOptions.index(strSelection)

		self.objLeftEntry.Reset()
		self.objRightEntry.Reset()

		# Set state for right entry widget
		if iIndex == 6:
			# "<>" has been selected
			self.objRightEntry.SetState("normal")
			self.objRightEntry.SetValue(self.dictDefault["RightEditBox"]["iMin"])
		else:
			self.objRightEntry.SetValueDisabled("")
		# End of if

		self.objLeftEntry.SetValue(self.dictDefault["LeftEditBox"]["iMin"])
	# End of _HandlerCombobox()

	def _HandlerEntryWidget(self, iValue, strWhich):
		for x in range(1):
			# Ignore if right widget is disabled
			strState = self.objRightEntry.GetState()
			if strState.find("disabled") == 0:
				break
			# End of if

			# Get values
			iLeftValue = int(self.objLeftEntry.GetValue() or 0)
			iRightValue = int(self.objRightEntry.GetValue() or 0)

			match strWhich:
				case "Left":
					if iLeftValue <= iRightValue:
						self.objLeftEntry.SetStatus()
						self.objRightEntry.SetStatus()
						break
					# End of if

					# Flag error
					self.objLeftEntry.SetStatus(-1, "Fatal", "Value should be less than right side value")
					self.objRightEntry.SetStatus()
				# End of case

				case "Right":
					if iLeftValue <= iRightValue:
						self.objLeftEntry.SetStatus()
						self.objRightEntry.SetStatus()
						break
					# End of if

					# Flag error
					self.objLeftEntry.SetStatus()
					self.objRightEntry.SetStatus(-1, "Fatal", "Value should be greater than left side value")
				# End of case
			# End of match
		# End of for loop
	# End of _HandlerEntryWidget()
# End of class clNumberRange

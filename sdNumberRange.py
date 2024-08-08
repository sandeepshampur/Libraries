#
# Created:	 08-August--2024
#

import sdEntryWidget as objLibEntry
import tkinter as objLibTK
from tkinter import font as objLibTkFont
from tkinter import ttk as objLibTTK

class clNumberRange:
	def __init__(self, dictDefault, font="Arial 11 normal", dictColours={}):
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
		self.strFont = font
		self.dictColours = dictColours

		self.arrFont = font.split(" ")
		self.ComboOptions = ["=", "!=", ">", ">=", "<", "<=", "<>"]
		self.iPad = 10

		# Calculate size of widget
		self.objFont = objLibTkFont.Font(family=self.arrFont[0], size=self.arrFont[1], weight=self.arrFont[2])
		self.iComboW = self.objFont.measure("WWW")
		self.iComboH = self.objFont.metrics("linespace") + 5

		iChars = dictDefault["LeftEditBox"]["maxChars"]
		if iChars < dictDefault["RightEditBox"]["maxChars"]:
			iChars = dictDefault["RightEditBox"]["maxChars"]
		# End of if
		iChars += 1
		strChars = "".join("8" * iChars)
		self.iEntryW = self.objFont.measure(strChars)

		iWidgetW = self.iComboW + (self.iEntryW * 2) + (self.iPad * 4)
		iWidgetH = self.iComboH + (self.iPad * 4)

		self.dictDim = [iWidgetW, iWidgetH]
	# End of __init__()

	def Display(self, objWindow, strHeading, iX, iY, dictValues, iW=-1, iH=-1):
		'''
		Structure of dictValues
		dictValues = {
			"ComboboxSelection": 0,
			"LeftEditBoxValue": 0,
			"RightEditBoxValue": 0
		}
		'''

		objFrame = objLibTK.LabelFrame(objWindow, text=strHeading, font=self.strFont)

		# Combobox ----------------------------------------------------------------------------------------------------------------------

		self.cbComboBox = objLibTTK.Combobox(master=objFrame, state="readonly", values=self.ComboOptions, font=self.strFont)
		self.cbComboBox.place(x=self.iPad, y=self.iPad, width=self.iComboW, height=self.iComboH)
		self.cbComboBox.current(dictValues["ComboboxSelection"])
		self.cbComboBox.bind("<<ComboboxSelected>>", self.HandlerCombobox)

		# Change font of dropdown. Note: This will affect font of listbox. Refer to link for better solution
		# https://stackoverflow.com/questions/43086378/how-to-modify-ttk-combobox-fonts
		objWindow.option_add('*TCombobox*Listbox.font', self.strFont)

		# Left Entry Widget --------------------------------------------------------------------------------------------------------------
		iEntryX = self.iComboW + (self.iPad * 2)
		strChars = "".join("8" * (self.dictDefault["LeftEditBox"]["maxChars"]+1))
		self.objLeftEntry = objLibEntry.clEntryWidget(value=dictValues["LeftEditBoxValue"], state="normal", font=self.strFont,
													  maxChars=self.dictDefault["LeftEditBox"]["maxChars"], charsAllowed="\d+", emptyAllowed="no",
													  callback=self.HandlerEntryWidget, callbackargs=("Left",),
													  iMin=self.dictDefault["LeftEditBox"]["iMin"], iMax=self.dictDefault["LeftEditBox"]["iMax"])
		self.objLeftEntry.Display(objFrame, x=iEntryX, y=self.iPad, w=self.iEntryW, h=self.iComboH, justify="center")

		# Right Entry Widget --------------------------------------------------------------------------------------------------------------
		iEntryX += self.iEntryW + self.iPad
		self.objRightEntry = objLibEntry.clEntryWidget(value=dictValues["RightEditBoxValue"], state="normal", font=self.strFont,
													  maxChars=self.dictDefault["RightEditBox"]["maxChars"], charsAllowed="\d+", emptyAllowed="no",
													   callback=self.HandlerEntryWidget, callbackargs=("Right",),
													  iMin=self.dictDefault["RightEditBox"]["iMin"], iMax=self.dictDefault["RightEditBox"]["iMax"])
		self.objRightEntry.Display(objFrame, x=iEntryX, y=self.iPad, w=self.iEntryW, h=self.iComboH, justify="center")

		# Set state for right entry widget
		if dictValues["ComboboxSelection"] != 6:
			self.objRightEntry.SetValue("")
			self.objRightEntry.SetState("disabled")
		# End of if

		iWidth = self.dictDim[0] if self.dictDim[0] >= iW else iW
		iHeight = self.dictDim[1] if self.dictDim[1] >= iH else iH
		objFrame.place(x=iX, y=iY, width=iWidth, height=iHeight)

		return self.dictDim
	# End of Show()

	def HandlerCombobox(self, objEvent=None):
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
	# End of HandlerCombobox()

	def HandlerEntryWidget(self, iValue, strWhich):
		for x in range(1):
			# Ignore if right widget is disabled
			strState = self.objRightEntry.GetState()
			if strState.find("disabled") == 0:
				break
			# End of if

			# Get values
			iLeftValue = int(self.objLeftEntry.GetValue() or 0)
			iRightValue = int(self.objRightEntry.GetValue() or 0)
			print("User handler ->", iLeftValue, iRightValue)

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
					print("User handler -> Left error")
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
					print("User handler -> Right error")
				# End of case
			# End of match
		# End of for loop
	# End of HandlerEntryWidget()

	def GetSize(self):
		return self.dictDim
	# End of GetSize()

	def Reset(self):
		self.cbComboBox.current(self.dictDefault["ComboboxSelection"])
		self.HandlerCombobox()
	# End of Reset()
# End of class clNumberRange

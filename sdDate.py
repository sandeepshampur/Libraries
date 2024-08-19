#!/usr/bin/env python3

#
#	Completed : 19-August-2024
#

import datetime as objLibDateTime
from dateutil.relativedelta import relativedelta as objLibRelativeDelta
import tkinter as objLibTK
from tkinter import font as objLibTkFont
from tkinter import ttk as objLibTTK

class clDate:
	def __init__(self, iComponents, dictDefault, arrFont, dictColours, objCommon, objWindow):
		'''
		Meaning of iComponents
			1: Shows only date row
			2: Shows only date range
			3: Shows only filters
			4: Shows date row with filters
			5: Shows date range with filters

		Structure of dictDefault
		dictDefault = {
			"EndDate": {
				"Day": 1,
				"Month": 0, # 0 = Jan
				"Year": 2024
			},
			"Filters": {
				"Day": [False, 0], # True = checked; date value
				"Month": [False, 0], # True = checked; month value (0 = Jan)
				"Year": [False, 0] # # True = checked; year value
			},
			"StartDate": {
				"Day": 1,
				"Month": 0, # 0 = Jan
				"Year": 2024
			}
		}
		'''
		self.iComponents = iComponents
		self.dictDefault = dictDefault
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon
		self.objWindow = objWindow

		self.iPad = 10
		self.iHalfPad = int(self.iPad / 2)
		self.arrMonth = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

		self.ilbH = self.objCommon.GetFontInfo("TextHeight") + self.iHalfPad

		# Classes
		dictParams = { "objCommon": self.objCommon }
		self.objCanvasGeneral = self.objCommon.GetLibrary("sdCanvas", **dictParams)

		dictParams = { "objCommon": self.objCommon }
		self.objMessageBox = self.objCommon.GetLibrary("sdMessageBox", **dictParams)
		self.objMessageBox.SetParentWindow(objWindow)

		self.dictWidgets = {"Images": []}
		'''
		Structure of self.dictWidgets
		self.dictWidgets = {
			"AddSubtract": {
				"Days": <objWidget>,
				"Months": <objWidget>,
				"Years": <objWidget>,
				"Combobox": <objWidget>,
				"Text": <objWidget>
			},
			"EndDate"|"StartDate": {
				"Day": <objWidget>,
				"Month": <objWidget>,
				"Year": <objWidget>
				"DatePicker": <objWidget>
			},
			"Filters": {
				"Checkboxes": {
					"Day": <objWidget>,
					"Month": <objWidget>,
					"Year": <objWidget>
				},
				"Fields": {
					"Day": <objWidget>,
					"Month": <objWidget>,
					"Year": <objWidget>
				}
			},
			"Images": [],
		}
		'''
	# End of __init__()

	def Display(self, objFrame, strHeading, iX, iY, dictValues={}):
		# Structure of dictValues is same as dictDefault
		self.dictValues = self.dictDefault if len(dictValues) == 0 else dictValues

		objDateFrame = objLibTK.LabelFrame(objFrame, text=strHeading)

		match self.iComponents:
			case 1:
				# Show only date row
				iWidth = self._CreateDateRow(objDateFrame, "StartDate", self.iPad, self.iPad)
				iWidth += self.iPad
				iHeight = self.ilbH + (self.iPad * 4)
			# End of case

			case 2:
				# Show only date range
				arrDim = self._CreateDateRange(objDateFrame, self.iPad, self.iPad)
				iWidth = arrDim[0] + (self.iPad * 2)
				iHeight = arrDim[1] + (self.iPad * 4)
			# End of case

			case 3:
				# Show only filters
				arrDim = self._CreateFilters(objDateFrame, self.iPad, self.iPad)
				iWidth = arrDim[0] + (self.iPad * 2)
				iHeight = arrDim[1] + (self.iPad * 4)
			# End of case

			case 4:
				# Show date row with filters
				iDateRowW = self._CreateDateRow(objDateFrame, "StartDate", self.iPad, self.iPad)

				iFilterY = self.ilbH + (self.iPad * 2)
				arrDim = self._CreateFilters(objDateFrame, self.iPad, iFilterY)

				iWidth = arrDim[0] if arrDim[0] >= iDateRowW else iDateRowW
				iHeight = iFilterY + arrDim[1]

				iWidth += (self.iPad * 2)
				iHeight += (self.iPad * 3)
			# End of case

			case 5:
				# Show date range with filters
				arrDimDateRange = self._CreateDateRange(objDateFrame, self.iPad, self.iPad)

				iFilterY = arrDimDateRange[1] + (self.iPad * 2)
				arrDimFilter = self._CreateFilters(objDateFrame, self.iPad, iFilterY)

				iWidth = arrDimDateRange[0] if arrDimDateRange[0] >= arrDimFilter[0] else arrDimFilter[0]
				iHeight = arrDimDateRange[1] + arrDimFilter[1]

				iWidth += (self.iPad * 2)
				iHeight += (self.iPad * 5)
			# End of case
		# End of match

		# Date frame
		objDateFrame.place(x=iX, y=iY, width=iWidth, height=iHeight)

		return [iWidth, iHeight]
	# End of Display()

	def GetDate(self, strWhich="StartDate"):
		# strWhich = "StartDate"|"EndDate"
		# arrDate = [1, "Jan", 2024]
		arrDate = []

		objWidget = self.dictWidgets[strWhich]["Day"]
		arrDate.append(objWidget.GetValue())
		objWidget = self.dictWidgets[strWhich]["Month"]
		arrDate.append(objWidget.get())
		objWidget = self.dictWidgets[strWhich]["Year"]
		arrDate.append(objWidget.GetValue())

		return arrDate
	# End of GetDate()

	def GetFilterValues(self):
		# arrFilterValue = [1, "Jan", 2024] or ["", "", ""] if not selected
		arrFilterValue = []

		objWidget = self.dictWidgets["Filters"]["Fields"]["Day"]
		arrFilterValue.append(objWidget.GetValue())

		objWidget = self.dictWidgets["Filters"]["Checkboxes"]["Month"]
		if objWidget.GetState():
			objWidget = self.dictWidgets["Filters"]["Fields"]["Month"]
			arrFilterValue.append(objWidget.get())
		else:
			arrFilterValue.append("")
		# End of if

		objWidget = self.dictWidgets["Filters"]["Fields"]["Year"]
		arrFilterValue.append(objWidget.GetValue())

		return arrFilterValue
	# End of GetFilterValues()

	def Reset(self):
		if "StartDate" in self.dictWidgets:
			objWidget = self.dictWidgets["StartDate"]["Day"]
			objWidget.Reset()
			objWidget.SetValue(self.dictDefault["StartDate"]["Day"])

			objWidget = self.dictWidgets["StartDate"]["Month"]
			objWidget.current(self.dictDefault["StartDate"]["Month"])

			objWidget = self.dictWidgets["StartDate"]["Year"]
			objWidget.Reset()
			objWidget.SetValue(self.dictDefault["StartDate"]["Year"])
		# End of if

		if "EndDate" in self.dictWidgets:
			objWidget = self.dictWidgets["EndDate"]["Day"]
			objWidget.Reset()
			objWidget.SetValue(self.dictDefault["EndDate"]["Day"])

			objWidget = self.dictWidgets["EndDate"]["Month"]
			objWidget.current(self.dictDefault["EndDate"]["Month"])

			objWidget = self.dictWidgets["EndDate"]["Year"]
			objWidget.Reset()
			objWidget.SetValue(self.dictDefault["EndDate"]["Year"])
		# End of if

		if "AddSubtract" in self.dictWidgets:
			objWidget = self.dictWidgets["AddSubtract"]["Days"]
			objWidget.Reset()
			objWidget.SetValue(0)

			objWidget = self.dictWidgets["AddSubtract"]["Months"]
			objWidget.Reset()
			objWidget.SetValue(0)

			objWidget = self.dictWidgets["AddSubtract"]["Years"]
			objWidget.Reset()
			objWidget.SetValue(0)

			objWidget = self.dictWidgets["AddSubtract"]["Combobox"]
			objWidget.current(0)

			dtDate = self._GetDate("StartDate")
			strDate = dtDate,strftime("%d-%b-%Y")
			objWidget = self.dictWidgets["AddSubtract"]["Text"]
			objWidget.SetValue(strDate)
		# End of if

		if "Filters" in self.dictWidgets:
			objWidget = self.dictWidgets["Filters"]["Checkboxes"]["Day"]
			objWidget.SetState(False)
			objWidget = self.dictWidgets["Filters"]["Fields"]["Day"]
			objWidget.Reset()
			objWidget.SetValueDisabled("")

			objWidget = self.dictWidgets["Filters"]["Checkboxes"]["Month"]
			objWidget.SetState(False)
			objWidget = self.dictWidgets["Filters"]["Fields"]["Month"]
			objWidget["state"] = "readonly"
			objWidget.current(0)
			objWidget["state"] = "disabled"

			objWidget = self.dictWidgets["Filters"]["Checkboxes"]["Year"]
			objWidget.SetState(False)
			objWidget = self.dictWidgets["Filters"]["Fields"]["Year"]
			objWidget.Reset()
			objWidget.SetValueDisabled("")
		# End of if
	# End of Reset()

	def Validate(self):
		iValidity = 0
		# Significance of iValidity bits
		# 0 : Valid
		# 1 : Date error (fist bit)
		# 2 : Filter error (second bit)
		# 4 : Error with date range - start date is greater than end date (third bit)
		# 8 : Filter is out of date / date range

		match self.iComponents:
			case 1:
				# Date row only
				dtDate = self._GetDate("StartDate")
				if dtDate is None:
					iValidity = 1
				# End of if
			# End of case

			case 2:
				# Date range only
				dtStartDate = self._GetDate("StartDate")
				if dtStartDate is None:
					iValidity = 1
				# End of if
				dtEndDate = self._GetDate("EndDate")
				if dtEndDate is None:
					iValidity = 1
				# End of if

				if (dtStartDate is not None) and (dtEndDate is not None):
					if dtStartDate > dtEndDate:
						iValidity |= 4
					# End of if
				# End of if
			# End of case

			case 3:
				# Filter only
				bValid = self._ValidateFilter()
				if not bValid:
					iValidity = 8
				# End of if
			# End of case

			case 4:
				# Date row with filter
				dtDate = self._GetDate("StartDate")
				if dtDate is None:
					iValidity = 1
				# End of if
				bValid = self._ValidateFilter(dtDate)
				if not bValid:
					iValidity |= 8
				# End of if
			# End of case

			case 5:
				# Date range with filter
				dtStartDate = self._GetDate("StartDate")
				if dtStartDate is None:
					iValidity = 1
				# End of if
				dtEndDate = self._GetDate("EndDate")
				if dtEndDate is None:
					iValidity = 1
				# End of if

				if (dtStartDate is not None) and (dtEndDate is not None):
					if dtStartDate > dtEndDate:
						iValidity |= 4
					# End of if
				# End of if

				bValid = self._ValidateFilter(dtStartDate, dtEndDate)
				if not bValid:
					iValidity |= 8
				# End of if
			# End of case
		# End of match

		return iValidity
	# End of Validate()

	def _CreateDateRow(self, objFrame, strKey, iX, iY):
		self.dictWidgets[strKey] = {}

		# Date
		iDateW = self.objCommon.GetFontInfo("TextWidth", "888")
		dictParams = { "strValue": self.dictValues[strKey]["Day"], "maxChars": 2, "charsAllowed": "\d+", "emptyAllowed": "no",
					   "callback": self._HandlerEntryWidget, "callbackargs": (strKey, "Day",), "iMin": 1, "iMax": 31, "objCommon": self.objCommon }

		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objFrame, iX=iX, iY=iY, iW=iDateW, iH=self.ilbH, justify="center")
		self.dictWidgets[strKey]["Day"] = objWidget

		# Month
		iX += iDateW + self.iPad
		iMonthW = self.objCommon.GetFontInfo("TextWidth", "WWWW")
		objWidget = objLibTTK.Combobox(master=objFrame, state="readonly", values=self.arrMonth)
		objWidget.place(x=iX, y=iY, width=iMonthW, height=self.ilbH)
		objWidget.current(self.dictValues[strKey]["Month"])
		objWidget.bind("<<ComboboxSelected>>", lambda _, strKey=strKey: self._HandlerCombobox(strKey))
		self.dictWidgets[strKey]["Month"] = objWidget

		# Year
		iX += iMonthW + self.iPad
		iYearW = self.objCommon.GetFontInfo("TextWidth", "88888")

		dictParams = { "strValue": self.dictValues[strKey]["Year"], "maxChars": 4, "charsAllowed": "\d+", "emptyAllowed": "no",
					   "callback": self._HandlerEntryWidget, "callbackargs": (strKey, "Year",), "iMin": 1973, "objCommon": self.objCommon }
		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objFrame, iX=iX, iY=iY, iW=iYearW, iH=self.ilbH, justify="center")
		self.dictWidgets[strKey]["Year"] = objWidget

		# Button
		ibtnX = iX + iYearW + self.iPad
		ibtnW = self.objCommon.GetFontInfo("TextWidth", "WWWW") + self.iHalfPad
		iImgH = self.ilbH - self.iHalfPad

		dictParams = { "objCommon": self.objCommon }
		objDatePicker = self.objCommon.GetLibrary("sdDatePicker", **dictParams)
		objDateImage = objDatePicker.GetImage(-1, iImgH)
		self.dictWidgets[strKey]["DatePicker"] = objDatePicker

		objWidget = objLibTK.Button(objFrame, text="Pick", command=lambda: self._HandlerDatePicker(strKey), image=objDateImage,
									compound="right", padx=5, anchor="w")
		objWidget.place(x=ibtnX, y=iY, width=ibtnW, height=self.ilbH)

		iWidth = ibtnX + ibtnW
		return iWidth
	# End of _CreateDateRow()

	def _CreateDateRange(self, objFrame, iX, iY):
		objRangeFrame = objLibTK.LabelFrame(objFrame, text="Range")

		# First row -------------------------------------------------------------------------------------------------------------
		iWidgetY = self.iPad
		self._CreateDateRow(objRangeFrame, "StartDate", iX, iWidgetY)

		# Second row ------------------------------------------------------------------------------------------------------------
		iWidgetY += self.ilbH + self.iPad
		self._CreateDateRow(objRangeFrame, "EndDate", iX, iWidgetY)

		# Adder / subtractor -----------------------------------------------------------------------------------------------------
		self.dictWidgets["AddSubtract"] = {}
		iWidgetX = iX
		iWidgetY += self.ilbH + self.iPad
		iWidgetW = self.objCommon.GetFontInfo("TextWidth", "88888")

		# Header
		dictInfo = {
			"Labels": ["D", "M", "Y"],
			"Key": ["Days", "Months", "Years"]
		}
		for iIndex in range(len(dictInfo["Labels"])):
			strKey = dictInfo["Key"][iIndex]

			iWidgetASY = iWidgetY
			objWidget = objLibTK.Label(master=objRangeFrame, text=dictInfo["Labels"][iIndex], anchor="center")
			objWidget.place(x=iWidgetX, y=iWidgetASY, width=iWidgetW, height=self.ilbH)

			iWidgetASY += self.ilbH
			dictParams = { "strValue": 0, "maxChars": 4, "charsAllowed": "\d+", "emptyAllowed": "no", "callback": self._HandlerEntryWidget,
						   "callbackargs": ("AddSubtract", strKey,), "iMin": 0, "objCommon": self.objCommon }
			objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
			objWidget.Display(objRangeFrame, iX=iWidgetX, iY=iWidgetASY, iW=iWidgetW, iH=self.ilbH, justify="center")
			self.dictWidgets["AddSubtract"][strKey] = objWidget

			iWidgetX += iWidgetW + self.iPad
		# End of for loop

		# Combobox
		iWidgetW = self.objCommon.GetFontInfo("TextWidth", "WWWW")
		objWidget = objLibTTK.Combobox(master=objRangeFrame, state="readonly", values=("Add", "Sub",))
		objWidget.place(x=iWidgetX, y=iWidgetASY, width=iWidgetW, height=self.ilbH)
		objWidget.current(0)
		objWidget.bind("<<ComboboxSelected>>", lambda _: self._HandlerCombobox("AddSubtract"))
		self.dictWidgets["AddSubtract"]["Combobox"] = objWidget

		# Resulting date field
		iWidgetY = iWidgetASY + self.ilbH + self.iPad
		iTxtW = iWidgetX - iX - self.iPad
		dictParams = { "strState": "disabled", "objCommon": self.objCommon }
		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objRangeFrame, iX=iX, iY=iWidgetY, iW=iTxtW, iH=self.ilbH, justify="center")
		self.dictWidgets["AddSubtract"]["Text"] = objWidget

		self._CalculateDateString("StartDate")

		# Button
		objWidget = objLibTK.Button(objRangeFrame, text="Set", command=lambda: self._HandlerbtnSet())
		objWidget.place(x=iWidgetX, y=iWidgetY, width=iWidgetW, height=self.ilbH)

		iWidth = iWidgetX + iWidgetW + self.iPad
		iHeight = iWidgetY + (self.iPad * 5)
		objRangeFrame.place(x=iX, y=iY, width=iWidth, height=iHeight)

		return [iWidth, iHeight]
	# End of _CreateDateRange()

	def _CreateFilters(self, objFrame, iX, iY):
		objFilterFrame = objLibTK.LabelFrame(objFrame, text="Filters")

		iWidgetX = self.iPad
		iWidgetY = self.iPad
		iWidgetW = self.objCommon.GetFontInfo("TextWidth", "WWWW8")
		icbWH = int(self.ilbH / 2)
		icbLbW = iWidgetW - icbWH
		self.dictWidgets["Filters"] = {}
		self.dictWidgets["Filters"]["Checkboxes"] = {}
		self.dictWidgets["Filters"]["Fields"] = {}

		dictInfo = {
			"Labels": ["Day", "Month", "Year"],
			"MaxChars": [2, 0, 4],
			"iMin": [1, 0, 1973],
			"iMax": [31, 0, -1],
		}
		for iIndex in range(len(dictInfo["Labels"])):
			strLabel = dictInfo["Labels"][iIndex]
			iWidgetFilterY = iWidgetY

			dictParams = { "objCommon": self.objCommon }
			objWidget = self.objCommon.GetLibrary("sdCheckbutton", **dictParams)
			objWidget.Display(objFilterFrame, iWidgetX, iWidgetFilterY, icbWH, iDescW=icbLbW, iDescH=self.ilbH, strLabel=strLabel, bChecked=False)
			objWidget.Bind(self._HandlerCheckbutton, (strLabel,))
			self.dictWidgets["Filters"]["Checkboxes"][strLabel] = objWidget

			iWidgetFilterY += self.ilbH
			if strLabel.find("Month") == -1:
				dictParams = { "strState": "disabled", "maxChars": dictInfo["MaxChars"][iIndex], "charsAllowed": "\d+", "emptyAllowed": "no",
							   "callback": self._HandlerEntryWidget, "callbackargs": ("Filters", strLabel,), "iMin": dictInfo["iMin"][iIndex],
							   "iMax": dictInfo["iMax"][iIndex], "objCommon": self.objCommon }
				objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
				objWidget.Display(objFilterFrame, iX=iWidgetX, iY=iWidgetFilterY, iW=iWidgetW, iH=self.ilbH, justify="center")
				self.dictWidgets["Filters"]["Fields"][strLabel] = objWidget
			else:
				objWidget = objLibTTK.Combobox(master=objFilterFrame, state="readonly", values=self.arrMonth)
				objWidget.place(x=iWidgetX, y=iWidgetFilterY, width=iWidgetW, height=self.ilbH)
				objWidget.set("")
				objWidget.config(state="disabled")
				objWidget.bind("<<ComboboxSelected>>", lambda _: self._HandlerCombobox("Filters"))
				self.dictWidgets["Filters"]["Fields"][strLabel] = objWidget
			# End of if

			iWidgetX += iWidgetW + self.iPad
		# End of for loop

		iWidth = iWidgetX
		iHeight = (self.ilbH * 2) + (self.iPad * 4)
		objFilterFrame.place(x=iX, y=iY, width=iWidth, height=iHeight)

		return [iWidth, iHeight]
	# End of _CreateFilters()

	def _HandlerbtnSet(self):
		for x in range(1):
			# Get date string
			objWidget = self.dictWidgets["AddSubtract"]["Text"]
			strDate = objWidget.GetValue()

			# Get Add/Subtract combobox selection
			objWidget = self.dictWidgets["AddSubtract"]["Combobox"]
			strSelection = objWidget.get()

			match strSelection:
				case "Add":
					strKey = "StartDate"
					strText = "Start Date"
				# End of case

				case "Sub":
					strKey = "EndDate"
					strText = "End Date"
				# End of case
			# End of match

			# Check for error
			if strDate.find("Error") == 0:
				strMsg = "".join(["Correct errors in ", strText])
				self.objMessageBox.ShowError("Error", strMsg)
				break
			# End of if

			strMsg = "".join(["Set date to ", strText, "?"])
			strChoice = self.objMessageBox.ShowQuestion("Confirm", strMsg)
			if strChoice.find("Yes") != 0:
				break
			# End of if

			# Set date
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%b-%Y")
			objWidget = self.dictWidgets[strKey]["Day"]
			objWidget.SetValue(dtDate.day)

			objWidget = self.dictWidgets[strKey]["Month"]
			objWidget.current(dtDate.month-1)

			objWidget = self.dictWidgets[strKey]["Year"]
			objWidget.SetValue(dtDate.year)
		# End of for loop
	# End of _HandlerbtnSet()

	def _HandlerCheckbutton(self, strKey):
		match strKey:
			case "Day":
				objcbWidget = self.dictWidgets["Filters"]["Checkboxes"][strKey]
				objField = self.dictWidgets["Filters"]["Fields"][strKey]

				if objcbWidget.GetState():
					objField.SetState("normal")
				else:
					objField.SetValue("")
					objField.SetStatus()
					objField.SetState("disabled")
				# End of if
			# End of case

			case "Month":
				objcbWidget = self.dictWidgets["Filters"]["Checkboxes"][strKey]
				objField = self.dictWidgets["Filters"]["Fields"][strKey]

				if objcbWidget.GetState():
					objField.config(state="readonly")
					objField.current(0)
				else:
					objField.set("")
					objField.config(state="disabled")
				# End of if
			# End of case

			case "Year":
				objcbWidget = self.dictWidgets["Filters"]["Checkboxes"][strKey]
				objField = self.dictWidgets["Filters"]["Fields"][strKey]

				if objcbWidget.GetState():
					objField.SetState("normal")
				else:
					objField.SetValue("")
					objField.SetState("disabled")
				# End of if
			# End of case
		# End of match
	# End of _HandlerCheckbutton()

	def _HandlerCombobox(self, strKey):
		match strKey:
			case "AddSubtract":
				self._CalculateDateString(strKey)
			# End of case

			case "EndDate"|"StartDate":
				dtDate = self._GetDate(strKey)
				self._CalculateDateString(strKey, dtDate, False)
			# End of case

			case "Filters":
				self._ValidateFilter()
			# End of case
		# End of match
	# End of _HandlerCombobox()

	def _HandlerDatePicker(self, strKey):
		for x in range(1):
			# Get current date from GUI
			dtDate = self._GetDate(strKey)
			if dtDate is None:
				strMsg = "".join([strKey, " is invalid!"])
				self.objMessageBox.ShowError("Error", strMsg)
				break
			# End of if

			# Display date picker
			arrDate = [dtDate.day, dtDate.month, dtDate.year]
			objWidget = self.dictWidgets[strKey]["DatePicker"]
			strDate = objWidget.Display(self.objWindow, arrDate)

			if len(strDate) == 0:
				break
			# End of if

			# Update GUI with picked date
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%B-%Y")

			objWidget = self.dictWidgets[strKey]["Day"]
			objWidget.SetValue(dtDate.day)

			objWidget = self.dictWidgets[strKey]["Month"]
			objWidget.current(dtDate.month-1)

			objWidget = self.dictWidgets[strKey]["Year"]
			objWidget.SetValue(dtDate.year)
		# End of for loop
	# End of _HandlerDatePicker()

	def _HandlerEntryWidget(self, iValue, strKey, strWhich):
		match strKey:
			case "EndDate"|"StartDate":
				dtDate = self._GetDate(strKey)
				objWidget = self.dictWidgets[strKey]["Day"]
				if dtDate is None:
					strMsg = "".join(["Invalid ", strWhich])
					objWidget.SetStatus(-1, "Fatal", strMsg)
				else:
					objWidget.SetStatus()
				# End of if

				self._CalculateDateString(strKey, dtDate, False)
			# End of case

			case "Filters":
				self._ValidateFilter()
			# End of case

			case "AddSubtract":
				self._CalculateDateString(strKey)
			# End of case
		# End of match
	# End of _HandlerEntryWidget()

	def _CalculateDateString(self, strKey, dtDate=None, bCheckDate=True):
		for x in range(1):
			# Ignore if there is no date string widget
			bUpdateDateString = False
			if "AddSubtract" not in self.dictWidgets:
				break
			# End of if

			# Get combobox selection
			objWidget = self.dictWidgets["AddSubtract"]["Combobox"]
			strSelection = objWidget.get()

			if strKey.find("AddSubtract") == 0:
				# Determine which date to use
				if strSelection.find("Add") == 0:
					strKey = "StartDate"
				else:
					strKey = "EndDate"
				# End of if
			# End of if

			# Check if updation is required
			if (strSelection.find("Add") == 0) and (strKey.find("StartDate") == 0):
				bUpdateDateString = True
			elif (strSelection.find("Sub") == 0) and (strKey.find("EndDate") == 0):
				bUpdateDateString = True
			# End of if

			if not bUpdateDateString:
				break
			# End of if

			strDate = "Error"

			# Get date
			if bCheckDate:
				dtDate = self._GetDate(strKey)
			# End of if
			if dtDate is None:
				break
			# End of if

			# Get values to add / subtract
			objWidget = self.dictWidgets["AddSubtract"]["Days"]
			if objWidget.GetStatus() != 0:
				break
			# End of if
			iDays = int(objWidget.GetValue() or 0)

			objWidget = self.dictWidgets["AddSubtract"]["Months"]
			if objWidget.GetStatus() != 0:
				break
			# End of if
			iMonths = int(objWidget.GetValue() or 0)

			objWidget = self.dictWidgets["AddSubtract"]["Years"]
			if objWidget.GetStatus() != 0:
				break
			# End of if
			iYears = int(objWidget.GetValue() or 0)

			if strSelection.find("Sub") == 0:
				iDays = -iDays
				iMonths = -iMonths
				iYears = -iYears
			# End of if

			dtNewDate = dtDate + objLibRelativeDelta(years=iYears, months=iMonths, days=iDays)
			strDate = dtNewDate.strftime("%d-%b-%Y")
		# End of for loop

		if bUpdateDateString:
			objWidget = self.dictWidgets["AddSubtract"]["Text"]
			objWidget.SetValueDisabled(strDate)
		# End of if
	# End of _CalculateDateString()

	def _GetDate(self, strKey):
		objWidgetDay = self.dictWidgets[strKey]["Day"]
		iDay = int(objWidgetDay.GetValue() or 0)
		strDay = f'{iDay:02}'

		objWidget = self.dictWidgets[strKey]["Month"]
		strMonth = objWidget.get()

		objWidgetYear = self.dictWidgets[strKey]["Year"]
		iYear = int(objWidgetYear.GetValue() or 0)

		strDate = "-".join([strDay, strMonth, str(iYear)])
		try:
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%b-%Y")
		except:
			dtDate = None
		# End of try / except

		if dtDate is None:
			# Check if year is valid
			if len(str(iYear)) != 4:
				objWidgetYear.SetStatus(-1, "Fatal", "Invalid year")
			else:
				objWidgetYear.SetStatus()
			# End of if

			# Check if day is valid
			strDate = "-".join([strDay, strMonth, str(2000)])
			bDayValid = True
			try:
				objLibDateTime.datetime.strptime(strDate, "%d-%b-%Y")
			except:
				bDayValid = False
			# End of try / except

			if bDayValid:
				objWidgetDay.SetStatus()
			else:
				objWidgetDay.SetStatus(-1, "Fatal", "Invalid day")
			# End of if
		else:
			objWidgetDay.SetStatus()
			objWidgetYear.SetStatus()
		# End of if

		return dtDate
	# End of _GetDate()

	def _ValidateFilter(self, dtStart=None, dtEnd=None):
		for x in range(1):
			bValid = True
			bAlternateDay = False
			bAlternateMonth = False
			bAlternateYear = False

			# -------------------------------------- Get values --------------------------------------------
			# Get day
			objWidgetDay = self.dictWidgets["Filters"]["Fields"]["Day"]
			strState = objWidgetDay.GetState()
			if strState.find("disabled") == 0:
				strDay = "01"
				bAlternateDay = True
			else:
				iDay = int(objWidgetDay.GetValue() or 0)
				strDay = f'{iDay:02}'
			# End of if

			# Get month
			objWidget = self.dictWidgets["Filters"]["Fields"]["Month"]
			strState = str(objWidget["state"])
			if strState.find("disabled") == 0:
				strMonth = "Jan" # Use month with 31 days to check date
				bAlternateMonth = True
			else:
				strMonth = objWidget.get()
			# End of if

			# Get year
			objWidgetYear = self.dictWidgets["Filters"]["Fields"]["Year"]
			strState = objWidgetYear.GetState()
			if strState.find("disabled") == 0:
				iYear = 2000 # Use leap year to check date
				bAlternateYear = True
			else:
				iYear = int(objWidgetYear.GetValue() or 0)
			# End of if

			# Ignore if filtering is not selected
			if bAlternateDay and bAlternateMonth and bAlternateYear:
				break
			# End of if

			# Check if it is a valid date
			dtFilterDate = None
			strDate = "-".join([strDay, strMonth, str(iYear)])
			try:
				dtFilterDate = objLibDateTime.datetime.strptime(strDate, "%d-%b-%Y")
			except:
				pass
			# End of try / except

			# ----------------------------- Check error with filter values ------------------------------------
			if dtFilterDate is None:
				# Check if year is valid
				if len(str(iYear)) != 4:
					objWidgetYear.SetStatus(-1, "Fatal", "Invalid year")
				# End of if

				# Check if day is valid
				strDate = "-".join([strDay, strMonth, str(iYear)])
				bDayValid = True
				try:
					objLibDateTime.datetime.strptime(strDate, "%d-%b-%Y")
				except:
					bDayValid = False
				# End of try / except

				if not bDayValid:
					objWidgetDay.SetStatus(-1, "Fatal", "Invalid day")
				# End of if

				bValid = False
				break
			# End of if

			# ----------------------------------- Compare with dates-----------------------------------------
			# Refer flow chart "sdDateFlowChart.odg"
			# Check if start date is none
			if dtStart is None:
				break
			# End of if

			# Check if end date is none
			if dtEnd is None:
				dtEnd = dtStart
			# End of if

			# Check if start date is greater than end date
			if dtStart > dtEnd:
				bValid = False
				break
			# End of if

			# Check if filter date has alternate values
			if not (bAlternateYear or bAlternateMonth or bAlternateDay):
				# Check if filter date is within range
				if (dtFilterDate < dtStart) or (dtFilterDate > dtEnd):
					bValid = False
					break
				# End of if
				break
			# End of if

			# Check if filter has year
			if not bAlternateYear:
				# Check if filter year is within range
				if (dtFilterDate.year < dtStart.year) or (dtFilterDate.year > dtEnd.year):
					bValid = False
					break
				# End of if
			# End of if

			# Check if dates year separated
			if dtStart.year != dtEnd.year:
				if  dtFilterDate.year != dtEnd.year:
					break
				# End of if
			# End of if

			# Check if filter has month
			if not bAlternateMonth:
				# Check if month is in range
				if (dtFilterDate.month < dtStart.month) or (dtFilterDate.month > dtEnd.month):
					bValid = False
					break
				# End of if
			# End of if

			# Check if dates month separated
			if dtStart.month != dtEnd.month:
				if  dtFilterDate.month != dtEnd.month:
					break
				# End of if
			# End of if

			# Check if filter has day
			if bAlternateDay:
				break
			# End of if

			# Check if filter day is within range
			if (dtFilterDate.day < dtStart.day) or (dtFilterDate.day > dtEnd.day):
				bValid = False
				break
			# End of if
		# End of for loop

		if bValid:
			objWidgetYear.SetStatus()
			objWidgetDay.SetStatus()
		# End of if

		return bValid
	# End of _ValidateFilter()
# End of class clDate

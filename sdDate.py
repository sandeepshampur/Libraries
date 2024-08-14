#!/usr/bin/env python3

import sdCommon as objLibCommon
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

		self.objFont = objLibTkFont.Font(family=self.arrFont[1][0], size=self.arrFont[1][1], weight=self.arrFont[1][2])
		self.ilbH = self.objFont.metrics("linespace") + self.iHalfPad

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

		objDateFrame = objLibTK.LabelFrame(objFrame, text=strHeading, font=self.arrFont[0])

		match self.iComponents:
			case 1:
				# Show only date row
				iWidth = self.CreateDateRow(objDateFrame, "StartDate", self.iPad, self.iPad)
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
				iDateRowW = self.CreateDateRow(objDateFrame, "StartDate", self.iPad, self.iPad)

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

	def _CreateDateRow(self, objFrame, strKey, iX, iY):
		self.dictWidgets[strKey] = {}

		# Date
		iDateW = self.objFont.measure("888")
		dictParams = { "strValue": self.dictValues[strKey]["Day"], "maxChars": 2, "charsAllowed": "\d+", "emptyAllowed": "no",
					   "callback": self._HandlerEntryWidget, "callbackargs": (strKey, "Day",), "iMin": 1, "iMax": 31, "objCommon": self.objCommon }
		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objFrame, iX=iX, iY=iY, iW=iDateW, iH=self.ilbH, justify="center")
		self.dictWidgets[strKey]["Day"] = objWidget

		# Month
		iX += iDateW + self.iPad
		iMonthW = self.objFont.measure("WWWW")
		objWidget = objLibTTK.Combobox(master=objFrame, state="readonly", values=self.arrMonth, font=self.arrFont[0])
		objWidget.place(x=iX, y=iY, width=iMonthW, height=self.ilbH)
		objWidget.current(self.dictValues[strKey]["Month"])
		objWidget.bind("<<ComboboxSelected>>", lambda _, strKey=strKey: self._HandlerCombobox(strKey))
		self.dictWidgets[strKey]["Month"] = objWidget

		# Year
		iX += iMonthW + self.iPad
		iYearW = self.objFont.measure("88888")

		dictParams = { "strValue": self.dictValues[strKey]["Year"], "maxChars": 4, "charsAllowed": "\d+", "emptyAllowed": "no",
					   "callback": self._HandlerEntryWidget, "callbackargs": (strKey, "Year",), "iMin": 1973, "objCommon": self.objCommon }
		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objFrame, iX=iX, iY=iY, iW=iYearW, iH=self.ilbH, justify="center")
		self.dictWidgets[strKey]["Year"] = objWidget

		# Button
		ibtnX = iX + iYearW + self.iPad
		ibtnW = self.objFont.measure("WWWW") + self.iHalfPad
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
		objRangeFrame = objLibTK.LabelFrame(objFrame, text="Range", font=self.arrFont[0])

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
		iWidgetW = self.objFont.measure("88888")

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
		iWidgetW = self.objFont.measure("WWWW-")
		objWidget = objLibTTK.Combobox(master=objRangeFrame, state="readonly", values=("Add", "Sub",), font=self.arrFont[0])
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
		objFilterFrame = objLibTK.LabelFrame(objFrame, text="Filters", font=self.arrFont[0])

		iWidgetX = self.iPad
		iWidgetY = self.iPad
		iWidgetW = self.objFont.measure("WWWWW")
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
				objWidget = objLibTTK.Combobox(master=objFilterFrame, state="readonly", values=self.arrMonth, font=self.arrFont[0])
				objWidget.place(x=iWidgetX, y=iWidgetFilterY, width=iWidgetW, height=self.ilbH)
				objWidget.current(0)
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
				self.objMessageBox.ShowError(self.objWindow, "Error", strMsg)
				break
			# End of if

			strMsg = "".join(["Set date to ", strText, "?"])
			strChoice = self.objMessageBox.ShowQuestion(self.objWindow, "Confirm", strMsg)
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
		print("HandlerCheckbutton strKey:", strKey)
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
				else:
					objField.current(0)
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
		print("HandlerCombobox strKey:", strKey)
		match strKey:
			case "AddSubtract":
				self._CalculateDateString(strKey)
			# End of case

			case "EndDate"|"StartDate":
				dtDate = self._GetDate(strKey)
				self._CalculateDateString(strKey, dtDate, False)
			# End of case

			case "Filters":
				self._GetDate(strKey)
			# End of case
		# End of match
	# End of _HandlerCombobox()

	def _HandlerDatePicker(self, strKey):
		objWidget = self.dictWidgets[strKey]["DatePicker"]
		strDate = objWidget.Display(self.objWindow)
		arrDate = strDate.split("-")

		objWidget = self.dictWidgets[strKey]["Day"]
		objWidget.SetValue(int(arrDate[2]))

		objWidget = self.dictWidgets[strKey]["Month"]
		objWidget.current(int(arrDate[1])-1)

		objWidget = self.dictWidgets[strKey]["Year"]
		objWidget.SetValue(int(arrDate[0]))
	# End of _HandlerDatePicker()

	def _HandlerEntryWidget(self, iValue, strKey, strWhich):
		print("HandlerEntryWidget iValue:", iValue, "strKey:", strKey, "strWhich:", strWhich)

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
				for x in range(1):
					# Ignore if month is disabled
					objWidget = self.dictWidgets[strKey]["Fields"]["Month"]
					strState = str(objWidget["state"])
					if strState.find("disabled") == 0:
						break
					# End of if

					self._GetDate(strKey)
				# End of for loop
			# End of case

			case "AddSubtract":
				self._CalculateDateString(strKey)
			# End of case
		# End of match
	# End of _HandlerEntryWidget()

	def _CalculateDateString(self, strKey, dtDate=None, bCheckDate=True):
		print("CalculateDateString strKey:", strKey, "dtDate:", dtDate, "bCheckDate:", bCheckDate)

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
		print("GetDate strKey:", strKey)

		bAlternateDay = False
		bAlternateYear = False

		match strKey:
			case "EndDate"|"StartDate":
				objWidgetDay = self.dictWidgets[strKey]["Day"]
				iDay = int(objWidgetDay.GetValue() or 0)
				strDay = f'{iDay:02}'

				objWidget = self.dictWidgets[strKey]["Month"]
				strMonth = objWidget.get()

				objWidgetYear = self.dictWidgets[strKey]["Year"]
				iYear = int(objWidgetYear.GetValue() or 0)
			# End of case

			case "Filters":
				objWidgetDay = self.dictWidgets[strKey]["Fields"]["Day"]
				strState = objWidgetDay.GetState()
				if strState.find("disabled") == 0:
					bAlternateDay = True
					strDay = "01"
				else:
					iDay = int(objWidgetDay.GetValue() or 0)
					strDay = f'{iDay:02}'
				# End of if

				objWidget = self.dictWidgets[strKey]["Fields"]["Month"]
				strState = str(objWidget["state"])
				if strState.find("disabled") == 0:
					strMonth = "Jan"
				else:
					objWidget = self.dictWidgets[strKey]["Fields"]["Month"]
					strMonth = objWidget.get()
				# End of if

				objWidgetYear = self.dictWidgets[strKey]["Fields"]["Year"]
				strState = objWidgetYear.GetState()
				if strState.find("disabled") == 0:
					bAlternateYear = True
					iYear = 2000
				else:
					iYear = int(objWidgetYear.GetValue() or 0)
				# End of if
			# End of case
		# End of match

		strDate = "-".join([strDay, strMonth, str(iYear)])
		print(strDate)
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
			print("Day validity", strDate)
			bDayValid = True
			try:
				objLibDateTime.datetime.strptime(strDate, "%d-%b-%Y")
			except:
				bDayValid = False
			# End of try / except
			print(bDayValid)

			if bDayValid:
				objWidgetDay.SetStatus()
				print("Valid day")
			else:
				print("Invalid day")
				objWidgetDay.SetStatus(-1, "Fatal", "Invalid day")
			# End of if
		else:
			objWidgetDay.SetStatus()
			objWidgetYear.SetStatus()
		# End of if

		return dtDate
	# End of _GetDate()

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

	def _ValidateGUI(self):
		bValid = True

		match self.iComponents:
			case 1:
				# Date row only
				dtDate = self._GetDate("StartDate")
				if dtDate is None:
					bValid = False
				# End of if
			# End of case

			case 2:
				# Date range only
				dtDate = self._GetDate("StartDate")
				if dtDate is None:
					bValid = False
				# End of if
				dtDate = self._GetDate("EndDate")
				if dtDate is None:
					bValid = False
				# End of if
			# End of case

			case 3:
				# Filter only
				dtDate = self._GetDate("Filters")
				if dtDate is None:
					bValid = False
				# End of if
			# End of case

			case 4:
				# Date row with filter
				dtDate = self._GetDate("StartDate")
				if dtDate is None:
					bValid = False
				# End of if
				dtDate = self._GetDate("Filters")
				if dtDate is None:
					bValid = False
				# End of if
			# End of case

			case 5:
				# Date range with filter
				dtDate = self._GetDate("StartDate")
				if dtDate is None:
					bValid = False
				# End of if
				dtDate = self._GetDate("EndDate")
				if dtDate is None:
					bValid = False
				# End of if
				dtDate = self._GetDate("Filters")
				if dtDate is None:
					bValid = False
				# End of if
			# End of case
		# End of match

		return bValid
	# End of _ValidateGUI()
# End of class clDate

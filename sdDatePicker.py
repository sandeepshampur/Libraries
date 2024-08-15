#!/usr/bin/env python3

#
# Created: 04-March-2022
#
# Fix 		  : 22-Jun-2024 : Moved objWindow.grab_set() to end of function and added Added objWindow.wait_visibility() in clDatePicker:Display()
# Enhancement : 15-Aug-2024 : Revamped logic
#

class clDatePicker:
	def __init__(self, arrDateDefault, dictImage, arrFont, dictColours, objCommon):
		# arrDateDefault = [day, month, year]
		# month = 1 for Jan
		self.arrDateDefault = arrDateDefault
		self.dictImage = dictImage
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon

		self.objWindow = None
		self.strDate = ""
		self.iPad = 10
		self.iHalfPad = int(self.iPad / 2)

		self.dictInfo = {
			"CurrentDate": {
				"MonthDirty": False,
				"YearDirty": False
			},
			"CurrentGrid": "DateGrid",
			"Grids": ["DateGrid", "MonthGrid", "YearGrid"],
			"MonthArray": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
			"YearArray": []
		}
		'''
		Structure of self.dictInfo
		self.dictInfo = {
			"CurrentDate": {
				"Text": ""
				"Object": <objDate>
				"MonthDirty": <True|False>
				"YearDirty": <True|False>
			}
			"CurrentGrid": "<DateGrid|MonthGrid|YearGrid>"
			"Grids": []
			"YearArray": []
		}
		'''

		self.dictWidgets = { "Images": [] }
		'''
		Structure of self.dictWidgets
		self.dictWidgets = {
			"CurrentDate": <objWidget>			
			"DateGrid"|"MonthGrid"|"YearGrid": {
				"Frame": [<objWidget>, <frame info>]
				"Buttons": []
			}
			"Images": []
		}
		'''
		self.SetDate(arrDateDefault, False)
	# End of __init__()

	def Display(self, objParentWindow):
		# Initialise
		self.objParentWindow = objParentWindow

		objWindow = objLibTK.Toplevel(self.objParentWindow)
		objWindow.withdraw()
		self.objWindow = objWindow
		objWindow.wm_overrideredirect(True)
		objWindow.configure(bg=self.dictColours["colourBg"])

		# ------------------------- Border -------------------------
		objBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=self.dictColours["colourBg"])

		# ------------------------- Heading -------------------------

		print(self.arrFont)
		tFont = (self.arrFont[0], self.arrFont[1], "bold")
		objHdrLabel = objLibTK.Label(objBorder, text="Select Date", anchor="center", foreground=self.dictColours["colourFg"],
										  background=self.dictColours["colourBg"], font=tFont)
		ilbH = objHdrLabel.winfo_reqheight()

		# ------------------------- Current date -------------------------
		iCurDateY = ilbH + (self.iPad * 2)
		iCurDateW = self.objCommon.GetFontInfo("TextWidth", "00-September-0000") + self.iHalfPad

		dictParams = { "strValue": self.dictInfo["CurrentDate"]["Text"], "strState": "disabled", "objCommon": self.objCommon,
					   "tooltip": "Click to toggle grid", "tooltipPos": "top-left" }
		objWidget = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		objWidget.Display(objBorder, self.iPad, iCurDateY, iCurDateW, ilbH, justify="center")
		objWidget.Bind("<Button-1>", lambda _: self._ToggleGrid())
		self.dictWidgets["CurrentDate"] = objWidget

		# ------------------------- Date grid -------------------------
		iGridY = iCurDateY + ilbH + self.iPad
		arrGridWH = self._CreateDateGrid(objBorder, self.iPad, iGridY)
		objGrid = self.dictWidgets["DateGrid"]["Frame"][0]

		# ------------------------- Month grid -------------------------
		objGrid = self._CreateMonthYearGrid(objBorder, "MonthGrid", self.dictInfo["MonthArray"], self.iPad, iGridY, arrGridWH)
		objGrid = self.dictWidgets["MonthGrid"]["Frame"][0]
		objGrid.place_forget()

		# ------------------------- Year grid -------------------------
		objGrid = self._CreateMonthYearGrid(objBorder, "YearGrid", self.dictInfo["YearArray"], self.iPad, iGridY, arrGridWH)
		objGrid = self.dictWidgets["YearGrid"]["Frame"][0]
		objGrid.place_forget()

		# ------------------------- Scroll buttons -------------------------
		iScrW = self.objCommon.GetFontInfo("TextWidth", "WW")
		iScrX = (arrGridWH[0] + self.iPad) - iScrW

		objButton = objLibTK.Button(objWindow, text=">", foreground=self.dictColours["colourFg"], background=self.dictColours["colourBg"],
									activeforeground=self.dictColours["colourFg"], activebackground=self.dictColours["colourBg"],
									command=lambda: self._HandlerbtnLeftRight("Right"))
		objButton.place(x=iScrX, y=iCurDateY+3, width=iScrW, height=ilbH)

		iScrX -= (iScrW + self.iHalfPad)
		objButton = objLibTK.Button(objWindow, text="<", foreground=self.dictColours["colourFg"], background=self.dictColours["colourBg"],
									activeforeground=self.dictColours["colourFg"], activebackground=self.dictColours["colourBg"],
									command=lambda: self._HandlerbtnLeftRight("Left"))
		objButton.place(x=iScrX, y=iCurDateY+3, width=iScrW, height=ilbH)

		# ------------------------- Buttons -------------------------
		ibtnY = iGridY + arrGridWH[1] + (self.iPad * 3)
		ibtnW = self.objCommon.GetFontInfo("TextWidth", "Cancel") + (self.iPad * 2)
		ibtnX = int(arrGridWH[0] / 2) - (ibtnW * 1.5) - self.iPad

		dictInfo = {
			"Names": ["Done", "Reset", "Cancel"],
			"Functions": [self._HandlerbtnDone, self._HandlerbtnReset, self._HandlerbtnCancel]
		}

		for iIndex in range(len(dictInfo["Names"])):
			objButton = objLibTK.Button(objWindow, text=dictInfo["Names"][iIndex],  justify="center", foreground=self.dictColours["colourFg"],
										background=self.dictColours["colourBg"], activeforeground=self.dictColours["colourFg"],
										activebackground=self.dictColours["colourBg"], command=dictInfo["Functions"][iIndex])
			objButton.place(x=ibtnX, y=ibtnY, width=ibtnW)
			ibtnX += ibtnW + (self.iPad * 2)
		# End of for loop
		ibtnH = objButton.winfo_reqheight()

		# ------------------------- Window -------------------------

		# Bind to Esc key press
		objWindow.bind("<Escape>", lambda _: self._HandlerbtnCancel())
		objWindow.protocol("WM_DELETE_WINDOW", self._HandlerbtnCancel)

		iWinW = arrGridWH[0] + int(self.iPad * 2.5)
		iWinH = ibtnY + ibtnH + self.iPad

		# Frame
		iHdrW = iWinW - int(self.iPad * 2.5)
		objHdrLabel.place(x=self.iPad, y=self.iPad, width=iHdrW, height=ilbH)
		objBorder.place(x=0, y=0, width=iWinW, height=iWinH)

		# Get coordinates
		self.objParentWindow.update()
		iX = self.objParentWindow.winfo_rootx()
		iW = self.objParentWindow.winfo_width()
		iX += int(iW / 2)- int(iWinW / 2)
		if iX < 0:
			iX = 0
		# End of if

		self.objParentWindow.update()
		iY = self.objParentWindow.winfo_rooty()
		iH = self.objParentWindow.winfo_height()
		iScrH = objWindow.winfo_screenheight()
		iY += int(iH / 2)- int(iWinH / 2)
		if (iY + iWinH) > iScrH:
			iY = iScrH - iWinH
		# End of if

		# todo
		iX += 200
		iY += 200

		strWinDim = "".join([str(iWinW), "x", str(iWinH), "+", str(iX), "+", str(iY)])
		objWindow.geometry(strWinDim)

		objWindow.deiconify()
		objWindow.focus_force()

		objWindow.wait_visibility()
		objWindow.grab_set()

		self.objParentWindow.wait_window(objWindow)
		objWindow.grab_release()
		self.objParentWindow.focus_force()

		strDate = self.strDate
		self.strDate = ""
		return strDate
	# End of Display()

	def GetImage(self, iImgW, iImgH):
		dictParams = { "objCommon": self.objCommon }
		objCanvas = self.objCommon.GetLibrary("sdCanvas", **dictParams)

		strImgPath = objLibOSPathJoin(self.dictImage["Path"], self.dictImage["File"])
		objCanvas.CreateImage(strImgPath, iImgW, iImgH)
		dictDim = objCanvas.GetDimensions()

		self.dictWidgets["Images"].append(dictDim["Image"])

		return dictDim["Image"]
	# End of GetImage()

	def SetDate(self, arrDate, bUpdateGUI=True):
		# arrDate = [day, month, year]
		# month = 1 for Jan

		# Form date string
		if len(arrDate) == 0:
			dtDate = objLibDateTime.datetime.today()
			strDate = str(f'{dtDate.day:02}')
			strMonth = str(f'{dtDate.month:02}')
			strYear = str(dtDate.year)
		else:
			strDate = str(f'{int(arrDate[0]):02}')
			strMonth = str(f'{arrDate[1]:02}')
			strYear = str(arrDate[2])
		# End of if
		strDate = "-".join([strDate, strMonth, strYear])
		dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")

		# Update date
		self.dictInfo["CurrentDate"]["Text"] = dtDate.strftime("%d-%B-%Y")
		self.dictInfo["CurrentDate"]["Object"] = dtDate

		self._SetYearArray(int(strYear))
		if bUpdateGUI:
			self._UpdateGUI()
		# End of if
	# End of SetDate()

	def _CreateDateGrid(self, objFrame, iGridX, iGridY):
		ibtnX = 0
		ibtnY = 0
		ibtnW = self.objCommon.GetFontInfo("TextWidth", "WWd")
		ibtnH = self.objCommon.GetFontInfo("TextHeight") + self.iHalfPad
		arrHdr = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
		self.dictWidgets["DateGrid"] = {}
		self.dictWidgets["DateGrid"]["Frame"] = []
		self.dictWidgets["DateGrid"]["Buttons"] = []
		arrDateArray = self._GetDateArray()

		# Frame
		objDateFrame = objLibTK.Frame(objFrame, background=self.dictColours["colourBg"])
		self.dictWidgets["DateGrid"]["Frame"].append(objDateFrame)

		# Initialise
		dictButtons = self.dictWidgets["DateGrid"]["Buttons"]
		for iRow in range(6):
			for iColumn in range(7):
				if iRow == 0:
					objWidget = objLibTK.Label(objDateFrame, text=arrHdr[iColumn], foreground=self.dictColours["colourFg"], background=self.dictColours["colourBg"])
				else:
					iIndex = ((iRow - 1) * 7) + iColumn
					strDateValue = arrDateArray[iIndex]

					if len(strDateValue) == 0:
						objWidget = objLibTK.Button(objDateFrame, state="disabled", foreground=self.dictColours["colourFg"], background=self.dictColours["colourBg"])
					else:
						objWidget = objLibTK.Button(objDateFrame, text=strDateValue, foreground=self.dictColours["colourFg"], background=self.dictColours["colourBg"])
					# End of if
					dictButtons.append(objWidget)
				# End of if
				objWidget.place(x=ibtnX, y=ibtnY, width=ibtnW, height=ibtnH)

				# Bind
				strBtnCoord = "-".join(["DateGrid", str(iRow-1), str(iColumn)])
				objWidget.bind("<Button-1>", lambda _, strBtnCoord=strBtnCoord: self._HandlerGridButtonClick(strBtnCoord))

				ibtnX += ibtnW
			# End of for loop
			ibtnX = 0
			ibtnY +=  ibtnH
		# End of for loop

		iGridW = (ibtnW * 7) + self.iHalfPad
		iGridH = ibtnY
		objDateFrame.place(x=iGridX, y=iGridY, width=iGridW, height=iGridH)
		self.dictWidgets["DateGrid"]["Frame"].append(objDateFrame.place_info())

		return [iGridW, iGridH]
	# End of _CreateDateGrid()

	def _CreateMonthYearGrid(self, objFrame, strType, arrValues, iGridX, iGridY, arrDateGridWH):
		ibtnX = 0
		ibtnY = 0
		ibtnW = int(arrDateGridWH[0] / 3)
		ibtnH = round(arrDateGridWH[1] / 4)
		self.dictWidgets[strType] = {}
		self.dictWidgets[strType]["Frame"] = []
		self.dictWidgets[strType]["Buttons"] = []

		# Frame
		objMonthYearFrame = objLibTK.Frame(objFrame, background=self.dictColours["colourBg"])
		self.dictWidgets[strType]["Frame"].append(objMonthYearFrame)

		dictButtons = self.dictWidgets[strType]["Buttons"]
		for iRow in range(4):
			for iColumn in range(3):
				iIndex = (iRow * 3) + iColumn
				strValue = arrValues[iIndex]
				objWidget = objLibTK.Button(objMonthYearFrame, text=strValue, foreground=self.dictColours["colourFg"], background=self.dictColours["colourBg"])
				objWidget.place(x=ibtnX, y=ibtnY, width=ibtnW, height=ibtnH)
				dictButtons.append(objWidget)

				# Bind
				strBtnCoord = "-".join([strType, str(iRow), str(iColumn)])
				objWidget.bind("<Button-1>", lambda _, strBtnCoord=strBtnCoord: self._HandlerGridButtonClick(strBtnCoord))

				ibtnX += ibtnW
			# End of for loop
			ibtnX = 0
			ibtnY += ibtnH
		# End of for loop

		iGridW = (ibtnW * 3) + self.iHalfPad
		iGridH = ibtnY
		objMonthYearFrame.place(x=iGridX, y=iGridY, width=iGridW, height=iGridH)
		self.dictWidgets[strType]["Frame"].append(objMonthYearFrame.place_info())
	# End of _CreateMonthYearGrid()

	def _HandlerbtnCancel(self):
		self.objWindow.destroy()
		self.objWindow = None
	# End of _HandlerbtnCancel()

	def _HandlerbtnDone(self):
		self.strDate = "-".join([str(self.dictGrid["Date"][2]), str(self.dictGrid["Date"][1]), str(self.dictGrid["Date"][0])])
		self._HandlerbtnCancel()
	# End of _HandlerbtnDone()

	def _HandlerbtnLeftRight(self, strType):
		strCurrentGrid = self.dictInfo["CurrentGrid"]
		match strCurrentGrid:
			case "DateGrid":
				dtDate = self.dictInfo["CurrentDate"]["Object"]
				# Update month
				if strType.find("Left") == 0:
					dtNewDate = dtDate - objLibRelativeDelta(months=1)
				else:
					dtNewDate = dtDate + objLibRelativeDelta(months=1)
				# End of if

				# Set dirty flags
				self.dictInfo["CurrentDate"]["MonthDirty"] = True
				if dtDate.year != dtNewDate.year:
					self.dictInfo["CurrentDate"]["YearDirty"] = True
				# End of if

				# Update date
				arrDate = [dtNewDate.day, dtNewDate.month, dtNewDate.year]
				self.SetDate(arrDate)
			# End of case

			case "MonthGrid":
				dtDate = self.dictInfo["CurrentDate"]["Object"]
				# Update year
				if strType.find("Left") == 0:
					dtNewDate = dtDate - objLibRelativeDelta(years=1)
				else:
					dtNewDate = dtDate + objLibRelativeDelta(years=1)
				# End of if
				self.dictInfo["CurrentDate"]["YearDirty"] = True
				arrDate = [dtNewDate.day, dtNewDate.month, dtNewDate.year]
				self.SetDate(arrDate)
			# End of case

			case "YearGrid":
				dtDate = self.dictInfo["CurrentDate"]["Object"]
				# Update year
				if strType.find("Left") == 0:
					dtNewDate = dtDate - objLibRelativeDelta(years=12)
				else:
					dtNewDate = dtDate + objLibRelativeDelta(years=12)
				# End of if
				self.dictInfo["CurrentDate"]["YearDirty"] = True
				arrDate = [dtNewDate.day, dtNewDate.month, dtNewDate.year]
				self.SetDate(arrDate)
			# End of case
		# End of match
	# End of _HandlerbtnLeft()

	def _HandlerbtnReset(self):
		self.dictInfo["CurrentDate"]["MonthDirty"] = True
		self.dictInfo["CurrentDate"]["YearDirty"] = True
		self.SetDate(self.arrDateDefault)
		self._ToggleGrid("DateGrid")
	# End of _HandlerbtnReset()

	def _HandlerGridButtonClick(self, strButtonCoord):
		# Initialise
		arrText = strButtonCoord.split("-")
		strKey = arrText[0]
		iRow = int(arrText[1])
		iColumn = int(arrText[2])

		# Calculate button array index
		match strKey:
			case "DateGrid":
				iIndex = (iRow * 7) + iColumn
			# End of case

			case "MonthGrid"|"YearGrid":
				iIndex = (iRow * 3) + iColumn
			# End of case
		# End of match

		# Get text on the button clickced
		objWidget = self.dictWidgets[strKey]["Buttons"][iIndex]
		strButtonText = str(objWidget["text"])

		for x in range(1):
			if len(strButtonText) == 0:
				break
			# End of if

			# Change date
			match strKey:
				case "DateGrid":
					dtDate = self.dictInfo["CurrentDate"]["Object"]
					arrDate = [strButtonText, dtDate.month, dtDate.year]
					self.SetDate(arrDate)
				# End of case

				case "MonthGrid":
					self.dictInfo["CurrentDate"]["MonthDirty"] = True
					dtDate = self.dictInfo["CurrentDate"]["Object"]
					iMonth = self.dictInfo["MonthArray"].index(strButtonText)
					arrDate = [dtDate.day, iMonth+1, dtDate.year]
					self._ToggleGrid("DateGrid")
					self.SetDate(arrDate)
				# End of case

				case "YearGrid":
					self.dictInfo["CurrentDate"]["YearDirty"] = True
					dtDate = self.dictInfo["CurrentDate"]["Object"]
					arrDate = [dtDate.day, dtDate.month, strButtonText]
					self._ToggleGrid("MonthGrid")
					self.SetDate(arrDate)
				# End of case
			# End of match

		# End of for loop
	# End of _HandlerGridButtonClick()

	def _GetDateArray(self):
		arrDateArray = []

		# Initialise
		dtDate = objLibDateTime.datetime.strptime(self.dictInfo["CurrentDate"]["Text"], "%d-%B-%Y")
		dtDate = dtDate.replace(day=1)
		iCurMonth = dtDate.month
		iCurWeekDay = 6

		for iIndex in range(35):
			# Determine date value
			iWeekDay = dtDate.weekday()
			iMonth = dtDate.month
			for x in range(1):
				if iCurWeekDay != iWeekDay:
					strDateValue = ""
					break
				# End of if

				if iMonth != iCurMonth:
					strDateValue = ""
					break
				# End of if

				strDateValue = str(dtDate.day)
				dtDate = dtDate + objLibDateTime.timedelta(days=1)
			# End of for loop

			# Update date values
			iCurWeekDay = (iCurWeekDay + 1) % 7

			arrDateArray.append(strDateValue)
		# End of for loop

		return arrDateArray
	# End of _GetDateArray()

	def _SetYearArray(self, iYear):
		arrYear = []
		iStartYear = iYear - 5
		for iIndex in range(12):
			arrYear.append(iStartYear)
			iStartYear += 1
		# End of for loop
		self.dictInfo["YearArray"] = arrYear
	# End of _SetYearArray()

	def _ToggleGrid(self, strNextGrid=""):
		# Determine next grid to display
		strCurrentGrid = self.dictInfo["CurrentGrid"]

		if len(strNextGrid) == 0:
			iCurrentGridPos = self.dictInfo["Grids"].index(strCurrentGrid)
			iNextGridPos = (iCurrentGridPos + 1) % 3
			strNextGrid = self.dictInfo["Grids"][iNextGridPos]
		# End of if
		self.dictInfo["CurrentGrid"] = strNextGrid

		# Hide current grid
		objWidget = self.dictWidgets[strCurrentGrid]["Frame"][0]
		objWidget.place_forget()

		# Display next grid
		objWidget = self.dictWidgets[strNextGrid]["Frame"][0]
		objWidget.place(self.dictWidgets[strNextGrid]["Frame"][1])
	# End of _ToggleGrid()

	def _UpdateGUI(self):
		# Set date string
		strDate = self.dictInfo["CurrentDate"]["Text"]
		objWidget = self.dictWidgets["CurrentDate"]
		objWidget.SetValueDisabled(strDate)

		# Update date grid if dirty
		if self.dictInfo["CurrentDate"]["MonthDirty"]:
			arrDateArray = self._GetDateArray()
			for iIndex in range(35):
				objWidget = self.dictWidgets["DateGrid"]["Buttons"][iIndex]

				strDateValue = str(arrDateArray[iIndex])
				if len(strDateValue) == 0:
					objWidget.config(state="disabled")
				else:
					objWidget.config(state="normal")
				# End of if

				objWidget["text"] = strDateValue
			# End of for loop

			self.dictInfo["CurrentDate"]["MonthDirty"] = False
		# End of if

		# Update year grid if dirty
		if self.dictInfo["CurrentDate"]["YearDirty"]:
			iYear = self.dictInfo["CurrentDate"]["Object"].year
			self._SetYearArray(iYear)

			for iRow in range(4):
				for iColumn in range(3):
					iIndex = (iRow * 3) + iColumn
					objWidget = self.dictWidgets["YearGrid"]["Buttons"][iIndex]
					objWidget["text"] = self.dictInfo["YearArray"][iIndex]
				# End of for loop
			# End of for loop

			self.dictInfo["CurrentDate"]["YearDirty"] = False
		# End of if
	# End of _UpdateGUI()
# End of class clDatePicker

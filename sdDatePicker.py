#
# Created: 04-March-2022
#
# Fix : 22-Jun-2024 : Moved objWindow.grab_set() to end of function and added Added objWindow.wait_visibility() in clDatePicker:CreateWidget()
#


#********************************************************************************************
# Imports
#********************************************************************************************
import datetime as objLibDateTime
import sdCanvas as objLibCanvas
import tkinter as objLibTK
from tkinter import ttk as objLibTTK

class clDateGrid:
	def __init__(self, colourFg, colourBg, objCurrentDateChange):
		self.colourFg = colourFg
		self.colourBg = colourBg
		self.CurrentDateChange = objCurrentDateChange

		self.dictObjects = {
			"Date": [0, 0, 0],
			"Frame": {"Object": None, "Info": None},
			"Labels": []
		}
	# End of __init__()

	def Create(self, objWindow, iGridX, iGridY):
		self.objWindow = objWindow
		iX = 1
		iY = 1
		iWH = 30
		iW = (iWH*7)+8
		iH = (iWH*6)+7
		arrHdr = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

		# Frame
		objFrame = objLibTK.Frame(self.objWindow, borderwidth=0, background=self.colourBg)
		objFrame.place(x=iGridX, y=iGridY, width=iW, height=iH)
		self.dictObjects["Frame"]["Object"] = objFrame
		self.dictObjects["Frame"]["Info"] = objFrame.place_info()
		arrWH = [iW, iH]

		for iRow in range(6):
			for iColumn in range(7):
				if iRow == 0:
					objLabel = objLibTK.Label(objFrame, text=arrHdr[iColumn], foreground=self.colourFg, background=self.colourBg)
				else:
					objLabel = objLibTK.Label(objFrame, text="", foreground=self.colourFg, background=self.colourBg, borderwidth=1, relief="ridge")
				# End of if
				objLabel.place(x=iX, y=iY, width=iWH, height=iWH)
				self.dictObjects["Labels"].append(objLabel)

				# Bind
				strXY = "".join([str(iRow), "-", str(iColumn)])
				objLabel.bind("<Button-1>", lambda _, strXY=strXY: self.HandlerDateClick(strXY))

				iX += iWH + 1
			# End of for loop
			iX = 1
			iY +=  iWH + 1
		# End of for loop

		return arrWH
	# End of Create()

	def Destroy(self):
		self.dictObjects["Frame"]["Object"] = None
		self.dictObjects["Frame"]["Info"] = None
		self.dictObjects["Labels"].clear()
		self.objWindow.destroy()
	# End of Destroy()

	def Display(self, bDisplay):
		if bDisplay:
			frInfo = self.dictObjects["Frame"]["Info"]
			self.dictObjects["Frame"]["Object"].place(frInfo)
		else:
			self.dictObjects["Frame"]["Object"].place_forget()
		# End of if
	# End of Display()

	def HandlerDateClick(self, strGrid):
		for x in range(1):
			# Ignore heading
			if strGrid[0] == "0":
				break
			# End of if

			iIndex = (int(strGrid[0]) * 7) + int(strGrid[2])
			iDay = int(self.dictObjects["Labels"][iIndex]["text"] or 0)

			if iDay == 0:
				break
			# End of if

			# Update day
			self.dictObjects["Date"][0] = iDay

			# Update date
			self.CurrentDateChange(self.dictObjects["Date"])
		# End of for loop
	# End of HandlerDateClick()

	def Left(self):
		self.dictObjects["Date"][1] -= 1
		if self.dictObjects["Date"][1] < 1:
			self.dictObjects["Date"][1] = 12
			self.dictObjects["Date"][2] -= 1
		# End of if

		# Get new date
		strDate = "-".join(map(str, self.dictObjects["Date"]))
		dtDate = None
		try:
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		except:
			pass
		# End of try / except

		# Adjust day if it exceeds for the month
		if dtDate is None:
			# Calculate last day for the month
			strDate = "-".join(["28", str(self.dictObjects["Date"][1]), str(self.dictObjects["Date"][2])])
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
			dtDate = dtDate + objLibDateTime.timedelta(days=4)
			dtDate = dtDate - objLibDateTime.timedelta(days=dtDate.day)
			self.dictObjects["Date"][0] = dtDate.day
		# End of if

		self.Update()

		return self.dictObjects["Date"]
	# End of Left()

	def Right(self):
		self.dictObjects["Date"][1] += 1
		if self.dictObjects["Date"][1] > 12:
			self.dictObjects["Date"][1] = 1
			self.dictObjects["Date"][2] += 1
		# End of if

		# Get new date
		strDate = "-".join(map(str, self.dictObjects["Date"]))
		dtDate = None
		try:
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		except:
			pass
		# End of try / except

		# Adjust day if it exceeds for the month
		if dtDate is None:
			# Calculate last day for the month
			strDate = "-".join(["28", str(self.dictObjects["Date"][1]), str(self.dictObjects["Date"][2])])
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
			dtDate = dtDate + objLibDateTime.timedelta(days=4)
			dtDate = dtDate - objLibDateTime.timedelta(days=dtDate.day)
			self.dictObjects["Date"][0] = dtDate.day
		# End of if

		self.Update()

		return self.dictObjects["Date"]
	# End of Right()

	def SetDate(self, arrDate):
		self.dictObjects["Date"][0] = arrDate[0]
		self.dictObjects["Date"][1] = arrDate[1]
		self.dictObjects["Date"][2] = arrDate[2]
	# End of SetDate()

	def Update(self):
		# Get date
		strDate = "-".join(["01", str(self.dictObjects["Date"][1]), str(self.dictObjects["Date"][2])])
		dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")

		# Get date to start a day before Sunday
		iWeekNum = dtDate.isocalendar()[2] % 7
		dtDate = dtDate - objLibDateTime.timedelta(days=iWeekNum)

		# Loop through cells
		for iRow in range(5):
			for iColumn in range(7):
				# Calculate label index
				iIndex = ((iRow + 1) * 7) + iColumn

				# Check if end of month
				if dtDate.month != self.dictObjects["Date"][1]:
					self.dictObjects["Labels"][iIndex]["text"] = ""
					dtDate = dtDate + objLibDateTime.timedelta(days=1)
					continue
				# End of if

				self.dictObjects["Labels"][iIndex]["text"] = dtDate.day

				# Increment day
				dtDate = dtDate + objLibDateTime.timedelta(days=1)
			# End of for loop
		# End of for loop

		# Add spill over of days at the beginning
		iCount = 0
		while dtDate.month == self.dictObjects["Date"][1]:
			self.dictObjects["Labels"][iCount+7]["text"] = dtDate.day
			dtDate = dtDate + objLibDateTime.timedelta(days=1)
			iCount += 1
		# End of while loop
	# End of Update()
# End of class DateGrid

class clDatePicker:
	def __init__(self, colourFg, colourBg, objCallback):
		self.colourFg = colourFg
		self.colourBg = colourBg
		self.objCallback = objCallback
		self.objWindow = None

		# Classes
		objDateGrid = clDateGrid(colourFg, colourBg, self.HandlerCurrentDateChange)
		objMonthGrid = clMonthGrid(colourFg, colourBg, self.HandlerCurrentDateChange)
		objYearGrid = clYearGrid(colourFg, colourBg, self.HandlerCurrentDateChange)

		# Grid display
		dtDate = objLibDateTime.datetime.today()
		self.dictGrid = {
			"Date": [dtDate.day, dtDate.month, dtDate.year],
			"DefaultDate": [0, 0, 0],
			"Index": 0,
			"Objects": {0: objDateGrid, 1: objMonthGrid, 2: objYearGrid}
		}

		self.Images = []
	# End of __init__()

	def ShowIcon(self, objParentWindow, objMaster, iX, iY, iW, iH, strImgPath):
		# Initialise
		self.objParentWindow = objParentWindow
		self.objMaster = objMaster

		self.objCanvasIcon = objLibCanvas.clCanvas()
		self.objCanvasIcon.CreateImage(strImgPath, iW, iH)
		dictDim = self.objCanvasIcon.GetDimensions()
		self.Images.append(dictDim["Image"])
		self.objCanvasIcon.CreateCanvas(objMaster, iX, iY, self.colourBg)
		self.objCanvasIcon.Bind("<Button-1>", self.HandlerIconClick)

		return dictDim["Width"]
	# End of Show()

	def CreateWidget(self, objParentWindow=None):
		# Initialise
		if objParentWindow is not None:
			self.objParentWindow = objParentWindow
		# End of if

		objWindow = objLibTK.Toplevel(self.objParentWindow)
		objWindow.withdraw()
		self.objWindow = objWindow
		objWindow.wm_overrideredirect(True)
		objWindow.configure(bg=self.colourBg)

		# Set theme and general colours mapping
		objStyle = objLibTTK.Style()
		objStyle.theme_use("clam")

		itxtH = 25

		# ------------------------- Border -------------------------
		# Border
		objBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=self.colourBg)

		# ------------------------- Heading -------------------------

		self.objHdrLabel = objLibTK.Label(objWindow, text="Select Date", anchor="center", foreground=self.colourFg, background=self.colourBg)

		# ------------------------- Current date -------------------------
		iCurDtY = itxtH + 10
		iCurDtW = 110

		strDate = "-".join(map(str, self.dictGrid["Date"]))
		dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		strDate = dtDate.strftime("%d-%B-%Y")
		self.objCurDt = objLibTK.Label(objWindow, text=strDate, anchor="w", foreground=self.colourFg, background=self.colourBg)
		self.objCurDt.place(x=10, y=iCurDtY, width=iCurDtW, height=itxtH)
		self.objCurDt.bind("<Button-1>", lambda _: self.HandlerCurrentDate())

		# ------------------------- Date grid -------------------------
		iGdY = iCurDtY + itxtH + 10
		objWidget = self.dictGrid["Objects"][0]
		arrGridWH = objWidget.Create(objWindow, 10, iGdY)
		objWidget.SetDate(self.dictGrid["Date"])
		objWidget.Update()

		# ------------------------- Month grid -------------------------
		objWidget = self.dictGrid["Objects"][1]
		objWidget.Create(objWindow, 10, iGdY, arrGridWH[0], arrGridWH[1])
		objWidget.Display(False)

		# ------------------------- Year grid -------------------------
		objWidget = self.dictGrid["Objects"][2]
		objWidget.Create(objWindow, 10, iGdY, arrGridWH[0], arrGridWH[1])
		objWidget.Display(False)

		# ------------------------- Scroll buttons -------------------------
		iScrW = 25
		iScrX = arrGridWH[0] - (iScrW * 2) + 5

		objButton = objLibTK.Button(objWindow, text="<", foreground=self.colourFg, background=self.colourBg, activeforeground=self.colourFg, activebackground=self.colourBg, command=lambda: self.HandlerbtnLeft())
		objButton.place(x=iScrX, y=iCurDtY, width=iScrW, height=itxtH)

		iScrX += iScrW + 5
		objButton = objLibTK.Button(objWindow, text=">", foreground=self.colourFg, background=self.colourBg, activeforeground=self.colourFg, activebackground=self.colourBg, command=lambda: self.HandlerbtnRight())
		objButton.place(x=iScrX, y=iCurDtY, width=iScrW, height=itxtH)

		# ------------------------- Buttons -------------------------
		ibtnY = iGdY + arrGridWH[1] + 20
		ibtnW = 75
		ibtnX = int(arrGridWH[0] / 2) - ibtnW

		objButton = objLibTK.Button(objWindow, text="Done", justify="center", foreground=self.colourFg, background=self.colourBg, activeforeground=self.colourFg, activebackground=self.colourBg, command=lambda: self.HandlerbtnDone())
		objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=itxtH)

		ibtnX += ibtnW + 20
		objButton = objLibTK.Button(objWindow, text="Cancel", justify="center", foreground=self.colourFg, background=self.colourBg, activeforeground=self.colourFg, activebackground=self.colourBg, command=lambda: self.HandlerbtnCancel())
		objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=itxtH)

		# ------------------------- Window -------------------------

		# Bind to Esc key press
		objWindow.bind("<Escape>", lambda _: self.HandlerbtnCancel())
		objWindow.protocol("WM_DELETE_WINDOW", self.HandlerbtnCancel)

		iWinW = arrGridWH[0] + 20
		iWinH = ibtnY + itxtH + 10

		# Place widgets
		self.objHdrLabel.place(x=5, y=5, width=iWinW-10, height=itxtH)
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

		strWinDim = "".join([str(iWinW), "x", str(iWinH), "+", str(iX), "+", str(iY)])
		objWindow.geometry(strWinDim)

		objWindow.deiconify()
		objWindow.focus_force()

		objWindow.wait_visibility()
		objWindow.grab_set()

		self.objParentWindow.wait_window(objWindow)
		objWindow.grab_release()
	# End of CreateWidget()

	def HandlerbtnCancel(self):
		self.dictGrid["Objects"][0].Destroy()
		self.dictGrid["Objects"][1].Destroy()
		self.dictGrid["Objects"][2].Destroy()
		self.objWindow.destroy()
		self.objWindow = None
	# End of HandlerbtnCancel()

	def HandlerCurrentDate(self):
		# Get index
		iIndex = self.dictGrid["Index"]

		# Hide curent frame
		self.dictGrid["Objects"][iIndex].Display(False)

		# Update index
		iIndex = (iIndex + 1) % 3
		self.dictGrid["Index"] = iIndex

		# Update date and display frame
		self.dictGrid["Objects"][iIndex].SetDate(self.dictGrid["Date"])
		self.dictGrid["Objects"][iIndex].Update()
		self.dictGrid["Objects"][iIndex].Display(True)
	# End of HandlerCurrentDate()

	def HandlerCurrentDateChange(self, arrDate):
		self.dictGrid["Date"][0] = arrDate[0]
		self.dictGrid["Date"][1] = arrDate[1]
		self.dictGrid["Date"][2] = arrDate[2]

		# Update date
		strDate = "-".join(map(str, self.dictGrid["Date"]))
		dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		strDate = dtDate.strftime("%d-%B-%Y")
		self.objCurDt["text"] = strDate
	# End of HandlerCurrentDateChange()

	def HandlerbtnDone(self):
		strDate = "-".join([str(self.dictGrid["Date"][2]), str(self.dictGrid["Date"][1]), str(self.dictGrid["Date"][0])])
		self.objCallback(strDate)
		self.HandlerbtnCancel()
	# End of HandlerbtnDone()

	def HandlerbtnLeft(self):
		arrDate = self.dictGrid["Objects"][self.dictGrid["Index"]].Left()
		self.dictGrid["Date"][0] = arrDate[0]
		self.dictGrid["Date"][1] = arrDate[1]
		self.dictGrid["Date"][2] = arrDate[2]

		# Update date
		strDate = "-".join(map(str, self.dictGrid["Date"]))
		dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		strDate = dtDate.strftime("%d-%B-%Y")
		self.objCurDt["text"] = strDate
	# End of HandlerbtnLeft()

	def HandlerbtnRight(self):
		arrDate = self.dictGrid["Objects"][self.dictGrid["Index"]].Right()
		self.dictGrid["Date"][0] = arrDate[0]
		self.dictGrid["Date"][1] = arrDate[1]
		self.dictGrid["Date"][2] = arrDate[2]

		# Update date
		strDate = "-".join(map(str, self.dictGrid["Date"]))
		dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		strDate = dtDate.strftime("%d-%B-%Y")
		self.objCurDt["text"] = strDate
	# End of HandlerbtnRight()

	def HandlerIconClick(self):
		# Set date
		if self.dictGrid["DefaultDate"][0] != 0:
			self.dictGrid["Date"][0] = self.dictGrid["DefaultDate"][0]
			self.dictGrid["Date"][1] = self.dictGrid["DefaultDate"][1]
			self.dictGrid["Date"][2] = self.dictGrid["DefaultDate"][2]
		else:
			dtDate = objLibDateTime.datetime.today()
			self.dictGrid["Date"][0] = dtDate.day
			self.dictGrid["Date"][1] = dtDate.month
			self.dictGrid["Date"][2] = dtDate.year
		# End of if

		self.CreateWidget()
	# End of HandlerClock()

	def SetDate(self, arrDate):
		self.dictGrid["DefaultDate"][0] = arrDate[2]
		self.dictGrid["DefaultDate"][1] = arrDate[1]
		self.dictGrid["DefaultDate"][2] = arrDate[0]
	# End of if
# End of class clDatePicker

class clMonthGrid:
	def __init__(self, colourFg, colourBg, objCurrentDateChange):
		self.colourFg = colourFg
		self.colourBg = colourBg
		self.CurrentDateChange = objCurrentDateChange
		self.objWindow = None

		self.dictObjects = {
			"Date": [0, 0, 0],
			"Frame": {"Object": None, "Info": None},
			"Labels": []
		}

		self.arrMonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
	# End of __init__()

	def Create(self, objWindow, iGridX, iGridY, iGridW, iGridH):
		self.objWindow = objWindow
		iX = 1
		iY = 1
		iW = int(iGridW / 3) - 1
		iH = int(iGridH / 4) - 1

		# Frame
		objFrame = objLibTK.Frame(self.objWindow, borderwidth=0, background=self.colourBg)
		objFrame.place(x=iGridX, y=iGridY, width=iGridW, height=iGridH)
		self.dictObjects["Frame"]["Object"] = objFrame
		self.dictObjects["Frame"]["Info"] = objFrame.place_info()

		for iRow in range(4):
			for iColumn in range(3):
				iMonth = (iRow * 3) + iColumn
				objLabel = objLibTK.Label(objFrame, text=self.arrMonths[iMonth], foreground=self.colourFg, background=self.colourBg, borderwidth=1, relief="ridge")
				objLabel.place(x=iX, y=iY, width=iW, height=iH)
				self.dictObjects["Labels"].append(objLabel)

				# Bind
				strMonth = self.arrMonths[iMonth]
				objLabel.bind("<Button-1>", lambda _, strMonth=strMonth: self.HandlerMonthClick(strMonth))

				iX += iW + 1
			# End of for loop
			iX = 1
			iY +=  iH + 1
		# End of for loop
	# End of Create()

	def Destroy(self):
		self.dictObjects["Frame"]["Object"] = None
		self.dictObjects["Frame"]["Info"] = None
		self.dictObjects["Labels"].clear()
		self.objWindow.destroy()
	# End of Destroy()

	def Display(self, bDisplay):
		if bDisplay:
			frInfo = self.dictObjects["Frame"]["Info"]
			self.dictObjects["Frame"]["Object"].place(frInfo)
		else:
			self.dictObjects["Frame"]["Object"].place_forget()
		# End of if
	# End of Display()

	def HandlerMonthClick(self, strMonth):
		# Update month
		self.dictObjects["Date"][1] = self.arrMonths.index(strMonth) + 1

		# Check validity of date
		strDate = "-".join(map(str, self.dictObjects["Date"]))
		dtDate = None
		try:
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		except:
			pass
		# End of try / except

		# Adjust day if it exceeds for the month
		if dtDate is None:
			# Calculate last day for the month
			strDate = "-".join(["28", str(self.dictObjects["Date"][1]), str(self.dictObjects["Date"][2])])
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
			dtDate = dtDate + objLibDateTime.timedelta(days=4)
			dtDate = dtDate - objLibDateTime.timedelta(days=dtDate.day)
			self.dictObjects["Date"][0] = dtDate.day
		# End of if

		# Update date
		self.CurrentDateChange(self.dictObjects["Date"])
	# End of HandlerMonthClick()

	def Left(self):
		iMonth = self.dictObjects["Date"][1] - 1
		if iMonth < 1:
			iMonth = 12
		# End of if
		self.dictObjects["Date"][1] = iMonth

		# Check validity of date
		strDate = "-".join(map(str, self.dictObjects["Date"]))
		dtDate = None
		try:
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		except:
			pass
		# End of try / except

		# Adjust day if it exceeds for the month
		if dtDate is None:
			# Calculate last day for the month
			strDate = "-".join(["28", str(self.dictObjects["Date"][1]), str(self.dictObjects["Date"][2])])
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
			dtDate = dtDate + objLibDateTime.timedelta(days=4)
			dtDate = dtDate - objLibDateTime.timedelta(days=dtDate.day)
			self.dictObjects["Date"][0] = dtDate.day
		# End of if

		return self.dictObjects["Date"]
	# End of Left()

	def Right(self):
		iMonth = self.dictObjects["Date"][1] + 1
		if iMonth > 12:
			iMonth = 1
		# End of if
		self.dictObjects["Date"][1] = iMonth

		# Check validity of date
		strDate = "-".join(map(str, self.dictObjects["Date"]))
		dtDate = None
		try:
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		except:
			pass
		# End of try / except

		# Adjust day if it exceeds for the month
		if dtDate is None:
			# Calculate last day for the month
			strDate = "-".join(["28", str(self.dictObjects["Date"][1]), str(self.dictObjects["Date"][2])])
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
			dtDate = dtDate + objLibDateTime.timedelta(days=4)
			dtDate = dtDate - objLibDateTime.timedelta(days=dtDate.day)
			self.dictObjects["Date"][0] = dtDate.day
		# End of if

		return self.dictObjects["Date"]
	# End of Right()

	def SetDate(self, arrDate):
		self.dictObjects["Date"][0] = arrDate[0]
		self.dictObjects["Date"][1] = arrDate[1]
		self.dictObjects["Date"][2] = arrDate[2]
	# End of SetDate()

	def Update(self):
		pass
	# End of Update()
# End of class clMonthGrid

class clYearGrid:
	def __init__(self, colourFg, colourBg, objCurrentDateChange):
		self.colourFg = colourFg
		self.colourBg = colourBg
		self.CurrentDateChange = objCurrentDateChange
		self.objWindow = None

		self.dictObjects = {
			"Date": [0, 0, 0],
			"Frame": {"Object": None, "Info": None},
			"GridYear": 0,
			"Labels": []
		}
	# End of __init__()

	def Create(self, objWindow, iGridX, iGridY, iGridW, iGridH):
		self.objWindow = objWindow
		iX = 1
		iY = 1
		iW = int(iGridW / 3) - 1
		iH = int(iGridH / 4) - 1

		# Frame
		objFrame = objLibTK.Frame(self.objWindow, borderwidth=0, background=self.colourBg)
		objFrame.place(x=iGridX, y=iGridY, width=iGridW, height=iGridH)
		self.dictObjects["Frame"]["Object"] = objFrame
		self.dictObjects["Frame"]["Info"] = objFrame.place_info()

		for iRow in range(4):
			for iColumn in range(3):
				objLabel = objLibTK.Label(objFrame, text="", foreground=self.colourFg, background=self.colourBg, borderwidth=1, relief="ridge")
				objLabel.place(x=iX, y=iY, width=iW, height=iH)
				self.dictObjects["Labels"].append(objLabel)

				# Bind
				strXY = "".join([str(iRow), "-", str(iColumn)])
				objLabel.bind("<Button-1>", lambda _, strXY=strXY: self.HandlerYearClick(strXY))

				iX += iW + 1
			# End of for loop
			iX = 1
			iY +=  iH + 1
		# End of for loop
	# End of Create()

	def Destroy(self):
		self.dictObjects["Frame"]["Object"] = None
		self.dictObjects["Frame"]["Info"] = None
		self.dictObjects["Labels"].clear()
		self.objWindow.destroy()
	# End of Destroy()

	def Display(self, bDisplay):
		if bDisplay:
			frInfo = self.dictObjects["Frame"]["Info"]
			self.dictObjects["Frame"]["Object"].place(frInfo)
		else:
			self.dictObjects["Frame"]["Object"].place_forget()
		# End of if
	# End of Display()

	def HandlerYearClick(self, strGrid):
		# Get year
		iIndex = (int(strGrid[0]) * 3) + int(strGrid[2])
		iYear = int(self.dictObjects["Labels"][iIndex]["text"])

		self.dictObjects["Date"][2] = iYear

		# Check validity of date
		strDate = "-".join(map(str, self.dictObjects["Date"]))
		dtDate = None
		try:
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
		except:
			pass
		# End of try / except

		# Adjust day if it exceeds for the month
		if dtDate is None:
			# Calculate last day for the month
			strDate = "-".join(["28", str(self.dictObjects["Date"][1]), str(self.dictObjects["Date"][2])])
			dtDate = objLibDateTime.datetime.strptime(strDate, "%d-%m-%Y")
			dtDate = dtDate + objLibDateTime.timedelta(days=4)
			dtDate = dtDate - objLibDateTime.timedelta(days=dtDate.day)
			self.dictObjects["Date"][0] = dtDate.day
		# End of if

		# Update date
		self.CurrentDateChange(self.dictObjects["Date"])
	# End of HandlerYearClick()

	def Left(self):
		iYear = self.dictObjects["GridYear"] - 12
		self.dictObjects["GridYear"] = iYear
		self.Update()

		return self.dictObjects["Date"]
	# End of Left()

	def Right(self):
		iYear = self.dictObjects["GridYear"] + 12
		self.dictObjects["GridYear"] = iYear
		self.Update()

		return self.dictObjects["Date"]
	# End of Right()

	def SetDate(self, arrDate):
		self.dictObjects["Date"][0] = arrDate[0]
		self.dictObjects["Date"][1] = arrDate[1]
		self.dictObjects["Date"][2] = arrDate[2]
		self.dictObjects["GridYear"] = arrDate[2]
	# End of SetDate()

	def Update(self):
		iYear = self.dictObjects["GridYear"] - 5
		self.dictObjects["GridYear"] = iYear
		for iRow in range(4):
			for iColumn in range(3):
				iIndex = (iRow * 3) + iColumn
				self.dictObjects["Labels"][iIndex]["text"] = iYear
				iYear += 1
			# End of for loop
		# End of for loop
	# End of Update()
# End of class clYearGrid

#
# Created: 02-March-2022
#
# Fix : 22-Jun-2024 : Moved objWindow.grab_set() to end of function and added Added objWindow.wait_visibility() in clTimePicker:CreateWidget()
#

#********************************************************************************************
# Imports
#********************************************************************************************
import datetime as objLibDateTime
import sdCanvas as objLibCanvas
import sdEntryWidget as objLibEntryWidget
import threading as objLibThreading
import tkinter as objLibTK
from tkinter import ttk as objLibTTK

class clTimePicker:
	def __init__(self, colourFg, colourBg, objCallback):
		self.colourFg = colourFg
		self.colourBg = colourBg
		self.objCallback = objCallback

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

	def ShowWidget(self, objParentWindow=None):
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

		objStyle = objLibTTK.Style(objWindow)
		objStyle.map("TCombobox", selectforeground=[('readonly', '!focus', 'black'), ('readonly', 'focus', 'white')], selectbackground=[('readonly', '!focus', 'white')], fieldbackground=[('readonly', '!focus', 'white'), ('disabled', '#DCDAD5')], foreground=[('readonly', '!focus', 'black')])

		itxtH = 25

		# ------------------------- Border -------------------------
		# Border
		objBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=self.colourBg)

		# ------------------------- Heading -------------------------

		self.objHdrLabel = objLibTK.Label(objWindow, text="Enter time", anchor="center", foreground=self.colourFg, background=self.colourBg)

		# ------------------------- Time -------------------------
		iX = 10
		iY = itxtH + 15
		iW = 50

		# Hour
		self.txtHour = objLibEntryWidget.clEntryWidget(value="", maxChars=2, iMin=0, iMax=12, charsAllowed="\d+", emptyAllowed="yes")
		self.txtHour.Display(objWindow, x=iX, y=iY, w=iW, h=itxtH, justify="center")

		# Separator
		iX += iW + 5
		objLabel = objLibTK.Label(objWindow, text=":", anchor="center", foreground=self.colourFg, background=self.colourBg)
		objLabel.place(x=iX, y=iY, width=20, height=itxtH)

		# Minute
		iX += 25
		self.txtMinute = objLibEntryWidget.clEntryWidget(value="", maxChars=2, iMin=0, iMax=59, charsAllowed="\d+", emptyAllowed="yes")
		self.txtMinute.Display(objWindow, x=iX, y=iY, w=iW, h=itxtH, justify="center")

		# Combobox
		iX += iW + 15
		self.cbDayPart = objLibTTK.Combobox(master=objWindow, state="readonly", values=("AM", "PM", ))
		self.cbDayPart.place(x=iX, y=iY, width=iW, height=itxtH)
		self.cbDayPart.set("AM")

		iWinW = iX + iW + 15

		# Hour heading
		iX = 10
		iY += itxtH + 5
		objLabel = objLibTK.Label(objWindow, text="Hour", anchor="center", foreground=self.colourFg, background=self.colourBg)
		objLabel.place(x=iX, y=iY, width=iW, height=itxtH)

		# Minute heading
		iX += iW + 30
		objLabel = objLibTK.Label(objWindow, text="Minute", anchor="center", foreground=self.colourFg, background=self.colourBg)
		objLabel.place(x=iX, y=iY, width=iW, height=itxtH)

		# ------------------------- Buttons -------------------------
		ibtnW = 75
		ibtnX = int(iWinW / 2) - ibtnW - 10
		ibtnY = iY + itxtH + 20

		objButton = objLibTK.Button(objWindow, text="Done", foreground=self.colourFg, background=self.colourBg, activeforeground=self.colourFg, activebackground=self.colourBg, command=lambda: self.HandlerbtnDone())
		objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=itxtH)

		ibtnX += ibtnW + 20
		objButton = objLibTK.Button(objWindow, text="Cancel", foreground=self.colourFg, background=self.colourBg, activeforeground=self.colourFg, activebackground=self.colourBg, command=lambda: self.HandlerbtnCancel())
		objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=itxtH)

		# ------------------------- Window -------------------------

		# Bind to Esc key press
		objWindow.bind("<Escape>", lambda _: self.HandlerbtnCancel())
		objWindow.protocol("WM_DELETE_WINDOW", self.HandlerbtnCancel)

		iWinH = ibtnY + itxtH + 20

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
	# End of ShowWidget()

	def HandlerbtnCancel(self):
		self.objWindow.destroy()
	# End of HandlerbtnCancel()

	def HandlerbtnDone(self):
		# Get time
		iHour = int(self.txtHour.GetValue() or 0)
		iMinute = int(self.txtMinute.GetValue() or 0)
		strDayPart = self.cbDayPart.get()

		# Zero pad
		strHour = f"{iHour:02}"
		strMinute = f"{iMinute:02}"

		# Form time
		strTime = "".join([strHour, ":", strMinute, strDayPart])

		# Check if time is valid
		try:
			objLibDateTime.datetime.strptime(strTime, "%I:%M%p")
			bError = False
		except:
			bError = True
		# End of try / except

		if bError:
			self.objHdrLabel["text"] = "Invalid date! Enter valid date."
			self.objHdrLabel.configure(foreground="#FF9B9B")
			self.objWindow.focus_force()
		else:
			# Callback
			objThread = objLibThreading.Thread(target=self.objCallback, args=(strTime, ))
			objThread.start()
			self.objWindow.destroy()
		# End of if
	# End of HandlerbtnDone()

	def HandlerIconClick(self):
		self.ShowWidget()
	# End of HandlerClock()
# End of class clTimePicker

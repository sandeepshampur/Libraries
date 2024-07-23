#
# Created:	 23-July-2024
#

from datetime import datetime as objLibDateTime
from time import time as objLibCurrentTime
import tkinter as objLibTK
from tkinter import font as objLibTkFont

class clTimePicker:
	def __init__(self, font="Arial 12 normal", colourFg="black", colourBg="#d9d9d9", objCallback=None):
		self.strFont = font
		self.colourFg = colourFg
		self.colourBg = colourBg
		self.objCallback = objCallback

		self.arrFont = font.split(" ")
		self.strCurTimePeriod = "AM"
		self.strCurTimeFocus = "Hour"
		self.bResetFlow = False
		self.iHour = 0
		self.iMinute = 0
		self.strTime = ""
		self.dictWidgets = {}
		'''
		Dictionary structure
		self.dictWidgets = {
			"Time": [<Hour|Minute>]
			"TimeString": <objWidget>
			"AMPM": [<AM|PM>]
			"Numpad": [<0-9>]
			"Buttons": [<Done|Cancel>]
		}		
		'''
	# End of __init__()

	def Show(self, objParentWindow, iWinX=-1, iWinY=-1):
		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.grab_set()
		objWindow.withdraw()
		objWindow.configure(bg=self.colourBg)
		self.objWindow = objWindow

		# Font values
		objFont = objLibTkFont.Font(family=self.arrFont[0], size=self.arrFont[1], weight=self.arrFont[2])
		self.itxtH = objFont.metrics("linespace")
		self.itxtW = objFont.measure("W")

		# Screen dimensions
		self.iScrW = objParentWindow.winfo_screenwidth()
		self.iScrH = objParentWindow.winfo_screenheight()
		self.strTime = ""

		# Border
		iPad = 10
		objfrBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=self.colourBg)

		# ------------------------- Time -------------------------
		ibtnX = iPad
		ibtnY = iPad
		self.dictWidgets["Time"] = []

		# Hour
		iFontSize = int(self.arrFont[1]) * 2
		strFont = " ".join([self.arrFont[0], str(iFontSize), "bold"])
		objButton = objLibTK.Button(objfrBorder, text="00", font=strFont, padx=2, pady=2)
		objButton.config(relief="sunken")
		objButton.place(x=ibtnX, y=ibtnY)
		objButton.bind("<Button-1>", lambda _: self.HandlerbtnTime("Hour"))
		ibtnWH = objButton.winfo_reqwidth()
		self.dictWidgets["Time"].append(objButton)

		# Time separator
		ibtnX += ibtnWH + 1
		objLabel = objLibTK.Label(master=objfrBorder, text=":", font=strFont)
		objLabel.place(x=ibtnX, y=ibtnY)
		ilbW = objLabel.winfo_reqwidth()

		# Minute
		ibtnX += ilbW + 1
		objButton = objLibTK.Button(objfrBorder, text="00", font=strFont, padx=2, pady=2)
		objButton.config(relief="sunken")
		objButton.place(x=ibtnX, y=ibtnY)
		objButton.bind("<Button-1>", lambda _: self.HandlerbtnTime("Minute"))
		self.dictWidgets["Time"].append(objButton)

		self.strCurTimeFocus = "Hour"

		# ------------------------- AM / PM -------------------------
		ibtnX += ibtnWH + iPad
		ibtnH = int(ibtnWH / 2)
		iFontSize = int(int(self.arrFont[1]) * 0.75)
		strFont = " ".join([self.arrFont[0], str(iFontSize), "bold"])
		self.dictWidgets["AMPM"] = []

		arrInfo = ["AM", "PM"]
		for strPeriod in arrInfo:
			objButton = objLibTK.Button(objfrBorder, text=strPeriod, font=strFont, padx=2, pady=2,
										command=lambda strPeriod=strPeriod:self.ToggleAMPM(strPeriod))
			objButton.place(x=ibtnX, y=ibtnY, height=ibtnH)
			ibtnH = objButton.winfo_reqheight()
			self.dictWidgets["AMPM"].append(objButton)

			ibtnY += ibtnH
		# End of for loop

		# Set current time period
		fCurrentTime = objLibCurrentTime()
		strHour = objLibDateTime.fromtimestamp(fCurrentTime).strftime("%H")
		if int(strHour) > 12:
			self.strCurTimePeriod = "PM"
			self.dictWidgets["AMPM"][1].config(relief="sunken")
		else:
			self.strCurTimePeriod = "AM"
			self.dictWidgets["AMPM"][0].config(relief="sunken")
		# End of if

		# ------------------------- Time display -------------------------
		ilbTimeY = ibtnY + iPad
		ilbTimeW = 100

		strTime = "".join(["(00:00 ", self.strCurTimePeriod,")"])
		objLabel = objLibTK.Label(master=objfrBorder, text=strTime, font=self.strFont)
		ilbW = objLabel.winfo_reqwidth()

		ilbTimeX = int(((ibtnWH + ilbW) / 2) - (ilbW / 2))
		objLabel.place(x=ilbTimeX, y=ilbTimeY)
		ilbH = objLabel.winfo_reqheight()
		self.dictWidgets["TimeString"] = objLabel

		# ------------------------- Number pad -------------------------
		iNumPadX = iPad
		iNumPadY = ilbTimeY + ilbH + iPad
		self.dictWidgets["Numpad"] = []

		for iCount in range(10):
			if iCount == 9:
				iValue = 0
			else:
				iValue = iCount + 1
			# End of if

			# Center last button
			if iValue == 0:
				iNumPadX += ibtnWH
			# End of if

			objButton = objLibTK.Button(objfrBorder, text=iValue, font=self.strFont, padx=iPad, pady=iPad,
										command=lambda iValue=iValue: self.UpdateTime(iValue))

			if iCount == 0:
				ibtnWH = objButton.winfo_reqwidth()
			# End of if
			objButton.place(x=iNumPadX, y=iNumPadY, width=ibtnWH, height=ibtnWH)
			if iValue == 0:
				self.dictWidgets["Numpad"].insert(0, objButton)
			# End of if

			if (iValue % 3) == 0:
				iNumPadX = iPad
				iNumPadY += ibtnWH
			else:
				iNumPadX += ibtnWH
			# End of if
		# End of if

		# ------------------------- Buttons -------------------------
		ibtnX = iPad
		ibtnY = iNumPadY + iPad
		ibtnW = int(ibtnWH * 1.8)
		self.dictWidgets["Buttons"] = []

		dictInfo = {
			"Names": ["Done", "Cancel"],
			"Functions": [self.HandlerbtnDone, self.Exit]
		}
		for iIndex in range(len(dictInfo["Names"])):
			strName = dictInfo["Names"][iIndex]

			objButton = objLibTK.Button(objfrBorder, text=strName, font=self.strFont,
										command=dictInfo["Functions"][iIndex])
			objButton.place(x=ibtnX, y=ibtnY, width=ibtnW)
			self.dictWidgets["Buttons"].append(objButton)
			ibtnH = objButton.winfo_reqheight()

			ibtnX += ibtnW + iPad
		# End of for loop

		# ------------------------- Window -------------------------
		iWinW = ibtnX + (iPad * 2)
		iWinH = ibtnY + ibtnH + (iPad * 2)

		# Border
		objfrBorder.place(x=0, y=0, width=iWinW, height=iWinH)

		# Calculate window location
		if iWinX == -1:
			objParentWindow.update()
			iWinX = objParentWindow.winfo_x()
			iWinX += int((objParentWindow.winfo_width() / 2) - (iWinW / 2))
			if iWinX < 0:
				iWinX = 0
			elif iWinX > self.iScrW:
				iWinX -= (iWinX - self.iScrW)
			# End of if
		# End of if
		if iWinY == -1:
			objParentWindow.update()
			iWinY = objParentWindow.winfo_y()
			iWinY += int((objParentWindow.winfo_height() / 2) - (iWinH / 2))
			if iWinY < 0:
				iWinY = 0
			elif iWinY > self.iScrH:
				iWinY -= (iWinY - self.iScrH)
			# End of if
		# End of if

		objWindow.wm_overrideredirect(True)
		objWindow.bind('<Key>', self.HandlerKeystroke)
		objWindow.bind("<Escape>", lambda _: self.Exit())
		objWindow.protocol("WM_DELETE_WINDOW", self.Exit)

		strWinDim = "".join([str(iWinW), "x", str(iWinH), "+", str(iWinX), "+", str(iWinY)])
		objWindow.geometry(strWinDim)
		objWindow.deiconify()
		objWindow.focus_force()

		objParentWindow.wait_window(objWindow)
		objParentWindow.focus_force()
		return self.strTime
	# End of Show()

	def HandlerbtnDone(self):
		strHour = str(f'{self.iHour:02}')
		strMinute = str(f'{self.iMinute:02}')
		self.strTime = "".join([strHour, ":", strMinute, " ", self.strCurTimePeriod])
		self.Exit()
	# End of HandlerbtnDone()

	def HandlerbtnTime(self, strFocus):
		self.strCurTimeFocus = strFocus
		if strFocus.find("Hour") == 0:
			self.bResetFlow = True
		# End of if
	# End of HandlerbtnTime()

	def HandlerKeystroke(self, objEvent):
		for x in range(1):
			cKey = objEvent.char
			if not cKey.isdigit():
				break
			# End of if

			self.UpdateTime(int(cKey))
		# End of for loop
	# End of HandlerKeystroke()

	def Exit(self):
		self.Reset()
		self.objWindow.grab_release()
		self.objWindow.destroy()
	# End of Exit()

	def Reset(self):
		self.strCurTimePeriod = "AM"
		self.strCurTimeFocus = "Hour"
		self.bResetFlow = False
		self.iHour = 0
		self.iMinute = 0
		self.dictWidgets.clear()
	# End of Reset()

	def ToggleAMPM(self, strPeriod):
		for x in range(1):
			if self.strCurTimePeriod.find(strPeriod) == 0:
				break
			# End of if

			if self.strCurTimePeriod.find("AM") == 0:
				# Change to PM
				objWidget = self.dictWidgets["AMPM"][1]
				objWidget.config(relief="sunken")
				objWidget = self.dictWidgets["AMPM"][0]
				objWidget.config(relief="raised")
				self.strCurTimePeriod = "PM"
			else:
				# Change to AM
				objWidget = self.dictWidgets["AMPM"][0]
				objWidget.config(relief="sunken")
				objWidget = self.dictWidgets["AMPM"][1]
				objWidget.config(relief="raised")
				self.strCurTimePeriod = "AM"
			# End of if

			self.UpdateTime(-1)
		# End of for loop
	# End of ToggleAMPM()

	def UpdateTime(self, iNumber):
		for x in range(1):
			# Update AM / PM only
			if iNumber == -1:
				break
			# End of if

			# Update hour
			if self.strCurTimeFocus.find("Hour") == 0:
				if self.bResetFlow:
					self.iHour = iNumber
					self.bResetFlow = False
					break
				# End of if

				iNewHour = (self.iHour * 10) + iNumber
				if iNewHour < 13:
					self.iHour = iNewHour
					break
				# End of if

				# Fall through
				self.strCurTimeFocus = "Minute"
			# End of if

			iNewMinute = (self.iMinute * 10) + iNumber
			if iNewMinute < 60:
				self.iMinute = iNewMinute
			else:
				self.iMinute = iNumber
			# End of if
		# End of for loop

		# Update time string
		strHour = str(f'{self.iHour:02}')
		strMinute = str(f'{self.iMinute:02}')
		strTime = "".join(["(", strHour, ":", strMinute, " ", self.strCurTimePeriod, ")"])
		objWidget = self.dictWidgets["TimeString"]
		objWidget["text"] = strTime

		# Update time
		objWidget = self.dictWidgets["Time"][0]
		objWidget["text"] = strHour
		objWidget = self.dictWidgets["Time"][1]
		objWidget["text"] = strMinute
	# End of UpdateTime()
# End of class clTimePicker

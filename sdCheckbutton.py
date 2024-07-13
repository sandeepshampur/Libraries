#
# Completed : 21-February-2022
#
#
#

#********************************************************************************************
# Imports
#********************************************************************************************

import sdCanvas as objLibCanvas
import threading as objLibThreading
import tkinter as objLibTK
from tkinter import ttk as objLibTTK

class clCheckbutton:
	def __init__(self, strTickMarkPath, colourTickBg="white", colourTickBgDisabled="#DCDAD5", colourLabelFg="black", colourLabelBg="white"):
		self.strTickMarkPath = strTickMarkPath
		self.colourTickBg = colourTickBg
		self.colourTickBgDisabled = colourTickBgDisabled
		self.colourLabelBg = colourLabelBg
		self.colourLabelFg = colourLabelFg

		self.bChecked = True
		self.bDisabled = False
		self.objCallback = None
		self.tpBindArgs = None
		self.bTriggerCallback = True
	# End of __init__()

	def Display(self, objMaster, iX, iY, iTickMarkWH, iDescW=0, iDescH=0, strLabel="", bChecked=True, bDisabled=False):
		self.bChecked = bChecked
		self.bDisabled = bDisabled

		icbW = iTickMarkWH + iDescW + 5
		icbH = iTickMarkWH
		if iTickMarkWH < iDescH:
			icbH = iDescH
		# End of if

		# Tickmark -------------------------------------------------------------
		# Label
		objLabel = objLibTK.Label(objMaster, background=self.colourTickBg, borderwidth=1, relief="solid")
		objLabel.place(x=iX, y=iY, width=iTickMarkWH, height=iTickMarkWH)

		# Canvas
		self.objCanvas = objLibCanvas.clCanvas()
		self.objCanvas.CreateImage(self.strTickMarkPath, iTickMarkWH, iTickMarkWH)
		dictDim = self.objCanvas.GetDimensions()
		self.imgTickMark = dictDim["Image"]
		self.objCanvas.CreateCanvas(objLabel, 0, 0, self.colourTickBg, iW=iTickMarkWH, iH=iTickMarkWH)
		self.objCanvas.Bind("<Button-1>", self.HandlerClick)

		if not bChecked:
			self.objCanvas.Clear()
		# End of if

		# Description -------------------------------------------------------------
		if iDescW > 0:
			ilbX = iX + iTickMarkWH + 5

			objLabel = objLibTK.Label(objMaster, text=strLabel, anchor="w", foreground=self.colourLabelFg, background=self.colourLabelBg)
			objLabel.place(x=ilbX, y=iY, width=iDescW, height=iDescH)
			objLabel.bind("<Button-1>", lambda _: self.HandlerClick())
		# End of if

		return [icbW, icbH]
	# End of Display()

	def HandlerClick(self):
		for x in range(1):
			if self.bDisabled:
				break
			# End of if

			if self.bChecked:
				self.bChecked = False
				self.objCanvas.Clear()
			else:
				self.bChecked = True
				self.objCanvas.AddImage(0, 0, objImg=self.imgTickMark)
			# End of if

			if not self.bTriggerCallback:
				break
			# End of if

			if self.objCallback is None:
				break
			# End of if

			objThread = objLibThreading.Thread(target=self.objCallback, args=self.tpBindArgs)
			objThread.start()
			objThread = None
		# End of for loop
	# End of HandlerClick()

	def Bind(self, objCallback=None, tpParam=()):
		self.objCallback = objCallback
		self.tpBindArgs = tpParam
	# End of Bind()

	def Disable(self):
		self.bDisabled = True
		self.objCanvas.SetBackgroundColour(self.colourTickBgDisabled)
		self.bTriggerCallback = False
	# End of Disable()

	def Enable(self):
		self.bDisabled = False
		self.objCanvas.SetBackgroundColour(self.colourTickBg)
		self.bTriggerCallback = True
	# End of Enable()

	def GetState(self):
		return self.bChecked
	# End of GetState()

	def SetState(self, bChecked):
		self.bChecked = bChecked

		if self.bChecked:
			self.objCanvas.AddImage(0, 0, objImg=self.imgTickMark)
		else:
			self.objCanvas.Clear()
		# End of if
	# End of SetState()

	def SetCallbackTrigger(self, bTriggerCallback):
		self.bTriggerCallback = bTriggerCallback
	# End of SetCallbackTrigger()
# End of class clCheckbutton

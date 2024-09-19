#
# Completed : 21-February-2022
#
# Enhencement : 19-Sep-2024 : 1. Added parameter "font" to "__init__()". Changed default value of "colourLabelBg"
#							  2. Added code to vertically center the checkbox with respect to label height
#							  3. Modified code to match changes in library
#

from os.path import join as objLibOSPathJoin
import threading as objLibThreading
import tkinter as objLibTK
from tkinter import ttk as objLibTTK

class clCheckbutton:
	def __init__(self, dictImage, arrFont, dictColours, objCommon):
		self.dictImage = dictImage
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon

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
		ilbY = iY
		if iDescH > 0:
			ilbY = iY + int((iDescH / 2) - (iTickMarkWH / 2))
		# End of if

		objLabel = objLibTK.Label(objMaster, background=self.dictColours["colourTickBg"], borderwidth=1, relief="solid", font=self.arrFont)
		objLabel.place(x=iX, y=ilbY, width=iTickMarkWH, height=iTickMarkWH)

		# Canvas
		dictParams = { "objCommon": self.objCommon }
		self.objCanvas = self.objCommon.GetLibrary("sdCanvas", **dictParams)

		iPad = 2
		iImgPad = (iPad * 2)
		strTickMarkPath = objLibOSPathJoin(self.dictImage["Path"], self.dictImage["File"])
		self.objCanvas.CreateCanvasToFitImage(objLabel, strTickMarkPath, iPad, iPad, self.dictColours["colourTickBg"], iTickMarkWH-iImgPad, iTickMarkWH-iImgPad)
		self.objCanvas.Bind("<Button-1>", lambda _: self.HandlerClick())

		if not bChecked:
			self.objCanvas.ChangeImageVisibility(strState="hidden")
		# End of if

		# Description -------------------------------------------------------------
		if iDescW > 0:
			ilbX = iX + iTickMarkWH + 5

			objLabel = objLibTK.Label(objMaster, text=strLabel, anchor="w", foreground=self.dictColours["colourLabelFg"],
									  background=self.dictColours["colourLabelBg"], font=self.arrFont)
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
				self.objCanvas.ChangeImageVisibility(strState="hidden")
			else:
				self.bChecked = True
				self.objCanvas.ChangeImageVisibility(strState="normal")
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
		self.objCanvas.SetBackgroundColour(self.dictColours["colourTickBgDisabled"])
		self.bTriggerCallback = False
	# End of Disable()

	def Enable(self):
		self.bDisabled = False
		self.objCanvas.SetBackgroundColour(self.dictColours["colourTickBg"])
		self.bTriggerCallback = True
	# End of Enable()

	def GetState(self):
		return self.bChecked
	# End of GetState()

	def SetState(self, bChecked):
		self.bChecked = bChecked

		if self.bChecked:
			self.objCanvas.ChangeImageVisibility(strState="normal")
		else:
			self.objCanvas.ChangeImageVisibility(strState="hidden")
		# End of if
	# End of SetState()

	def SetCallbackTrigger(self, bTriggerCallback):
		self.bTriggerCallback = bTriggerCallback
	# End of SetCallbackTrigger()
# End of class clCheckbutton

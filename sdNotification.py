#
# Completed: 15-January-2022
#
# Enhancement : 13-Feb-2022 : Moved Window parameter from __init__() to Show() function
# Enhancement : 24-Sep-2024 : 1. Added font, colours, and objCommon as parameters
#							  2. Add functions "SetColours()" and "SetWrapLength()"
#							  3. Modified code to match changes in libraries
#

import os as objLibOS
import tkinter as objLibTK
import vlc as objLibVLC

class clNotification:
	def __init__(self, iTimeOut, iWrapLength, arrFont, dictColours, objCommon):
		self.iTimeOut = iTimeOut * 1000
		self.iWrapLength = iWrapLength
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon
	# End of __init__()

	def _GetWndXY(self, objWindow, iX, iY, iWndW, iWndH, justify):
		# Get screen dimensions
		iScrW = objWindow.winfo_screenwidth()
		iScrH = objWindow.winfo_screenheight()

		for x in range(1):
			if justify == "right-center":
				iNewX = iScrW - iWndW
				iNewY = int(iScrH / 2) - int(iWndH / 2)
				break
			# End of if

			if justify == "center":
				iNewX = int(iScrW / 2) - int(iWndW / 2)
				iNewY = int(iScrH / 2) - int(iWndH / 2)
				break
			# End of if

			if justify == "top-left":
				iNewX = 0
				iNewY = 0
				break
			# End of if

			if justify == "top-center":
				iNewX = int(iScrW / 2) - int(iWndW / 2)
				iNewY = 0
				break
			# End of if

			if justify == "top-right":
				iNewX = iScrW - iWndW
				iNewY = 0
				break
			# End of if

			if justify == "bottom-right":
				iNewX = iScrW - iWndW
				iNewY = iScrH - iWndH
				break
			# End of if

			if justify == "bottom-center":
				iNewX = int(iScrW / 2) - int(iWndW / 2)
				iNewY = iScrH - iWndH
				break
			# End of if

			if justify == "bottom-left":
				iNewX = 0
				iNewY = iScrH - iWndH
				break
			# End of if

			if justify == "left-center":
				iNewX = 0
				iNewY = int(iScrH / 2) - int(iWndH / 2)
				break
			# End of if
		# End of for loop

		if iX != -1:
			iNewX = iX
		# End of if

		if iY != -1:
			iNewY = iY
		# End of if

		return [iNewX, iNewY]
	# End of _GetWndXY()

	def SetColours(self, dictColours):
		'''
		Structure of dictColours
		dictColours = {
			"colourFg": <colour>,
			"colourBg": <colour>
		}
		'''
		self.dictColours = dictColours
	# End of SetColours()

	def SetTimeout(self, iTimeOut):
		# iTimeOut in seconds
		self.iTimeOut = iTimeOut * 1000
	# End of SetTimeout()

	def SetWrapLength(self, iWarpLength):
		self.iWrapLength = iWarpLength
	# End of SetWrapLength

	def Show(self, objParentWindow, strTitle="Title", strMsg="Message", strSound="", strImage="", iX=-1, iY=-1, iImgW=0, justify="center"):
		# Check if sound file exists
		if len(strSound) != 0:
			if not objLibOS.path.isfile(strSound):
				strSound = ""
			# End of if
		# End of if

		# Check if image file exists
		if len(strImage) != 0:
			if not objLibOS.path.isfile(strImage):
				strImage= ""
				iImgW = 0
			# End of if
		# End of if

		# Window ---------------------------------------------------------------------
		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.withdraw()
		objWindow.wm_overrideredirect(True)
		objWindow.attributes("-topmost", True)
		objWindow.configure(background=self.dictColours["colourBg"])

		# Title ---------------------------------------------------------------------
		strFont = "".join([self.arrFont[1][0], self.arrFont[1][1], "bold"])
		lbTitle = objLibTK.Label(objWindow, text=strTitle, justify="center", background=self.dictColours["colourBg"], font=strFont,
								 foreground=self.dictColours["colourFg"])
		ilbTitleW = lbTitle.winfo_reqwidth()
		ilbTitleH = lbTitle.winfo_reqheight()

		# Message ---------------------------------------------------------------------
		lbMessage = objLibTK.Label(objWindow, text=strMsg, justify="left", anchor="w", background=self.dictColours["colourBg"],
								   foreground=self.dictColours["colourFg"], wraplength=self.iWrapLength, font=self.arrFont[0])
		ilbMsgW = lbMessage.winfo_reqwidth()
		ilbMsgH = lbMessage.winfo_reqheight()

		# Image ---------------------------------------------------------------------
		iPad = 0
		iImgH = 0
		if iImgW != 0:
			dictParams = { "objCommon": self.objCommon }
			self.objCanvas = self.objCommon.GetLibrary("sdCanvas", **dictParams)
			self.objCanvas.CreateCanvasToFitImage(self, objWindow, strImage, iPad, iImgY, self.dictColours["colourBg"], iImgW)
			arrCanvasDim = self.objCanvas.GetCanvasDimensions()
			iImgH = arrCanvasDim[1]
			iPad = 5
		# End of if

		# Calculate widget coordinates and dimensions ----------------------------------------
		iImgPadW = iImgW + (iPad * 2)
		iImgPadH = iImgH + (iPad * 2)

		if ilbTitleW < (iImgPadW + ilbMsgW):
			ilbTitleW = iImgPadW + ilbMsgW
		# End of if

		iImgY = ilbTitleH + iPad
		ilbMsgX = iImgPadW

		if ilbMsgH < iImgPadH:
			ilbMsgH = iImgPadH
		# End of if

		# Place widgets ---------------------------------------------------------------------
		lbTitle.place(x=0, y=0, width=ilbTitleW, height=ilbTitleH)
		lbMessage.place(x=ilbMsgX, y=iImgY, width=ilbMsgW, height=ilbMsgH)

		# Calculate window coordinates ------------------------------------------------
		iWndW = ilbTitleW + 20
		iWndH = ilbTitleH + ilbMsgH + 20
		arrWndCoord = self._GetWndXY(objWindow, iX, iY, iWndW, iWndH, justify)

		strWinDim = "".join([str(iWndW), "x", str(iWndH), "+", str(arrWndCoord[0]), "+", str(arrWndCoord[1])])
		objWindow.geometry(strWinDim)

		objWindow.resizable(False, False)
		objWindow.bind("<Escape>", lambda _: objWindow.destroy())

		objWindow.deiconify()

		# Sound ---------------------------------------------------------------------
		if len(strSound) > 0:
			objSound = objLibVLC.MediaPlayer(strSound)
			objSound.play()
		# End of if

		# Timer ---------------------------------------------------------------------
		objWindow.after(self.iTimeout, objWindow.destroy)
	# End of Display()
# End of class clNotification

#
# Created:	 09-January-2022
#
# Fix 		  : 12-Feb-2022 : Image creation removed from __init__() and made it dynamic
# Fix 		  : 26-Feb-2022 : 1. Fixed code where pressing "Escape" button was not returing option as "Escape"
#							  2. Added flag "bDisableWinClose" and function "_HandlerWinClose()"
# Enhancement : 01-Mar-2022 : 1. Added border to window
# 							  2. Added code to consider text height based on font size
#
# Enhancement : 27-Jul-2024 : 1. Added "font" parameter to __init__()
#							  2. Redid logic of CreateWindow()
#							  3. Added function StandAlone()
# Fix		  : 07-Aug-2024 : Corrected Window width calculation in "CreateWindow()"
# Enhancement : 13-Aug-2024 : 1. Added default button text in "Show*()" functions
#							  2. Added function "SetParentWindow()" and removed passing it as parameter in "Show*()" functions
#							  3. Added code to customise colours during call to "__init__()"
#							  4. Added objCommon parameter
#

import os as objLibOS
from os.path import join as objLibOSPathJoin
import tkinter as objLibTK
from tkinter import font as objLibTkFont

class clMessageBox:
	def __init__(self, strImgPath, dictFileNames, bDisableEsc, bDisableWinClose, arrFont, dictColours, objCommon):
		self.strImgPath = strImgPath
		self.dictFileNames = dictFileNames
		self.bDisableEsc = bDisableEsc
		self.bDisableWinClose = bDisableWinClose
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon

		self.objParentWindow = None
		self.dictImages = {"Error": None, "Information": None, "Question": None, "Warning": None}
		self.strBtnOption = ""
		self.bFontInitialised = False
		dictParams = { "objCommon":self.objCommon}
		self.objCanvas = self.objCommon.GetLibrary("sdCanvas", **dictParams)
	# End of __init__()

	def _CreateWindow(self, strMBType, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg):
		objWindow = objLibTK.Toplevel(self.objParentWindow)
		objWindow.grab_set()
		objWindow.withdraw()
		objWindow.configure(bg=colourBg)
		self.objWindow = objWindow

		# Initialise
		if not self.bFontInitialised:
			objFont = objLibTkFont.Font(family=self.arrFont[1][0], size=self.arrFont[1][1], weight=self.arrFont[1][2])
			self.itxtH = objFont.metrics("linespace")
			self.itxtW = objFont.measure("W")
			self.iImgWH = self.itxtH * 3

			# Create images
			for strKey in self.dictImages:
				strPath = objLibOSPathJoin(self.strImgPath, self.dictFileNames[strKey])
				try:
					self.objCanvas.CreateImage(strPath, self.iImgWH, self.iImgWH)
				except:
					continue
				# End of try / except

				dictDim = self.objCanvas.GetDimensions()
				self.dictImages[strKey] = dictDim["Image"]
			# End of for loop

			self.bFontInitialised = True
		# End of if

		# Border
		objfrBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=colourBg)

		# ------------------------- Heading -------------------------
		tFont = (self.arrFont[1][0], self.arrFont[1][1], "bold")
		objHdrLabel = objLibTK.Label(objWindow, text=strTitle, anchor="center", font=tFont, fg=colourFg, bg=colourBg)
		iHdrlbW = objHdrLabel.winfo_reqwidth()
		iHdrlbH = objHdrLabel.winfo_reqheight()

		# ------------------------- Message -------------------------
		iMsglbY = iHdrlbH + 10
		iMsglbW = self.itxtW * 30

		objMsgLabel = objLibTK.Label(objWindow, font=(self.arrFont[0]), text=strMsg, justify="left", fg=colourFg,  bg=colourBg, wraplength=iMsglbW)
		iMsglbW = objMsgLabel.winfo_reqwidth()
		iMsglbH = objMsgLabel.winfo_reqheight()
		if iMsglbH < self.iImgWH:
			iMsglbH = self.iImgWH
		# End of if

		# ------------------------- Image -------------------------
		iImgY = iMsglbY + int(iMsglbH / 2) - int(self.iImgWH / 2)
		objImg = self.dictImages[strMBType]
		if objImg is not None:
			self.objCanvas.CreateCanvas(objWindow, 5, iImgY, colourBg, objImg=objImg)
		# End of if

		# ------------------------- Place headers -------------------------
		iMsglbX = self.iImgWH + 15

		objMsgLabel.place(x=iMsglbX, y=iMsglbY, width=iMsglbW, height=iMsglbH)
		iHdrlbW = iMsglbX + iMsglbW
		objHdrLabel.place(x=5, y=5, width=iHdrlbW, height=iHdrlbH)

		# ------------------------- Buttons -------------------------
		iMessageBoxW = iHdrlbW + 10
		ibtnY = iMsglbY + iMsglbH + 30
		ibtnW = self.itxtH * 5
		ibtnH = int(self.itxtH * 1.5)
		ibtnX = 10

		arrButtonText = [strButton1Text, strButton2Text, strButton3Text]
		for strButtonText in arrButtonText:
			if len(strButtonText) > 0:
				objButton = objLibTK.Button(objWindow, text=strButtonText, command=lambda strButtonText=strButtonText: self._Handlerbtn(strButtonText))
				objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=ibtnH)
				ibtnX += ibtnW + 10
			# End of if

		# End of for loop

		# ------------------------- Window -------------------------
		iMessageBoxW = max(iHdrlbW, iMsglbW, ibtnX) + 10
		objWindow.wm_overrideredirect(True)
		objWindow.bind("<Escape>", lambda _: self._HandlerbtnEsc())
		objWindow.protocol("WM_DELETE_WINDOW", self._HandlerWinClose)

		iMessageBoxH = ibtnY + ibtnH + 20

		# Border
		objfrBorder.place(x=0, y=0, width=iMessageBoxW, height=iMessageBoxH)

		# Calculate window location
		self.objParentWindow.update()
		# X-coordinate
		if iX == -1:
			iX = self.objParentWindow.winfo_x() + int((self.objParentWindow.winfo_width() / 2) - (iMessageBoxW / 2))
		# End of if
		if iX < 0:
			iX = 0
		elif (iX + iMessageBoxW) > self.objParentWindow.winfo_screenwidth():
			iX -= (iX + iMessageBoxW - self.objParentWindow.winfo_screenwidth())
		# End of if

		# Y-coordinate
		if iY == -1:
			iY = self.objParentWindow.winfo_y() + int((self.objParentWindow.winfo_height() / 2) - (iMessageBoxH / 2))
		# End of if
		if iY < 0:
			iY = 0
		elif (iY + iMessageBoxH) > self.objParentWindow.winfo_screenheight():
			iY -= (iY + iMessageBoxH - self.objParentWindow.winfo_screenheight())
		# End of if

		strWinDim = "".join([str(iMessageBoxW), "x", str(iMessageBoxH), "+", str(iX), "+", str(iY)])
		objWindow.geometry(strWinDim)
		objWindow.focus_force()
		objWindow.deiconify()

		self.objParentWindow.wait_window(objWindow)
		self.objParentWindow.focus_force()
	# End of _CreateWindow()

	def _Handlerbtn(self, strBtnOption):
		self.strBtnOption = strBtnOption
		self._Exit()
	# End of _Handlerbtn()

	def _HandlerbtnEsc(self):
		if not self.bDisableEsc:
			self.strBtnOption = "Escape"
			self._Exit()
		# End of if
	# End of _HandlerbtnEsc()

	def _HandlerWinClose(self):
		if not self.bDisableWinClose:
			self.strBtnOption = "Close"
			self._Exit()
		# End of if
	# End of _HandlerWinClose()

	def SetParentWindow(self, objParentWindow):
		self.objParentWindow = objParentWindow
	# End of SetParentWindow()

	def ShowError(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		self._CreateWindow("Error", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Error"]["Fg"],
						   self.dictColours["Error"]["Bg"])
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def ShowInformation(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		self._CreateWindow("Information", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Information"]["Fg"],
						   self.dictColours["Information"]["Bg"])
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def ShowQuestion(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="Yes", strButton2Text="No", strButton3Text=""):
		self._CreateWindow("Question", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Question"]["Fg"],
						   self.dictColours["Question"]["Bg"])
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def ShowWarning(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		self._CreateWindow("Warning", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Warning"]["Fg"],
						   self.dictColours["Warning"]["Bg"])
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def StandAlone(self, strType, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		# Create window
		objWindow = objLibTK.Tk()
		objWindow.withdraw()
		objWindow.attributes("-topmost", True)
		self.objWindow = objWindow
		self.objParentWindow = objWindow

		iScrW = int(objWindow.winfo_screenwidth() / 2)
		iScrH = int(objWindow.winfo_screenheight() / 2)

		strWinDim = "".join(["100x100+", str(iScrW), "+", str(iScrH)])
		objWindow.geometry(strWinDim)
		objWindow.deiconify()

		objWindow.resizable(False, False)
		objWindow.bind("<Escape>", lambda _: objWindow.destroy)
		objWindow.protocol("WM_DELETE_WINDOW", objWindow.destroy)

		match strType:
			case "ShowError":
				self.ShowError(strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case

			case "ShowInformation":
				self.ShowInformation(strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case

			case "ShowQuestion":
				self.ShowQuestion(strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case

			case "ShowWarning":
				self.ShowWarning(strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case
		# End of match

		objWindow.destroy()
		objWindow.mainloop()
	# End of StandAlone()

	def _Exit(self):
		self.objWindow.destroy()
		self.objWindow.grab_release()
		self.objWindow = None
	# End of Exit()
# End of class clMessageBox

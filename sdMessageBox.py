#
# Created:	 09-January-2022
#
# Fix 		  : 12-Feb-2022 : Image creation removed from __init__() and made it dynamic
# Fix 		  : 26-Feb-2022 : 1. Fixed code where pressing "Escape" button was not returing option as "Escape"
#							  2. Added flag "bDisableWinClose" and function "HandlerWinClose()"
# Enhancement : 01-Mar-2022 : 1. Added border to window
# 							  2. Added code to consider text height based on font size
#
# Enhancement : 27-Jul-2024 : 1. Added "font" parameter to __init__()
#							  2. Redid logic of CreateWindow()
#							  3. Added function StandAlone()

#********************************************************************************************
# Imports
#********************************************************************************************
import os as objLibOS
from os.path import join as objLibOSPathJoin
import sdCanvas as objLibCanvas
import tkinter as objLibTK
from tkinter import font as objLibTkFont

class clMessageBox:
	def __init__(self, strImgPath="", dictFileNames={}, bDisableEsc=False, bDisableWinClose=False, font="Arial 12 normal"):
		self.strImgPath = strImgPath
		if len(dictFileNames) == 0:
			self.dictFileNames = {"Error": "MB-Error.png", "Information": "MB-Information.png", "Question": "MB-Question.png", "Warning": "MB-Warning.png"}
		else:
			self.dictFileNames = dictFileNames
		# End of if
		self.bDisableEsc = bDisableEsc
		self.bDisableWinClose = bDisableWinClose
		self.arrFont = font.split(" ")

		self.dictImages = {"Error": None, "Information": None, "Question": None, "Warning": None}
		self.strBtnOption = ""
		self.bFontInitialised = False
		self.objCanvas = objLibCanvas.clCanvas()
	# End of __init__()

	def CreateWindow(self, objParentWindow, strMBType, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg):
		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.grab_set()
		objWindow.withdraw()
		objWindow.configure(bg=colourBg)
		self.objWindow = objWindow

		# Font values
		if not self.bFontInitialised:
			objFont = objLibTkFont.Font(family=self.arrFont[0], size=self.arrFont[1], weight=self.arrFont[2])
			self.itxtH = objFont.metrics("linespace")
			self.itxtW = objFont.measure("W")
			self.iImgWH = self.itxtH * 3

			# Create images
			for strKey in self.dictImages:
				try:
					strPath = objLibOSPathJoin(self.strImgPath, self.dictFileNames[strKey])
					self.objCanvas.CreateImage(strPath, self.iImgWH, self.iImgWH)
					dictDim = self.objCanvas.GetDimensions()
					self.dictImages[strKey] = dictDim["Image"]
				except:
					pass
				# End of try / except
			# End of for loop

			self.bFontInitialised = True
		# End of if

		# Border
		objfrBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=colourBg)

		# ------------------------- Heading -------------------------
		strFont = " ".join([self.arrFont[0], str(int(self.arrFont[1])+2), "bold"])
		objHdrLabel = objLibTK.Label(objWindow, text=strTitle, anchor="center", font=strFont, fg=colourFg, bg=colourBg)
		iHdrlbH = objHdrLabel.winfo_reqheight()

		# ------------------------- Message -------------------------
		iMsglbY = iHdrlbH + 10
		iMsglbW = self.itxtW * 30

		strFont = " ".join([self.arrFont[0], str(self.arrFont[1]), "normal"])
		objMsgLabel = objLibTK.Label(objWindow, font=strFont, text=strMsg, justify="left", fg=colourFg,  bg=colourBg, wraplength=iMsglbW)
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
				objButton = objLibTK.Button(objWindow, text=strButtonText, command=lambda strButtonText=strButtonText: self.Handlerbtn(strButtonText))
				objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=ibtnH)
				ibtnX += ibtnW + 10
			# End of if

		# End of for loop

		# ------------------------- Window -------------------------
		if iMessageBoxW < ibtnX:
			iMessageBoxW = ibtnX
		# End of if
		objWindow.wm_overrideredirect(True)
		objWindow.bind("<Escape>", lambda _: self.HandlerbtnEsc())
		objWindow.protocol("WM_DELETE_WINDOW", self.HandlerWinClose)

		iMessageBoxH = ibtnY + ibtnH + 20

		# Border
		objfrBorder.place(x=0, y=0, width=iMessageBoxW, height=iMessageBoxH)

		# Calculate window location
		objParentWindow.update()
		# X-coordinate
		if iX == -1:
			iX = objParentWindow.winfo_x() + int((objParentWindow.winfo_width() / 2) - (iMessageBoxW / 2))
		# End of if
		if iX < 0:
			iX = 0
		elif (iX + iMessageBoxW) > objParentWindow.winfo_screenwidth():
			iX -= (iX + iMessageBoxW - objParentWindow.winfo_screenwidth())
		# End of if

		# Y-coordinate
		if iY == -1:
			iY = objParentWindow.winfo_y() + int((objParentWindow.winfo_height() / 2) - (iMessageBoxH / 2))
		# End of if
		if iY < 0:
			iY = 0
		elif (iY + iMessageBoxH) > objParentWindow.winfo_screenheight():
			iY -= (iY + iMessageBoxH - objParentWindow.winfo_screenheight())
		# End of if

		strWinDim = "".join([str(iMessageBoxW), "x", str(iMessageBoxH), "+", str(iX), "+", str(iY)])
		objWindow.geometry(strWinDim)
		objWindow.focus_force()
		objWindow.deiconify()

		objParentWindow.wait_window(objWindow)
		objParentWindow.focus_force()
	# End of CreateWindow()

	def Handlerbtn(self, strBtnOption):
		self.strBtnOption = strBtnOption
		self.Exit()
	# End of Handlerbtn()

	def HandlerbtnEsc(self):
		if not self.bDisableEsc:
			self.strBtnOption = "Escape"
			self.Exit()
		# End of if
	# End of HandlerbtnEsc()

	def HandlerWinClose(self):
		if not self.bDisableWinClose:
			self.strBtnOption = "Close"
			self.Exit()
		# End of if
	# End of HandlerWinClose()

	def ShowError(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="",
				  colourFg="white", colourBg="#ED1B2E"):
		self.CreateWindow(objParentWindow, "Error", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text,
						  colourFg, colourBg)
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def ShowInformation(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="",
						colourFg="white", colourBg="#65357F"):
		self.CreateWindow(objParentWindow, "Information", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text,
						  colourFg, colourBg)
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def ShowQuestion(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="",
					 colourFg="white", colourBg="#1A62C5"):
		self.CreateWindow(objParentWindow, "Question", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text,
						  colourFg, colourBg)
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def ShowWarning(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="",
					colourFg="black", colourBg="#FFD42A"):
		self.CreateWindow(objParentWindow, "Warning", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text,
						  colourFg, colourBg)
		strBtnOption = self.strBtnOption
		self.strBtnOption = ""
		return strBtnOption
	# End of ShowError()

	def StandAlone(self, strType, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text=""):
		# Create window
		objWindow = objLibTK.Tk()
		objWindow.withdraw()
		objWindow.attributes("-topmost", True)
		self.objWindow = objWindow

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
				self.ShowError(objWindow, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case

			case "ShowInformation":
				self.ShowInformation(objWindow, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case

			case "ShowQuestion":
				self.ShowQuestion(objWindow, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case

			case "ShowWarning":
				self.ShowWarning(objWindow, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text)
			# End of case
		# End of match

		objWindow.destroy()
		objWindow.mainloop()
	# End of StandAlone()

	def Exit(self):
		self.objWindow.destroy()
		self.objWindow.grab_release()
		self.objWindow = None
	# End of Exit()
# End of class clMessageBox

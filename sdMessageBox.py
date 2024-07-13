#
# Created:	 09-January-2022
#
# Fix 		  : 12-Feb-2022 : Image creation removed from __init__() and made it dynamic
# Fix 		  : 26-Feb-2022 : 1. Fixed code where pressing "Escape" button was not returing option as "Escape"
#							  2. Added flag "bDisableWinClose" and function "HandlerWinClose()"
# Enhancement : 01-Mar-2022 : 1. Added border to window
# 							  2. Added code to consider text height based on font size
#

#********************************************************************************************
# Imports
#********************************************************************************************
import os as objLibOS
import sdCanvas as objLibCanvas
import tkinter as objLibTK
from tkinter import font as objLibTkFont

class clMessageBox:
	def __init__(self, strImgPath="", dictFileNames={}, bDisableEsc=False, bDisableWinClose=False):
		if len(dictFileNames) == 0:
			dictFileNames = {"Error": "MB-Error.png", "Information": "MB-Information.png", "Question": "MB-Question.png", "Warning": "MB-Warning.png"}
		# End of if
		self.dictFileNames = dictFileNames
		self.bDisableEsc = bDisableEsc
		self.bDisableWinClose = bDisableWinClose
		self.dictImages = {"Error": None, "Information": None, "Question": None, "Warning": None}
		self.strBtnOption = ""
		self.iImgWH = -1
		self.itxtW = -1
		self.itxtH = -1

		# Check images
		self.strImgPath = ""
		for x in range(1):
			if len(strImgPath) == 0:
				break
			# End of if

			# Check if path exists
			if not objLibOS.path.isdir(strImgPath):
				break
			# End of if

			if strImgPath[-1:] != objLibOS.sep:
				strImgPath = "".join([strImgPath, objLibOS.sep])
			# End of if
			self.strImgPath = strImgPath

			# Check if images exists
			for strType in dictFileNames:
				strFilePath = "".join([strImgPath, dictFileNames[strType]])

				if not objLibOS.path.isfile(strFilePath):
					dictFileNames[strType] = ""
				else:
					dictFileNames[strType] = strFilePath
				# End of if
			# End of for loop
		# End of for loop
	# End of __init__()

	def CreateWindow(self, objParentWindow, strMBType, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg):
		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.withdraw()
		objWindow.grab_set()
		objWindow.configure(bg=colourBg)
		self.objWindow = objWindow

		# Text height
		if self.itxtH == -1:
			objFont = objLibTkFont.Font(font="TkDefaultFont")
			self.itxtH = objFont.metrics("linespace")
			self.itxtW = objFont.measure("x")
			self.iImgWH = self.itxtH * 3
		# End of if

		# Border
		objBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=colourBg)

		# ------------------------- Heading -------------------------
		objHdrLabel = objLibTK.Label(objWindow, text=strTitle, anchor="center", fg=colourFg, bg=colourBg)
		objHdrLabel.config(font="bold")
		iHdrlbH = objHdrLabel.winfo_reqheight()

		# ------------------------- Message -------------------------
		iMsglbY = iHdrlbH + 10
		iMsglbH = self.itxtH * 3
		iMsglbW = self.itxtW * 50

		objMsgLabel = objLibTK.Label(objWindow, text=strMsg, justify="left", anchor="w", fg=colourFg,  bg=colourBg, wraplength=iMsglbW)

		# ------------------------- Image -------------------------
		iImgY = iMsglbY + int(iMsglbH / 2) - int(self.iImgWH / 2)

		objImg = self.dictImages[strMBType]
		# Create image if required
		self.objCanvas = objLibCanvas.clCanvas()
		if objImg is None:
			try:
				strImgPath = self.dictFileNames[strMBType]
				self.objCanvas.CreateImage(strImgPath, self.iImgWH, self.iImgWH)
				dictDim = self.objCanvas.GetDimensions()
				objImg = dictDim["Image"]
				self.dictImages[strMBType] = objImg
			except:
				pass
			# End of try / except
		# End of if

		if objImg is not None:
			self.objCanvas.CreateCanvas(objWindow, 5, iImgY, colourBg, objImg=objImg)
		# End of if

		# ------------------------- Place headers -------------------------
		iMsglbX = self.iImgWH + 15

		objMsgLabel.place(x=iMsglbX, y=iMsglbY, width=iMsglbW, height=iMsglbH)
		iHdrlbW = iMsglbX + iMsglbW
		objHdrLabel.place(x=5, y=5, width=iHdrlbW, height=iHdrlbH)

		# ------------------------- Buttons -------------------------
		ibtnY = iMsglbY + iMsglbH + 10
		ibtnW = self.itxtH * 5
		ibtnH = int(self.itxtH * 1.5)
		ibtnX = int(iHdrlbW / 2) - int(ibtnW * 1.5) - 10

		arrButtonText = [strButton1Text, strButton2Text, strButton3Text]
		for strButtonText in arrButtonText:
			if len(strButtonText) > 0:
				objButton = objLibTK.Button(objWindow, text=strButtonText, command=lambda strButtonText=strButtonText: self.Handlerbtn(strButtonText))
				objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=ibtnH)
			# End of if

			ibtnX += ibtnW + 10
		# End of for loop

		# ------------------------- Window -------------------------
		objWindow.wm_overrideredirect(True)
		objWindow.bind("<Escape>", lambda _: self.HandlerbtnEsc())
		objWindow.protocol("WM_DELETE_WINDOW", self.HandlerWinClose)

		iWinW = iHdrlbW + 10
		iWinH = ibtnY + ibtnH + 20

		# Border
		objBorder.place(x=0, y=0, width=iWinW, height=iWinH)

		# Window location
		if iX == -1:
			objParentWindow.update()
			iWinX = objParentWindow.winfo_rootx()
			iW = objParentWindow.winfo_width()
			iWinX += int(iW / 2)- int(iWinW / 2)
			if iWinX < 0:
				iWinX = 0
			# End of if
		# End of if
		if iY == -1:
			iScrH = objParentWindow.winfo_screenheight()
			objParentWindow.update()
			iWinY = objParentWindow.winfo_rooty()
			iH = objParentWindow.winfo_height()
			iWinY += iY + int(iH / 2)- int(iWinH / 2)
			if (iWinY + iWinH) > iScrH:
				iWinY = iScrH - iWinH
			# End of if
		# End of if

		strWinDim = "".join([str(iWinW), "x", str(iWinH), "+", str(iWinX), "+", str(iWinY)])
		objWindow.geometry(strWinDim)
		objWindow.focus_force()
		objWindow.deiconify()

		objParentWindow.wait_window(objWindow)
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

	def ShowError(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="", colourFg="white", colourBg="#ED1B2E"):
		self.CreateWindow(objParentWindow, "Error", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg)
		return self.strBtnOption
	# End of ShowError()

	def ShowInformation(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="", colourFg="white", colourBg="#65357F"):
		self.CreateWindow(objParentWindow, "Information", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg)
		return self.strBtnOption
	# End of ShowError()

	def ShowQuestion(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="", colourFg="white", colourBg="#1A62C5"):
		self.CreateWindow(objParentWindow, "Question", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg)
		return self.strBtnOption
	# End of ShowError()

	def ShowWarning(self, objParentWindow, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", strButton3Text="", colourFg="black", colourBg="#FFD42A"):
		self.CreateWindow(objParentWindow, "Warning", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg)
		return self.strBtnOption
	# End of ShowError()

	def Exit(self):
		self.objCanvas = None
		self.objWindow.grab_release()
		self.objWindow.destroy()
		self.objWindow = None
	# End of Exit()
# End of class clMessageBox

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
# Enhancement : 25-Sep-2024 : 1. Added default button text in "Show*()" functions
#							  2. Added function "SetParentWindow()" and removed passing it as parameter in "Show*()" functions
#							  3. Added code to customise colours during call to "__init__()"
#							  4. Added objCommon parameter
#							  5. Modified code to match changes in libraries
# Fix		  : 17-Oct-2024 : Added "objWindow.wait_visibility()" before "grab_set" to prevent freezing of window
# Enhancement : 02-Nov-2024 : 1. Added mouse button click binding to get focus to window
#							  2. Added "overrideredirect" and removed "splash" window
# Fix		  : 28-Nov-2024 : Added missing code in "StandAlone()" to initialise font information
#


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

		self.dictInfo = {
			"ButtonChoice": "",
			"ParentWindow": None
		}

		dictParams = { "objCommon":self.objCommon}
		self.objCanvas = self.objCommon.GetLibrary("sdCanvas", **dictParams)
	# End of __init__()

	def _CreateWindow(self, strMBType, strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, colourFg, colourBg):
		self.strMBType = strMBType

		objWindow = objLibTK.Toplevel(self.dictInfo["ParentWindow"])
		objWindow.withdraw()
		objWindow.configure(bg=colourBg)
		self.objWindow = objWindow

		# Border
		objfrBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=colourBg)

		# ------------------------- Heading -------------------------
		tFont = (self.arrFont[0], self.arrFont[1], "bold")
		objHdrLabel = objLibTK.Label(objWindow, text=strTitle, anchor="center", font=tFont, fg=colourFg, bg=colourBg)
		iHdrlbW = objHdrLabel.winfo_reqwidth()
		iHdrlbH = objHdrLabel.winfo_reqheight()

		# ------------------------- Message -------------------------
		iMsglbY = iHdrlbH + 10
		iMsglbW = self.itxtW * 30

		objMsgLabel = objLibTK.Label(objWindow, text=strMsg, justify="left", fg=colourFg,  bg=colourBg, wraplength=iMsglbW)
		iMsglbW = objMsgLabel.winfo_reqwidth()
		iMsglbH = objMsgLabel.winfo_reqheight()
		if iMsglbH < self.iImgWH:
			iMsglbH = self.iImgWH
		# End of if

		# ------------------------- Image -------------------------
		iImgY = iMsglbY + int(iMsglbH / 2) - int(self.iImgWH / 2)

		# Create image
		strPath = objLibOSPathJoin(self.strImgPath, self.dictFileNames[strMBType])
		self.objCanvas.CreateCanvasToFitImage(objWindow, strPath, 5, iImgY, colourBg, self.iImgWH, self.iImgWH)

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
				objButton = objLibTK.Button(objWindow, text=strButtonText, command=lambda strButtonText=strButtonText: self._HandlerButtons(strButtonText))
				objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=ibtnH)
				ibtnX += ibtnW + 10
			# End of if

		# End of for loop

		# ------------------------- Window -------------------------
		iMessageBoxW = max(iHdrlbW, iMsglbW, ibtnX) + 10
		objWindow.overrideredirect(True)
		objWindow.bind("<Escape>", lambda _: self._HandlerbtnEsc())
		objWindow.bind("<Button-1>", objWindow.focus_force())
		objWindow.protocol("WM_DELETE_WINDOW", self._HandlerWinClose)

		iMessageBoxH = ibtnY + ibtnH + 20

		# Border
		objfrBorder.place(x=0, y=0, width=iMessageBoxW, height=iMessageBoxH)

		# Calculate window location
		objParentWindow = self.dictInfo["ParentWindow"]
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
		objWindow.deiconify()
		objWindow.wait_visibility()
		objWindow.focus_force()
		objWindow.grab_set()

		objParentWindow.wait_window(objWindow)
		objParentWindow.focus_force()
	# End of _CreateWindow()

	def SetParentWindow(self, objParentWindow):
		self.dictInfo["ParentWindow"] = objParentWindow

		self.itxtH = self.objCommon.GetFontInfo("TextHeight")
		self.itxtW = self.objCommon.GetFontInfo("TextWidth")
		self.iImgWH = self.itxtH * 3
	# End of SetParentWindow()

	def ShowError(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		self._CreateWindow("Error", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Error"]["Fg"],
						   self.dictColours["Error"]["Bg"])
		strBtnOption = self.dictInfo["ButtonChoice"]
		self.dictInfo["ButtonChoice"] = ""
		return strBtnOption
	# End of ShowError()

	def ShowInformation(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		self._CreateWindow("Information", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Information"]["Fg"],
						   self.dictColours["Information"]["Bg"])
		strBtnOption = self.dictInfo["ButtonChoice"]
		self.dictInfo["ButtonChoice"] = ""
		return strBtnOption
	# End of ShowError()

	def ShowQuestion(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="Yes", strButton2Text="No", strButton3Text=""):
		self._CreateWindow("Question", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Question"]["Fg"],
						   self.dictColours["Question"]["Bg"])
		strBtnOption = self.dictInfo["ButtonChoice"]
		self.dictInfo["ButtonChoice"] = ""
		return strBtnOption
	# End of ShowError()

	def ShowWarning(self, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		self._CreateWindow("Warning", strTitle, strMsg, iX, iY, strButton1Text, strButton2Text, strButton3Text, self.dictColours["Warning"]["Fg"],
						   self.dictColours["Warning"]["Bg"])
		strBtnOption = self.dictInfo["ButtonChoice"]
		self.dictInfo["ButtonChoice"] = ""
		return strBtnOption
	# End of ShowError()

	def StandAlone(self, strType, strTitle="", strMsg="", iX=-1, iY=-1, strButton1Text="OK", strButton2Text="", strButton3Text=""):
		# Create window
		objWindow = objLibTK.Tk()
		objWindow.withdraw()
		objWindow.attributes("-topmost", True)
		self.objWindow = objWindow
		self.dictInfo["ParentWindow"] = objWindow

		iScrW = int(objWindow.winfo_screenwidth() / 2)
		iScrH = int(objWindow.winfo_screenheight() / 2)

		strWinDim = "".join(["100x100+", str(iScrW), "+", str(iScrH)])
		objWindow.geometry(strWinDim)
		objWindow.deiconify()

		self.itxtH = self.objCommon.GetFontInfo("TextHeight")
		self.itxtW = self.objCommon.GetFontInfo("TextWidth")
		self.iImgWH = self.itxtH * 3

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

	def _HandlerbtnEsc(self):
		if not self.bDisableEsc:
			self.dictInfo["ButtonChoice"] = "Escape"
			self._Exit()
		# End of if
	# End of _HandlerbtnEsc()

	def _HandlerButtons(self, strBtnOption):
		self.dictInfo["ButtonChoice"] = strBtnOption
		self._Exit()
	# End of _HandlerButtons()

	def _HandlerWinClose(self):
		if not self.bDisableWinClose:
			self.dictInfo["ButtonChoice"] = "Close"
			self._Exit()
		# End of if
	# End of _HandlerWinClose()

	def _Exit(self):
		self.objWindow.grab_release()
		self.objWindow.destroy()
		self.objWindow = None
	# End of Exit()
# End of class clMessageBox

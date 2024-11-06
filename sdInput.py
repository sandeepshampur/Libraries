#
# Created:	 14-January-2022
#
# Enhancement : 06-Nov-2022 : 1. Modified code to match changes in libraries
#							  2. Added custom button feature
#

import math as objLibMath
import tkinter as objLibTK

class clInput:
	def __init__(self, arrFont, dictColours, objCommon):
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon

		dictParams = { "objCommon": self.objCommon }
		self.objMessageBox = self.objCommon.GetLibrary("sdMessageBox", **dictParams)
		self.objCanvas = self.objCommon.GetLibrary("sdCanvas", **dictParams)

		self.arrImages = []
		self.strUserInput = ""
	# End of __init__()

	def Display(self, objParentWindow, strTitle, strPrompt, iX=-1, iY=-1, arrButtonImages=[]):
		'''
		arrButtonImages = [<Path to OK button>, <Path to Cancel button>]
		'''
		colourFg = self.dictColours["colourFg"]
		colourBg = self.dictColours["colourBg"]

		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.title(strTitle)
		objWindow.withdraw()
		objWindow.configure(bg=self.dictColours["colourBg"])
		self.objWindow = objWindow

		# Initialise
		self.objMessageBox.SetParentWindow(objWindow)
		iPad = 10
		iHalfPad = int(iPad / 2)
		ilbH = self.objCommon.GetFontInfo(strKey="TextHeight") + iPad
		self.strUserInput = ""

		# Border
		objfrBorder = objLibTK.Frame(objWindow, borderwidth=4, relief="ridge", background=colourBg)

		# ------------------------- Prompt -------------------------
		iPromptW = self.objCommon.GetFontInfo("TextWidth") * 20 # 20 characters wide
		iPromptH = (objLibMath.ceil(len(strPrompt) / iPromptW) * ilbH) + iPad

		objMsgLabel = objLibTK.Label(objWindow, text=strPrompt, justify="left", anchor="w", fg=colourFg,  bg=colourBg, wraplength=iPromptW)
		objMsgLabel.place(x=iPad, y=iPad, width=iPromptW, height=iPromptH)

		# ------------------------- Entry widget -------------------------
		ilbY = ilbH + (iPad * 2)

		dictParams = { "emptyAllowed": "no", "objCommon": self.objCommon }
		self.objEntry = self.objCommon.GetLibrary("sdEntryWidget", **dictParams)
		self.objEntry.Display(objWindow, iPad, ilbY, iPromptW, ilbH)

		# ------------------------- Buttons -------------------------
		ibtnX = iPad
		ibtnY = ilbY + ilbH + (iPad * 2)
		ibtnW = self.objCommon.GetFontInfo("TextWidth", "Cancel") + iPad

		arrButtonText = ["OK", "Cancel"]
		for iIndex in range(2):
			strButtonText = arrButtonText[iIndex]

			if len(arrButtonImages) == 0:
				# Normal buttons
				objButton = objLibTK.Button(objWindow, text=strButtonText, command=lambda strButtonText=strButtonText: self._Handlerbtn(strButtonText))
				objButton.place(x=ibtnX, y=ibtnY, width=ibtnW, height=ilbH)
			else:
				# Custom buttons
				strImagePath = arrButtonImages[iIndex]

				# Image
				objImage = self.objCanvas.CreateImage(strImagePath, -1, ilbH)
				self.arrImages.append(objImage)
				ibtnW = objImage.width()

				# Button
				objButton = objLibTK.Button(objWindow, image=objImage, border=0, highlightthickness=0, activebackground=colourBg,
											background=colourBg, command=lambda strButtonText=strButtonText: self._Handlerbtn(strButtonText))
				objButton.place(x=ibtnX, y=ibtnY, width=ibtnW+1, height=ilbH+1)
			# End of if

			ibtnX += ibtnW + iPad
		# End of for loop

		# ------------------------- Window -------------------------
		objWindow.bind("<Escape>", lambda _: self._HandlerbtnEsc())
		objWindow.protocol("WM_DELETE_WINDOW", self._HandlerbtnEsc)
		objWindow.overrideredirect(True)

		iWinW = iPromptW + (iPad * 2)
		iWinH = ibtnY + ilbH + (iPad * 2)

		# Window location
		iWinX = iX
		if iX == -1:
			#objParentWindow.update()
			iWinX = objParentWindow.winfo_rootx()
			iW = objParentWindow.winfo_width()
			iWinX += int(iW / 2)- int(iWinW / 2)
			if iWinX < 0:
				iWinX = 0
			# End of if
		# End of if

		iWinY = iY
		if iY == -1:
			iScrH = objParentWindow.winfo_screenheight()
			#objParentWindow.update()
			iWinY = objParentWindow.winfo_rooty()
			iH = objParentWindow.winfo_height()
			iWinY += iY + int(iH / 2)- int(iWinH / 2)
			if (iWinY + iWinH) > iScrH:
				iWinY = iScrH - iWinH
			# End of if
		# End of if

		objfrBorder.place(x=0, y=0, width=iWinW, height=iWinH)

		strWinDim = "".join([str(iWinW), "x", str(iWinH), "+", str(iWinX), "+", str(iWinY)])
		objWindow.geometry(strWinDim)

		objWindow.deiconify()
		objWindow.wait_visibility()
		objWindow.grab_set()
		objWindow.focus_force()

		objParentWindow.wait_window(objWindow)

		return self.strUserInput
	# End of Display()

	def _Handlerbtn(self, strBtnOption):
		for x in range(1):
			if strBtnOption.find("Cancel") == 0:
				self._Exit()
				break
			# End of if

			self.strUserInput = self.objEntry.GetValue()
			if len(self.strUserInput) == 0:
				self.objMessageBox.ShowError("Invalid", "Input is blank")
				break
			# End of if
			self._Exit()
		# End of for loop
	# End of _Handlerbtn()

	def _HandlerbtnEsc(self):
		self._Exit()
	# End of _HandlerbtnEsc()

	def _Exit(self):
		self.arrImages.clear()
		self.objWindow.grab_release()
		self.objWindow.destroy()
	# End of _Exit()
# End of class clInput

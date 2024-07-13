#
# Created:	 14-January-2022
#

#********************************************************************************************
# Imports
#********************************************************************************************
import tkinter as objLibTK

class clInput:
	def __init__(self, bDisableEsc=False):
		self.bDisableEsc = bDisableEsc
		self.strBtnOption = ""
		self.strUserInput = ""
	# End of __init__()

	def CreateWindow(self, objParentWindow, strMsg, iX, iY, strButton1Text, strButton2Text, colourFg, colourBg):
		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.withdraw()
		objWindow.grab_set()
		objWindow.configure(bg=colourBg)
		self.objWindow = objWindow

		# ------------------------- Message -------------------------
		iMsglbH = 40
		iMsglbW = 300

		objMsgLabel = objLibTK.Label(objWindow, text=strMsg, justify="left", anchor="w", fg=colourFg,  bg=colourBg, wraplength=iMsglbW)
		objMsgLabel.place(x=10, y=10, width=iMsglbW, height=iMsglbH)
		
		# ------------------------- Entry widget -------------------------
		ilbY = iMsglbH + 20
		self.vUserInput = objLibTK.StringVar()
		objEntry = objLibTK.Entry(objWindow, textvariable=self.vUserInput)
		objEntry.place(x=10, y=ilbY, width=iMsglbW)

		# ------------------------- Buttons -------------------------
		ibtnY = ilbY + 40
		ibtnW = 75
		ibtnH = 25
		ibtnX = int(iMsglbW / 2) - int(ibtnW / 2) - 5

		arrButtonText = [strButton1Text, strButton2Text]
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
		objWindow.protocol("WM_DELETE_WINDOW", self.Exit)

		iWinW = iMsglbW + 20
		iWinH = ibtnY + ibtnH + 10

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
		self.strUserInput = self.vUserInput.get()
		self.Exit()
	# End of Handlerbtn()

	def HandlerbtnEsc(self):
		if not self.bDisableEsc:
			self.Exit()
		# End of if
	# End of HandlerbtnEsc()

	def GetInput(self, objParentWindow, strMsg="", iX=-1, iY=-1, strButton1Text="", strButton2Text="", colourFg="white", colourBg="#27AF5B"):
		self.CreateWindow(objParentWindow, strMsg, iX, iY, strButton1Text, strButton2Text, colourFg, colourBg)
		
		return [self.strBtnOption, self.strUserInput]
	# End of ShowError()

	def Exit(self):
		if len(self.strBtnOption) == 0:
			self.strBtnOption = "Escape"
		# End of if
		self.objWindow.destroy()
		self.objWindow.grab_release()
		self.objWindow = None
	# End of Exit()
# End of class clInput

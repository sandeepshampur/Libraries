#
# Completed : 29-December-2021
#
# Fix : 04-Jan-2022 : Added code to close tooltip when it is set to null
#
# Fix 		  : 13-Jul-2024 : Added code to prevent repeated calls to create tooltip when both tooltip and widget overlap
# Enhancement : 26-Sep-2024 : 1. Added function "ReplaceMessage()", "SetTooltipPosition()"
#							  2. Moved colours to dictionary
#							  3. Added font
#							  4. Added code to close tip when cursor enters tooltip window.
#							  5. Moved tooltip window creation to thread
#

from re import sub as objRESub
import threading as objLibThreading
import tkinter as objLibTK

class clTooltip:
	def __init__(self, objWidget, strMessage, strPosition, iTimeout, arrFont, dictColours):
		# Initialise class variables
		self.objWidget = objWidget
		self.strMessage = strMessage
		self.strTTPosition = strPosition
		self.iTimeout = abs(int(iTimeout) * 1000)
		self.arrFont = arrFont
		self.dictColours = dictColours

		self.objToolTipWin = None
		self.IsShowing = False
		self.lbMessage = None

		# Get screen dimensions
		self.iScrW = self.objWidget.winfo_screenwidth()
		self.iScrH = self.objWidget.winfo_screenheight()

		# Create tooltip window
		objLibThreading.Thread(target=self._CreateTTWindow, daemon=True).start()
	# End of __init__()

	def AppendMessage(self, strMessage=""):
		for x in range(1):
			if len(strMessage) == 0:
				break
			# End of if

			# Check for duplicate message
			if self.strMessage.find(strMessage) != -1:
				break
			# End of if

			if len(self.strMessage) != 0:
				self.strMessage = "\n".join([self.strMessage, strMessage])
			else:
				self.strMessage = strMessage
			# End of if

			# Get label dimensions
			if self.lbMessage is not None:
				self.lbMessage["text"] = self.strMessage
				self.lbMessage.update()
				self.ilbTTW = self.lbMessage.winfo_width() + 8
				self.ilbTTH = self.lbMessage.winfo_height() + 8
			# End of if
		# End of for loop
	# End of AppendMessage()

	def CloseTip(self, objEvent=None):
		for x in range(1):
			if not self.IsShowing:
				break
			# End of if

			self.IsShowing = False
			if self.objToolTipWin is not None:
				self.objToolTipWin.withdraw()
			# End of if
		# End of for loop
	# End of CloseTip()

	def IsError(self):
		bError = False
		if len(self.strMessage) != 0:
			bError = True
		# End of if

		return bError
	# End of IsError()

	def RemoveMessage(self, strMessage):
		for x in range(1):
			self.strMessage = self.strMessage.replace(strMessage, "")
			self.strMessage = self.strMessage.replace("\n\n", "\n")
			self.strMessage = self.strMessage.strip()

			if len(self.strMessage) == 0:
				self.CloseTip()
				break
			# End of if

			# Get label dimensions
			if self.lbMessage is not None:
				self.lbMessage["text"] = self.strMessage
				self.lbMessage.update()
				self.ilbTTW = self.lbMessage.winfo_width() + 8
				self.ilbTTH = self.lbMessage.winfo_height() + 8
			# End of if
		# End of for loop
	# End of RemoveMessage()

	def ReplaceMessage(self, strRegEx, strNewMessage):
		for x in range(1):
			if len(strRegEx) == 0:
				break
			# End of if

			if len(self.strMessage) == 0:
				self.strMessage = strNewMessage
			# End of if

			self.strMessage = objRESub(strRegEx, strNewMessage, self.strMessage)

			self.strMessage = self.strMessage.replace("\n\n", "\n")
			self.strMessage = self.strMessage.strip()

			# Get label dimensions
			if self.lbMessage is not None:
				self.lbMessage["text"] = self.strMessage
				self.lbMessage.update()
				self.ilbTTW = self.lbMessage.winfo_width() + 8
				self.ilbTTH = self.lbMessage.winfo_height() + 8
			# End of if
		# End of for loop
	# End of ReplaceMessage()

	def SetMessage(self, strMessage=""):
		for x in range(1):
			self.strMessage = strMessage
			if len(strMessage) == 0:
				self.CloseTip()
				break
			# End of if

			# Get label dimensions
			if self.lbMessage is not None:
				self.lbMessage["text"] = self.strMessage
				self.lbMessage.update()
				self.ilbTTW = self.lbMessage.winfo_width() + 8
				self.ilbTTH = self.lbMessage.winfo_height() + 8
			# End of if
		# End of for loop
	# End of SetMessage()

	def SetTooltipPosition(self, strPosition):
		self.strTTPosition = strPosition
	# End of SetTooltipPosition()

	def ShowTip(self, objEvent=None):
		for x in range(1):
			if self.objToolTipWin is None:
				break
			# End of if

			if len(self.strMessage) == 0:
				break
			# End of if

			if self.IsShowing:
				break
			# End of if

			# Get widget position
			self.objWidget.update()
			iTTX = self.objWidget.winfo_rootx()
			iTTY = self.objWidget.winfo_rooty()

			# Calculate tooltip position
			match self.strTTPosition:
				case "top-left":
					iTTY -= self.ilbTTH

					# Prevent tool tip from going out of screen
					if iTTY < 0:
						iTTY += self.ilbTTH + self.iWidgetH
					# End of if

					if (iTTX + self.ilbTTW) > self.iScrW:
						iTTX -= (iTTX + self.ilbTTW - self.iScrW)
					# End of if
				# End of case

				case "top-right":
					iTTX += self.iWidgetW

					# Prevent tool tip from going out of screen
					if (iTTX + self.ilbTTW) > self.iScrW:
						iTTX -= (iTTX + self.ilbTTW - self.iScrW)
						if (iTTY + self.ilbTTH) > self.iScrH:
							iTTY -= self.ilbTTH
						else:
							iTTY += self.iWidgetH
						# End of if
					else:
						if  (iTTY + self.ilbTTH) > self.iScrH:
							iTTY -= self.ilbTTH
						else:
							iTTY += self.iWidgetH
						# End of if
					# End of if
				# End of case

				case "bottom-left":
					iTTY += self.iWidgetH

					# Prevent tool tip from going out of screen
					if (iTTY + self.ilbTTH) > self.iScrH:
						iTTY -= (self.iWidgetH + self.ilbTTH)
					# End of if
					if (iTTX + self.ilbTTW) > self.iScrW:
						iTTX -= (iTTX + self.ilbTTW - self.iScrW)
					# End of if
				# End of case

				case "bottom-right":
					iTTX += self.iWidgetW
					iTTY += self.iWidgetH

					# Prevent tool tip from going out of screen
					if (iTTX + self.ilbTTW) > self.iScrW:
						iTTX -= (iTTX + self.ilbTTW - self.iScrW)
					# End of if
					if (iTTY + self.ilbTTH) > self.iScrH:
						iTTY -= (self.iWidgetH + self.ilbTTH)
					# End of if
				# End of case
			# End of match

			self.objToolTipWin.wm_geometry("+%d+%d" % (iTTX, iTTY))
			self.objToolTipWin.deiconify()
			self.IsShowing = True

			# Add timeout
			self.objToolTipWin.after(self.iTimeout, self.CloseTip)
		# End of for loop
	# End of ShowTip()

	def _CreateTTWindow(self):
		# Create tooltip window
		objToolTipWin = objLibTK.Toplevel(self.objWidget)
		objToolTipWin.withdraw()
		objToolTipWin.wm_attributes('-type', 'splash')
		objToolTipWin.attributes("-topmost", True)
		objFrame = objLibTK.Frame(objToolTipWin, borderwidth=0, background=self.dictColours["colourBg"])
		self.lbMessage = objLibTK.Label(objFrame, text=self.strMessage, justify=objLibTK.LEFT, background=self.dictColours["colourBg"],
										foreground=self.dictColours["colourFg"], relief=objLibTK.SOLID, borderwidth=0, wraplength=250, font=self.arrFont)
		self.lbMessage.grid(padx=(5, 5), pady=(3, 3), sticky=objLibTK.NSEW)
		objFrame.grid()

		# Tooltip Label size
		self.lbMessage.update()
		self.ilbTTW = self.lbMessage.winfo_reqwidth() + 8
		self.ilbTTH = self.lbMessage.winfo_reqheight() + 8

		# Widget size
		self.objWidget.update()
		self.iWidgetW = self.objWidget.winfo_reqwidth()
		self.iWidgetH = self.objWidget.winfo_reqheight()

		# Bindings
		self.objWidget.bind("<Enter>", self.ShowTip)
		self.objWidget.bind("<Leave>", self.CloseTip)
		objToolTipWin.bind("<Enter>", self.CloseTip)

		self.objToolTipWin = objToolTipWin
	# End of _CreateTTWindow()
# End of class clTooltip

#
# Completed : 29-December-2021
#
# Fix : 04-Jan-2022 : Added code to close tooltip when it is set to null
#
# Fix 		  : 13-Jul-2024 : Added code to prevent repeated calls to create tooltip when both tooltip and widget overlap
# Enhancement : 13-Aug-2024 : 1. Added function "ReplaceMessage()"
#							  2. Moved colours to dictionary
#							  3. Added font
#

from re import sub as objRESub
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

		# Create tooltip window
		self.objToolTipWin = objLibTK.Toplevel(self.objWidget)
		self.objToolTipWin.withdraw()
		self.objToolTipWin.wm_overrideredirect(True)
		self.objToolTipWin.attributes("-topmost", True)
		objFrame = objLibTK.Frame(self.objToolTipWin, borderwidth=0, background=self.dictColours["colourBg"])
		self.lbMessage = objLibTK.Label(objFrame, text=strMessage, justify=objLibTK.LEFT, background=self.dictColours["colourBg"],
										foreground=self.dictColours["colourFg"], relief=objLibTK.SOLID, borderwidth=0, wraplength=250, font=(self.arrFont[0]))
		self.lbMessage.grid(padx=(5, 5), pady=(3, 3), sticky=objLibTK.NSEW)
		objFrame.grid()
		self.lbMessage.update()

		# Tooltip Label size
		self.ilbTTW = self.lbMessage.winfo_width() + 8
		self.ilbTTH = self.lbMessage.winfo_height() + 8

		# Widget size
		self.objWidget.update()
		self.iWidgetW = self.objWidget.winfo_width()
		self.iWidgetH = self.objWidget.winfo_height()

		# Bind to mouse
		self.objWidget.bind("<Enter>", self.ShowTip)
		self.objWidget.bind("<Leave>", self.CloseTip)

		# Get screen dimensions
		self.iScrW = self.objWidget.winfo_screenwidth()
		self.iScrH = self.objWidget.winfo_screenheight()
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

	def ShowTip(self, objEvent=None):
		for x in range(1):
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
# End of class clTooltip

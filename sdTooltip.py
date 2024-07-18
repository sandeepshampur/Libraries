#
# Completed : 29-December-2021
#
# Fix : 04-Jan-2022 : Added code to close tooltip when it is set to null
#
# Fix : 18-Jul-2024 : Added code to prevent repeated calls to create tooltip when both tooltip and widget overlap
#
import tkinter as objLibTK

class clTooltip:
	def __init__(self, objWidget, strMessage="", strPosition="top-right", fg="black", bg="#FFFA8A", iTimeout=3):
		# Initialise class variables
		self.objWidget = objWidget
		self.strMessage = strMessage
		self.strPosition = strPosition
		self.fg = fg
		self.bg = bg
		self.iTimeout = abs(int(iTimeout) * 1000)
		self.objToolTipWin = None
		self.IsShowing = False

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
				break
			# End of if

			self.strMessage = strMessage
		# End of for loop
	# End of AppendMessage()

	def CloseTip(self, objEvent=None):
		if self.objToolTipWin:
			self.objToolTipWin.withdraw()
			self.IsShowing = False
		# End of if
	# End of CloseTip()

	def IsError(self):
		bError = False
		if len(self.strMessage) != 0:
			bError = True
		# End of if

		return bError
	# End of IsError()

	def SetMessage(self, strMessage=""):
		self.strMessage = strMessage
		if len(strMessage) == 0:
			self.CloseTip()
		# End of if
	# End of SetMessage()

	def RemoveMessage(self, strMessage):
		self.strMessage = self.strMessage.replace(strMessage, "")
		self.strMessage = self.strMessage.replace("\n\n", "\n")
		self.strMessage = self.strMessage.strip()
	# End of RemoveMessage()

	def ShowTip(self, objEvent):
		if len(self.strMessage) == 0:
			return
		# End of if

		if (self.objToolTipWin is not None) and (self.IsShowing):
			return
		# End of if

		# Create tooltip window
		if self.objToolTipWin is None:
			# Create tooltip window
			self.objToolTipWin = objLibTK.Toplevel(self.objWidget)
			self.objToolTipWin.withdraw()
			self.objToolTipWin.wm_overrideredirect(True)
			self.objToolTipWin.attributes("-topmost", True)
			objFrame = objLibTK.Frame(self.objToolTipWin, borderwidth=0, background=self.bg)
			self.lbMessage = objLibTK.Label(objFrame, justify=objLibTK.LEFT, background=self.bg, foreground=self.fg, relief=objLibTK.SOLID, borderwidth=0, wraplength=250)
			self.lbMessage.grid(padx=(5, 5), pady=(3, 3), sticky=objLibTK.NSEW)
			objFrame.grid()

			# Get label dimensions
			self.lbMessage["text"] = self.strMessage
			self.lbMessage.update()
			self.ilbW = self.lbMessage.winfo_width()
			self.ilbH = self.lbMessage.winfo_height()
		# End of if

		# Get widget position
		self.objWidget.update()
		x = self.objWidget.winfo_rootx()
		y = self.objWidget.winfo_rooty()

		# Calculate tooltip position
		if self.strPosition == "top-left":
			y -= self.ilbH
		elif self.strPosition == "top-right":
			x += self.objWidget.winfo_width()
		elif self.strPosition == "bottom-left":
			y += self.objWidget.winfo_height()
		elif self.strPosition == "bottom-right":
			x += self.objWidget.winfo_width()
			y += self.objWidget.winfo_height()
		# End of if

		# Prevent going beyond screen
		if (y < 0):
			y = self.objWidget.winfo_height()
		elif (y + self.ilbH + 10) > self.iScrH:
			y = self.iScrH - self.objWidget.winfo_height() - self.ilbH - 10
		# End of if
		if (x + self.ilbW + 10) > self.iScrW:
			x = self.iScrW - self.ilbW - 10
			if self.strPosition == "top-right":
				y += self.objWidget.winfo_height()
			# End of if
		# End of if

		self.objToolTipWin.wm_geometry("+%d+%d" % (x, y))
		self.objToolTipWin.deiconify()
		self.IsShowing = True

		# Add timeout
		self.objToolTipWin.after(self.iTimeout, self.CloseTip)
	# End of ShowTip()
# End of class clTooltip

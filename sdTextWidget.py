#
# Completed ??-July-2024
#

import threading as objLibThreading
from tkinter import StringVar as objLibStringVar
from tkinter import Text as objLibText
from re import compile as objRECompile
import sdTooltip as objLibTooltip
import inspect

class clTextWidget:
	def __init__(self, value="", state="normal", font="", fg="black", bg="white", dfg="black", dbg="#DCDAD5",
				 errfg="black", errbg="#FF9B9B", maxChars=-1, charsAllowed=".*", emptyAllowed="yes", tooltip="",
				 callback=None, callbackargs=None, iMin=-1, iMax=-1, bTriggerCallback=True):
		# Save parameters
		self.value = value
		self.state = state
		self.font= font
		self.fg = fg
		self.bg = bg
		self.dfg = dfg
		self.dbg = dbg
		self.errfg = errfg
		self.errbg = errbg
		self.iMaxChars = maxChars
		strAllowed = "".join(["^", charsAllowed, "$"])
		self.charsAllowed = objRECompile(strAllowed)
		self.emptyAllowed = emptyAllowed.lower()
		self.tooltip = tooltip
		self.objCallback = callback
		self.tpCallbackArgs = callbackargs
		self.iMin = iMin
		self.iMax = iMax
		self.bTriggerCallback = bTriggerCallback

		self.status = ["", ""]
	# End of __init__()

	def Display(self, master, x=0, y=0, w=40, h=20):
		# Create
		self.Widget = objLibText(master)
		self.Widget.place(x=x, y=y, width=w, height=h)
		self.Widget.tag_configure("WidgetText", justify="center")
		self.Widget.tag_add("WidgetText", "1.0", "end")
		self.WidgetTT = objLibTooltip.clTooltip(self.Widget, strMessage=self.tooltip)

		# Configure
		self.Widget.configure(foreground=self.fg, background=self.bg,)
		if len(self.font) != 0:
			self.Widget.configure(font=self.font)
		# End of if
		self.Widget.insert("1.0", self.value)
		self.Widget["state"] = self.state
		self.Widget.bind("<KeyRelease>", self.HandlerValidate)
	# End of Display()

	def HandlerValidate(self, objEvent, iType=0, strValue=""):
		self.status[0] = ""
		self.status[1] = ""
		cFg = self.errfg
		cBg = self.errbg
		cDFg = self.errfg
		cDBg = self.errbg
		objThread = None

		for x in range(1):
			iLen = len(strValue)

			# Check for maximum characters
			if (self.iMaxChars != -1) and (iLen > self.iMaxChars):
				self.status[0] = "Fatal"
				self.status[1] = " ".join(["Maximum allowed is", str(self.iMaxChars), "characters"])
				break
			# End of if

			if iLen == 0:
				if self.emptyAllowed != "yes":
					self.status[0] = "Warning"
					self.status[1] = "Empty value is not valid"
					break
				# End of if
			else:
				# Check for allowed characters
				objResult = self.charsAllowed.search(strValue)
				if not objResult:
					self.status[0] = "Fatal"
					self.status[1] = "".join(["Character \"", strValue[-1:], "\" is not allowed"])
					break
				# End of if
				
				# Check for minimum
				try:
					iValue = int(strValue)
				except:
					iValue = 0
				# End of if
				if (self.iMin != -1) and (iValue < self.iMin):
					self.status[0] = "Fatal"
					self.status[1] = "".join(["Value should not be less than ", str(self.iMin)])
					break
					# End of if
				# End of if
				
				# Check for maximum
				if (self.iMax != -1) and (iValue > self.iMax):
					self.status[0] = "Fatal"
					self.status[1] = "".join(["Value should not be greater than ", str(self.iMax)])
					break
					# End of if
				# End of if				
			# End of if

			cFg = self.fg
			cBg = self.bg
			cDFg = self.dfg
			cDBg = self.dbg

			# Initialise callback function
			if not self.bTriggerCallback:
				break
			# End of if

			if self.objCallback != None:
				if self.tpCallbackArgs != None:
					arrArgs = list(self.tpCallbackArgs)
					arrArgs.insert(0, str(strValue))
					tpArgs = tuple(arrArgs)
				else:
					tpArgs = tuple([str(strValue)])
				# End of if

				objThread = objLibThreading.Thread(target=self.objCallback, args=tpArgs)
			# End of if
		# End of for loop

		# Set widget colours and tooltip
		self.Widget.configure(foreground=cFg, background=cBg)
		self.WidgetTT.SetMessage(self.status[1])

		# Callback function
		if objThread is not None:
			objThread.start()
		# End of if

		# Determine return value
		if self.status[0] == "Fatal":
			return False
		else:
			return True
		# End of if
	# End of HandlerValidate()

	def GetBg(self):
		return self.Widget["background"]
	# End of GetBg()

	def GetSize(self):
		arrSize = [0, 0]
		arrSize[0] = self.Widget.winfo_reqwidth()
		arrSize[1] = self.Widget.winfo_reqheight()

		return arrSize
	# End of GetSize()

	def GetState(self):
		return self.Widget["state"]
	# End of GetState()

	def GetStatus(self):
		iStatus = 0
		for x in range(1):
			# Check if empty values is allowed
			if self.emptyAllowed == "no":
				if self.Widget.get("1.0", "END") == "":
					iStatus = 1
					self.status[0] = "Warning"
					self.WidgetTT.SetMessage("Empty value is not valid")
					self.SetBg(self.errbg)
					break
				# End of if
			# End of if

			if self.status[0] == "Fatal":
				iStatus = -1
			elif self.status[0] == "Warning":
				iStatus = 1
			# End of if
		# End of for loop

		return iStatus
	# End of GetStatus()

	def GetValue(self):
		return self.Widget.get("1.0", "END")
	# End of Get()

	def Reset(self):
		self.Widget.configure(foreground=self.fg, background=self.bg)
		self.Widget.delete("1.0", self.value)
		self.Widget.insert("1.0", self.value)
		self.Widget["state"] = self.state
		self.WidgetTT.SetMessage(self.tooltip)
	# End of Reset()

	def SetBg(self, strValue):
		self.Widget.configure(background=strValue)		
	# End of SetBg()

	def SetCallbackTrigger(self, bTriggerCallback):
		self.bTriggerCallback = bTriggerCallback
	# End of SetCallbackTrigger()

	def SetFg(self, strValue):
		self.Widget.configure(foreground=strValue)
	# End of SetFg()

	def SetFont(self, strValue):
		self.Widget.configure(font=strValue)
		self.font = strValue
	# End of SetFg()

	def SetFocus(self):
		self.Widget.focus()
	# End of SetFocus()
	
	def SetMax(self, iMax):
		self.iMax = iMax
	# End of SetMax()

	def SetMaxChars(self, iMaxChars):
		self.iMaxChars = iMaxChars
	# End of SetMaxChars()

	def SetMin(self, iMin):
		self.iMin = iMin
	# End of SetMin()

	def SetRegEx(self, strRegEx):
		strRegEx = "".join(["^", strRegEx, "$"])
		self.charsAllowed = objRECompile(strRegEx)
	# End of SetRegEx()

	def SetState(self, strState):
		self.Widget["state"] = strState

		# Set widget backgound colour
		if strState == "disabled":
			self.Widget.configure(disabledbackground=self.dbg)
		else:
			self.Widget.configure(background=self.bg)
		# End of if
	# End of Get()

	def SetStatus(self, strState, strTooltip):
		self.status[0] = strState
		self.status[1] = strTooltip
		self.WidgetTT.SetMessage(strTooltip)
	# End of Get()

	def SetTooltip(self, strMsg):
		self.WidgetTT.SetMessage(strMsg)
	# End of SetTooltip()

	def SetValue(self, strValue):
		self.Widget.delete("1.0", self.value)
		self.Widget.insert("1.0", self.value)
	# End of Set()
# End of class clTextWidget

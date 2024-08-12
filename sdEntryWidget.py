#
# Completed 20-December-2021
#
# Fix 		  : 09-Jan-2022 : 1. Fixed validation where empty was not allowed though the flag was set
#					 	 	  2. Added functions SetRegEx(), SetMin(), SetMax()
#							  3. Added "iMin" and "iMax" parameters
# Enhancement : 06-Feb-2022 : 1. Added function "GetState()" and "SetCallbackTrigger()"
#							  2. Added flag "bTriggerCallback"
#
# Enhancement : 13-Jul-2024 : 1. Added support to change "font" of entry widget
#							  2. Added function to get size of widget "GetSize()"
#							  3. Added functions "SetMaxChars()", "GetBg()", "GetPlaceInfo()", "Forget()", "Place()", "GetName()", "SetName()", "Bind()"
#
# Fix /		  : 12-Aug-2024 : 1. Changed method of setting value in the widget from "vWidget.set" to "Wiget.insert()" and added code to disable / enable validation
# Enhancement				  2. Added function "SetValueDisabled()", "SetOption()", "SetBackground()"
#							  3. Changed functions "GetBg()" and "SetBg()" to "GetOption()"
#							  4. Modified "SetStatus()" to take status value and set background colour
#							  5. Modified logic in functions
#							  6. Changed code in "_HandlerValidate()" to return "Warning" when iMin and iMax do not match as it allows user to continue typing
#

import threading as objLibThreading
import tkinter as objLibTk
from tkinter import StringVar as objLibStringVar
from tkinter import Entry as objLibEntry
from re import compile as objRECompile
import sdTooltip as objLibTooltip
import inspect

class clEntryWidget:
	def __init__(self, strValue, strState, strFont, maxChars, charsAllowed, emptyAllowed, tooltip, callback, callbackargs, iMin, iMax, bTriggerCallback, dictColours):
		# Save parameters
		self.strValue = strValue
		self.strState = strState
		self.strFont= strFont
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
		self.dictColours = dictColours

		self.arrStatus = ["", "", 0] # Field [2] : It will be ("1") if user has set the error. Else it will be ("0")
		self.strName = ""
	# End of __init__()

	def Display(self, objMaster, iX, iY, iW, iH, justify="left"):
		# Create
		self.vWidget = objLibStringVar()
		self.Widget = objLibEntry(objMaster, justify=justify, textvariable=self.vWidget, validate="key", foreground=self.dictColours["fg"],
								  background=self.dictColours["bg"], disabledforeground=self.dictColours["dfg"],
								  disabledbackground=self.dictColours["dbg"], font=self.strFont)

		if (iW != -1) and (iH != -1):
			self.Widget.place(x=iX, y=iY, width=iW, height=iH)
		elif (iW == -1) and (iH == -1):
			self.Widget.place(x=iX, y=iY)
		elif iW == -1:
			self.Widget.place(x=iX, y=iY, height=iH)
		elif iH == -1:
			self.Widget.place(x=iX, y=iY, width=iW)
		# End of if
		self.WidgetTT = objLibTooltip.clTooltip(self.Widget, strMessage=self.tooltip)

		# Configure
		self.Widget.insert(0, self.strValue)
		self.Widget["state"] = self.strState
		self.Widget["validatecommand"] = (self.Widget.register(self._HandlerValidate), "%d", "%P")
	# End of Display()

	def _HandlerValidate(self, iType, strValue):
		self.arrStatus[0] = ""
		self.arrStatus[1] = ""
		cFg = self.dictColours["errfg"]
		cBg = self.dictColours["errbg"]
		cDFg = self.dictColours["errfg"]
		cDBg = self.dictColours["errbg"]
		objThread = None

		for x in range(1):
			iLen = len(strValue)

			# Check for maximum characters
			if (self.iMaxChars != -1) and (iLen > self.iMaxChars):
				self.arrStatus[0] = "Fatal"
				self.arrStatus[1] = " ".join(["Maximum allowed is", str(self.iMaxChars), "characters"])
				break
			# End of if

			if iLen == 0:
				if self.emptyAllowed != "yes":
					self.arrStatus[0] = "Warning"
					self.arrStatus[1] = "Empty value is not valid"
					break
				# End of if
			else:
				# Check for allowed characters
				objResult = self.charsAllowed.search(strValue)
				if not objResult:
					self.arrStatus[0] = "Fatal"
					self.arrStatus[1] = "".join(["Character \"", strValue[-1:], "\" is not allowed"])
					break
				# End of if

				# Check for minimum
				try:
					iValue = int(strValue)
				except:
					iValue = 0
				# End of if
				if (self.iMin != -1) and (iValue < self.iMin):
					self.arrStatus[0] = "Warning"
					self.arrStatus[1] = "".join(["Value should not be less than ", str(self.iMin)])
					break
					# End of if
				# End of if

				# Check for maximum
				if (self.iMax != -1) and (iValue > self.iMax):
					self.arrStatus[0] = "Warning"
					self.arrStatus[1] = "".join(["Value should not be greater than ", str(self.iMax)])
					break
					# End of if
				# End of if
			# End of if

			cFg = self.dictColours["fg"]
			cBg = self.dictColours["bg"]
			cDFg = self.dictColours["dfg"]
			cDBg = self.dictColours["dbg"]

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
		self.Widget.configure(foreground=cFg, background=cBg, disabledforeground=cDFg, disabledbackground=cDBg)
		self.WidgetTT.SetMessage(self.arrStatus[1])

		# Callback function
		if objThread is not None:
			objThread.start()
		# End of if

		# Determine return value
		if self.arrStatus[0] == "Fatal":
			return False
		else:
			return True
		# End of if
	# End of _HandlerValidate()

	def Bind(self, strEvent, objEventHandler):
		self.Widget.bind(strEvent, objEventHandler)
	# End of Bind()

	def Forget(self):
		self.Widget.place_forget()
	# End of Forget()

	def GetName(self):
		return self.strName
	# End of GetName()

	def GetOption(self, strOption):
		return self.Widget[strOption]
	# End of GetOption()

	def GetPlaceInfo(self):
		return self.Widget.place_info()
	# End of GetPlaceInfo()

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
		match self.arrStatus[0]:
			case "Fatal":
				iStatus = -1
			# End of case

			case "Warning":
				iStatus = 1
			# End of case
		# End of match

		return iStatus
	# End of GetStatus()

	def GetValue(self):
		return self.vWidget.get()
	# End of GetValue()

	def Place(self, dictPlaceInfo):
		self.Widget.place(dictPlaceInfo)
	# End of Place()

	def Reset(self):
		self.Widget.configure(foreground=self.dictColours["fg"], background=self.dictColours["bg"], disabledforeground=self.dictColours["dfg"], disabledbackground=self.dictColours["dbg"])
		self.Widget.config(validate="none")
		self.Widget.delete(0, objLibTk.END)
		self.Widget.insert(0, self.strValue)
		self.Widget.config(validate="key")
		self.Widget["state"] = self.strState
		self.WidgetTT.SetMessage(self.tooltip)
	# End of Reset()

	def SetBackground(self, strType):
		strState = self.Widget["state"]

		match strType:
			case "Normal":
				if strState.find("normal") == 0:
					self.Widget.configure(background=self.dictColours["bg"])
				else:
					self.Widget.configure(background=self.dictColours["dbg"])
				# End of if
			# End of case

			case "Error":
				self.Widget.configure(background=self.dictColours["errbg"])
			# End of case
		# End of match
	# End of SetBackground()

	def SetCallbackTrigger(self, bTriggerCallback):
		self.bTriggerCallback = bTriggerCallback
	# End of SetCallbackTrigger()

	def SetFont(self, strValue):
		self.Widget.configure(font=strValue)
		self.strFont = strValue
	# End of SetFont()

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

	def SetName(self, strName):
		self.strName = strName
	# End of SetName()

	def SetOption(self, strOption, strValue):
		self.Widget[strOption] = strValue
	# End of SetOption()

	def SetRegEx(self, strRegEx):
		strRegEx = "".join(["^", strRegEx, "$"])
		self.charsAllowed = objRECompile(strRegEx)
	# End of SetRegEx()

	def SetState(self, strState):
		self.Widget["state"] = strState

		# Set widget backgound colour
		if strState == "disabled":
			self.Widget.configure(disabledbackground=self.dictColours["dbg"])
		else:
			self.Widget.configure(background=self.dictColours["bg"])
		# End of if
	# End of SetState()

	def SetStatus(self, iState=0, strState="", strTooltip=""):
		for x in range(1):
			match iState:
				case 0:
					# User likes to reset error
					if self.GetStatus() != 0:
						if self.arrStatus[2] == 0:
							# Ignore if it is non-user set error
							break
						# End of if

						# Reset error
						self.arrStatus[0] = ""
						self.arrStatus[1] = ""
						self.arrStatus[2] = 0
						self.WidgetTT.SetMessage("")
						self.SetBackground("Normal")
					# End of if
				# End of case

				case 1|-1:
					# User likes to set error
					if self.GetStatus() != 0:
						# Ignore if there is already an error
						break
					# End of if

					# Set error
					self.arrStatus[0] = strState
					self.arrStatus[1] = strTooltip
					self.arrStatus[2] = 1
					self.WidgetTT.SetMessage(strTooltip)
					self.SetBackground("Error")
				# End of case
			# End of match
		# End of for loop
	# End of SetStatus()

	def SetTooltip(self, strMsg):
		self.WidgetTT.SetMessage(strMsg)
	# End of SetTooltip()

	def SetValue(self, strValue, bValidate=False):
		if bValidate:
			self.Widget.config(validate="none")
			self.Widget.delete(0, objLibTk.END)
			self.Widget.config(validate="key")
			self.Widget.insert(0, strValue)
		else:
			self.Widget.config(validate="none")
			self.Widget.delete(0, objLibTk.END)
			self.Widget.insert(0, strValue)
			self.Widget.config(validate="key")
		# End of if
	# End of SetValue()

	def SetValueDisabled(self, strValue):
		self.Widget.config(validate="none")
		self.Widget["state"] = "normal"
		self.Widget.delete(0, objLibTk.END)
		self.Widget.insert(0, strValue)
		self.Widget["state"] = "disabled"
		self.Widget.config(validate="key")
	# End of SetValueDisabled()
# End of class clEntryWidget

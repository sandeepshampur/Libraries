#
# Completed : 25-February-2022
#
# Fix 		  : 09-Mar-2022 : Added code in "SetProgress" to keep progress between 0% and  100%
# Enhancement : 01-Oct-2024 : Revamped logic
#

import tkinter as objLibTK
from tkinter import ttk as objLibTTK

class clProgressBar:
	def __init__(self, arrFont, dictColours, objCommon):
		'''
		dictColours = {
			"cTrough": "#d9d9d9",
			"cBar": "#d85f2c",
			"cLabel": "black",
			"cBorder": "black"
		}
		'''
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objCommon = objCommon
		self.iProgress = 0
	# End of __init__()

	def Display(self, objWidget, iX, iY, iW, iH, objParentWindow):
		# Colour setting
		# https://stackoverflow.com/questions/13510882/how-to-change-ttk-progressbar-color-in-python
		# Label
		# https://stackoverflow.com/questions/47896881/progressbar-with-percentage-label

		iLabelSize = int(iH * 0.55)
		tLabelFont = (self.arrFont[0], iLabelSize, self.arrFont[2])

		self.objProgressBarStyle = objLibTTK.Style(objParentWindow)
		self.objProgressBarStyle.layout("text.Horizontal.TProgressbar",
						  [("Horizontal.Progressbar.trough", {"children": [("Horizontal.Progressbar.pbar", {"side": "left", "sticky": "ns"})],
									"sticky": "nswe"}), ("Horizontal.Progressbar.label", {"sticky": "nswe"})])

		self.objProgressBarStyle.configure("text.Horizontal.TProgressbar", text="0%", anchor="center", font=tLabelFont, foreground=self.dictColours["cLabel"],
				troughcolor=self.dictColours["cTrough"], bordercolor=self.dictColours["cBorder"],
				background=self.dictColours["cBar"], lightcolor=self.dictColours["cBar"], darkcolor=self.dictColours["cBar"])

		self.objProgressBar = objLibTTK.Progressbar(objWidget, style="text.Horizontal.TProgressbar", maximum=100.01)
		self.objProgressBar.place(x=iX, y=iY, width=iW, height=iH)
	# End of Display()

	def Decrement(self, iValue):
		if (self.iProgress - iValue) < 0:
			iStepValue = self.iProgress * -1
			self.iProgress = 0
			iLabelValue = 0
		else:
			iStepValue = iValue * -1
			self.iProgress -= iValue
			iLabelValue = self.iProgress
		# End of if

		self._UpdateProgressBar(iStepValue, iLabelValue)
	# End of Decrement()

	def Increment(self, iValue):
		if (self.iProgress + iValue) > 100:
			iStepValue = 100 - self.iProgress
			self.iProgress = 100
			iLabelValue = 100
		else:
			iStepValue = iValue
			self.iProgress += iValue
			iLabelValue = self.iProgress
		# End of if

		self._UpdateProgressBar(iStepValue, iLabelValue)
	# End of Increment()

	def SetValue(self, iValue):
		for x in range(1):
			if iValue < 0:
				iStepValue = self.iProgress * -1
				self.iProgress = 0
				iLabelValue = 0
				break
			# End of if

			if iValue > 100:
				iStepValue = 100 - self.iProgress
				self.iProgress = 100
				iLabelValue = 100
				break
			# End of if

			iStepValue = iValue - self.iProgress
			self.iProgress = iValue
			iLabelValue = iValue
		# End of for loop

		self._UpdateProgressBar(iStepValue, iLabelValue)
	# End of SetProgress()

	def _UpdateProgressBar(self, iStepValue, iLabelValue):
		self.objProgressBar.step(iStepValue)
		strLabelValue = "".join([str(iLabelValue), "%"])
		self.objProgressBarStyle.configure("text.Horizontal.TProgressbar", text=strLabelValue)
	# End of _UpdateProgressBar()
# End of class clProgressBar

#
# Completed : 25-February-2022
#
# Fix : 09-Mar-2022 : Added code in "SetProgress" to keep progress between 0% and  100%
#

#********************************************************************************************
# Imports
#********************************************************************************************
import tkinter as objLibTK
from tkinter import ttk as objLibTTK

class clProgressBar:
	def __init__(self, objParentWindow, colourBg="black"):
		self.objParentWindow = objParentWindow
		self.colourBg = colourBg
	# End of __init__()

	def Display(self, objMaster, iX, iY, iW, iH, iMax=100, strMode="determinate"):
		self.objStyle = objLibTTK.Style(self.objParentWindow)
		self.objStyle.theme_use("clam")

		# Progress bar style
		# https://stackoverflow.com/questions/47896881/progressbar-with-percentage-label
		self.objStyle.layout("textProgressbar", [("Horizontal.Progressbar.trough", {"children": [("Horizontal.Progressbar.pbar", {"side": "left", "sticky": "ns"})], "sticky": "nswe"}), ("Horizontal.Progressbar.label", {"sticky": "nswe"})])
		self.objStyle.configure("textProgressbar", text="0 %", anchor="center", foreground="black", background="#18D122", bordercolor=self.colourBg, lightcolor=self.colourBg, darkcolor=self.colourBg)

		self.strPBStyle = "PB.textProgressbar"
		self.objStyle.configure(self.strPBStyle, "textProgressbar")
		self.vPB = objLibTK.StringVar(self.objParentWindow)
		objPB = objLibTTK.Progressbar(objMaster, variable=self.vPB, maximum=iMax, mode=strMode, style=self.strPBStyle)
		objPB.place(x=iX, y=iY, width=iW, height=iH)
	# End of Display()

	def SetProgress(self, iPercent):
		if iPercent < 0:
			iPercent = 0
		elif iPercent > 100:
			iPercent = 100
		# End of if

		self.vPB.set(iPercent)
		strPercent = "".join([str(iPercent), "%"])
		self.objStyle.configure(self.strPBStyle, text=strPercent)
	# End of SetProgress()
# End of class clProgressBar

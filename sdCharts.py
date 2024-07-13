#
# Started   : 01-July-2024
# Completed : 04-July-2024
#
# Fix 		  : 08-Jul-2024 : 1. Fixed divide by zero in FormatLabels()
#							  2. Added code in clPieChart.Plot() to display error message if chart values are all zero
#

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as objLibMLFigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk as objLibMLNavigationToolbar2Tk
from matplotlib.figure import Figure as objLibMLFigure
import matplotlib.pyplot as objLibPyplot
import numpy as objLibNumpy
import tkinter as objLibTK

class clCharts:
	def __init__(self):
		# Class instances
		self.objPieChart = clPieChart()
		self.objBarChart = clBarChart()
	# End of __init__()

	def BarChart(self, objParentWindow, arrChartValues, arrChartLabels, tupleChartSize=(10, 5), strWindowTitle="", strChartTitle="", iColour="#4285f4"):
		# Format labels
		arrChartLabels = self.FormatLabels(arrChartValues, arrChartLabels, False, True)

		self.objBarChart.Plot(objParentWindow, arrChartValues, arrChartLabels, tupleChartSize, strWindowTitle, strChartTitle, iColour)
	# End of BarChart()

	def PieChart(self, objParentWindow, arrChartValues, arrChartLabels, tupleChartSize=(12, 6), strWindowTitle="", strChartTitle=""):
		# Format labels
		arrChartLabels = self.FormatLabels(arrChartValues, arrChartLabels)

		self.objPieChart.Plot(objParentWindow, arrChartValues, arrChartLabels, tupleChartSize, strWindowTitle, strChartTitle)
	# End of PieChart()

	def FormatLabels(self, arrChartValues, arrChartLabels, bValue=True, bPercent=True):
		for x in range(1):
			if not bValue and not bPercent:
				arrFormattedLabels = arrChartLabels
				break
			# End of if

			iSum = sum(arrChartValues)

			arrFormattedLabels = []
			for iIndex in range(len(arrChartLabels)):
				if iSum != 0:
					fPercent = arrChartValues[iIndex] * 100 / iSum
				else:
					fPercent = 0.0
				# End of if
				fPercent = round(int(fPercent), 0)

				if bValue and bPercent:
					strNewLabel = "".join([str(arrChartLabels[iIndex]), " (", str(arrChartValues[iIndex]), "; ", str(fPercent), "%)"])
				elif bValue and not bPercent:
					strNewLabel = "".join([str(arrChartLabels[iIndex]), " (", str(arrChartValues[iIndex]), ")"])
				elif not bValue and bPercent:
					strNewLabel = "".join([str(arrChartLabels[iIndex]), " (", str(fPercent), "%)"])
				# End of if

				arrFormattedLabels.append(strNewLabel)
			# End of for loop
		return arrFormattedLabels
	# End of FormatLabels()
# End of class clCharts

class clBarChart:
	def __init__(self):
		pass
	# End of __init__()

	def Plot(self, objParentWindow, arrChartValues, arrChartLabels, tupleChartSize=(10, 5), strWindowTitle="", strChartTitle="", iColour="#4285f4"):
		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.wm_title(strWindowTitle)
		self.objWindow = objWindow

		# ----------------------- Create plot -------------------------------
		objLibPyplot.figure(figsize=tupleChartSize)
		objLibPyplot.bar(arrChartLabels, arrChartValues, color=iColour)
		objLibPyplot.xticks(rotation=30, ha='right')
		objLibPyplot.subplots_adjust(bottom=0.2)
		objLibPyplot.title(strChartTitle)

		# Add values at top of bars
		for iIndex in range(len(arrChartLabels)):
			objLibPyplot.text(iIndex, arrChartValues[iIndex], arrChartValues[iIndex], ha="center")
		# End of for loop

		# ----------------------- Canvas -------------------------------
		objChartCanvas = objLibMLFigureCanvasTkAgg(objLibPyplot.gcf(), master=objWindow)
		objChartCanvas.draw()

		# matplotlib toolbar
		toolbar = objLibMLNavigationToolbar2Tk(objChartCanvas, objWindow, pack_toolbar=False)
		toolbar.update()

		objButton = objLibTK.Button(master=objWindow, text="Exit", command=objWindow.destroy)
		objWindow.bind("<Escape>", lambda _: objWindow.destroy())

		objButton.pack(side=objLibTK.BOTTOM)
		toolbar.pack(side=objLibTK.BOTTOM, fill=objLibTK.X)
		objChartCanvas.get_tk_widget().pack(side=objLibTK.TOP, fill=objLibTK.BOTH, expand=True)
	# End of Plot()

	def KeyPress(self, objEvent):
		strKey = str(objEvent.key)
		if strKey.find("escape") == 0:
			self.objWindow.destroy()
		# End of if
	# End of KeyPress()
# End of class clBarChart

class clPieChart:
	def __init__(self):
		pass
	# End of __init__()

	def Plot(self, objParentWindow, arrChartValues, arrChartLabels, tupleChartSize=(12, 6), strWindowTitle="", strChartTitle=""):
		objWindow = objLibTK.Toplevel(objParentWindow)
		objWindow.wm_title(strWindowTitle)
		self.objWindow = objWindow

		# Display error if chart values have negative numbers
		bNegative = False
		for iValue in arrChartValues:
			if iValue < 0:
				bNegative = True
				break
			# End of if
		# End of for loop
		if bNegative:
			strMsg = "The chart values contains negative numbers!\nPie chart cannot be plotted."
			lbDesc = objLibTK.Label(master=objWindow, text=strMsg, width=50, height=20, anchor="center")
			lbDesc.pack(side=objLibTK.BOTTOM)

			objWindow.bind("<Escape>", lambda _: objWindow.destroy())
			return
		# End of if

		iSum = sum(arrChartValues)
		if iSum == 0:
			strMsg = "All chart values are zero!\nPie chart cannot be plotted."
			lbDesc = objLibTK.Label(master=objWindow, text=strMsg, width=50, height=20, anchor="center")
			lbDesc.pack(side=objLibTK.BOTTOM)

			objWindow.bind("<Escape>", lambda _: objWindow.destroy())
			return
		# End of if

		# ----------------------- Create plot -------------------------------
		objChartFigure = objLibMLFigure(figsize=tupleChartSize)
		objChartAxes = objChartFigure.add_subplot()
		arrChartWedges, _ = objChartAxes.pie(arrChartValues, labeldistance=1.2, startangle=45)
		objChartFigure.subplots_adjust(left=0.1, right=0.5, bottom=0.1, top=0.8, wspace=0.0, hspace=0.0)

		# Add callouts
		dictBbox = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
		dictKW = dict(arrowprops=dict(arrowstyle="-"), bbox=dictBbox, zorder=0, va="center")
		for iIndex, objChartWedge in enumerate(arrChartWedges):
			fAngle = (objChartWedge.theta2 - objChartWedge.theta1) / 2.0 + objChartWedge.theta1
			fYCoord = objLibNumpy.sin(objLibNumpy.deg2rad(fAngle))
			fXCoord = objLibNumpy.cos(objLibNumpy.deg2rad(fAngle))

			# Determine position of label (right or left)
			strHorizontalAlignment = {-1: "right", 1: "left"}[int(objLibNumpy.sign(fXCoord))]

			# Determine label and chart connection style
			strConnectionStyle = f"angle,angleA=0,angleB={fAngle}"

			dictKW["arrowprops"].update({"connectionstyle": strConnectionStyle})
			objChartAxes.annotate(arrChartLabels[iIndex], xy=(fXCoord, fYCoord), xytext=(	1.35 * objLibNumpy.sign(fXCoord), 1.4 * fYCoord), horizontalalignment=strHorizontalAlignment, **dictKW)
		# End of for loop

		objChartAxes.set_title(strChartTitle)
		strLegendLoc = "center right"
		objChartAxes.legend(arrChartWedges, arrChartLabels, loc=strLegendLoc, bbox_to_anchor=(2.2, 0.5))

		# ----------------------- Canvas -------------------------------

		objChartCanvas = objLibMLFigureCanvasTkAgg(objChartFigure, master=objWindow)
		objChartCanvas.draw()

		# matplotlib toolbar
		toolbar = objLibMLNavigationToolbar2Tk(objChartCanvas, objWindow, pack_toolbar=False)
		toolbar.update()

		objButton = objLibTK.Button(master=objWindow, text="Exit", command=objWindow.destroy)
		objWindow.bind("<Escape>", lambda _: objWindow.destroy())

		objButton.pack(side=objLibTK.BOTTOM)
		toolbar.pack(side=objLibTK.BOTTOM, fill=objLibTK.X)
		objChartCanvas.get_tk_widget().pack(side=objLibTK.TOP, fill=objLibTK.BOTH, expand=True)
	# End of Plot()

	def KeyPress(self, objEvent):
		strKey = str(objEvent.key)
		if strKey.find("escape") == 0:
			self.objWindow.destroy()
		# End of if
	# End of KeyPress()
# End of class clPieChart

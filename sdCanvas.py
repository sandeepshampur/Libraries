#
# Created:	 13-January-2022
#
# Enhancement : 15-Feb-2022 : 1. Add parameter "iImgID" to function Clear()
#							  2. Added functions Bind(), AddTooltip(), Show() and Hide()
# 							  3. Added parameters iW and iH to function CreateCanvas()
#							  5. Add parameter "strTooltip" to function AddImage()
#
# Fix 		  :	16-Oct-2023 : Changed deprecated function "ANTIALIAS" with "LANCZOS"
# Fix		  : 21-Jul-2024 : 1. Fixed code in CreateImage() where size was calculated wrongly when both width and height were -1
#							  2. Added function ResizeImage()
# Enhancement : 13-Aug-2024 : Added "objCommon" as parameter
# Enhancement : 24-Sep-2024 : Revamped code

from PIL import Image as objLibImage
from PIL import ImageTk as objLibImageTk
from re import sub as objLibRESub
import threading as objLibThreading
import tkinter as objLibTK

class clCanvas:
	def __init__(self, objCommon, objLoggerLog):
		self.objCommon = objCommon
		self.objLoggerLog = objLoggerLog

		self.dictInfo = {
			"Bind": {
				"Callback": None,
				"Params": ()
			},
			"Canvas": {
				"Height": -1,
				"PlaceInfo": None,
				"Width": -1
			},
			"ImageIDs": {},
			"Tooltip": ""
		}

		self.dictWidgets = {
			"Canvas": None,
			"Images": {},
			"Tooltip": None
		}
	# End of __init__()

	def AddImage(self, strImgPath, iX=0, iY=0, iW=-1, iH=-1, strImgName="", bIgnoreDuplicate=True):
		for x in range(1):
			if strImgName in self.dictInfo["ImageIDs"]:
				if bIgnoreDuplicate:
					if self.objLoggerLog is not None:
						self.objLoggerLog("Image name already exists. Ignoring as per flag.", strImgName)
					# End of if
					break
				else:
					if self.objLoggerLog is not None:
						self.objLoggerLog("WARNING: Image name already exists. Image is replaced!", strImgName)
					# End of if
				# End of if
			# End of if

			# Load image
			objImg = self.CreateImage(strImgPath, iW, iH)

			# Add image
			objCanvas = self.dictWidgets["Canvas"]
			iImgID = objCanvas.create_image(iX, iY, anchor=objLibTK.NW, image=objImg)

			# Image name
			if len(strImgName) == 0:
				strImgName = "".join(["Img-", str(iImgID)])
			# End of if

			self.dictInfo["ImageIDs"][strImgName] = iImgID
			self.dictWidgets["Images"][iImgID] = objImg
		# End of for loop
	# End of AddImage()

	def Bind(self, strKey, objCallback, tParam=(), bIgnoreEvent=False):
		self.bIgnoreEvent = bIgnoreEvent
		objCanvas = self.dictWidgets["Canvas"]
		objCanvas.bind(strKey, self.HandlerBind)

		self.dictInfo["Bind"]["Callback"] = objCallback
		self.dictInfo["Bind"]["Params"] = tParam
	# End of Bind()

	def ChangeImageVisibility(self, arrImgNames=[], strState="hidden"):
		'''
		strState = "hidden"|"normal"
		'''
		# Get image IDs from image names
		arrIDs = []
		if len(arrImgNames) == 0:
			arrIDs = list(self.dictInfo["ImageIDs"].values())
		else:
			for strImgName in arrImgNames:
				arrIDs.append(self.dictInfo["ImageIDs"][strImgName])
			# End of for loop
		# End of if

		# Hide images
		objCanvas = self.dictWidgets["Canvas"]
		for iImgID in arrIDs:
			objCanvas.itemconfigure(iImgID, state=strState)
		# End of for loop
	# End of HideImage()

	def ConfigureTooltip(self, strMessage="", strPosition=""):
		for x in range(1):
			objTooltip = self.dictWidgets["Tooltip"]
			if objTooltip is None:
				# Create tooltip widget
				objCanvas = self.dictWidgets["Canvas"]
				if len(strPosition) == 0:
					strPosition = "top-right"
				# End of if

				dictParams = { "objWidget": objCanvas, "strMessage": strMessage, "strPosition": strPosition }
				objTooltip = self.objCommon.GetLibrary("sdTooltip", **dictParams)
				self.dictWidgets["Tooltip"] = objTooltip
				break
			# End of if

			objTooltip.SetMessage(strMessage)

			if len(strPosition) == 0:
				break
			# End of if

			# Set tooltip posistion
			objTooltip.SetTooltipPosition(strPosition)
		# End of for loop
	# End of ConfigureTooltip()

	def CreateCanvas(self, objWindow, iX, iY, iW, iH, colourBg="#d9d9d9"):
		objCanvas = objLibTK.Canvas(objWindow, highlightthickness=0, background=colourBg)
		objCanvas.place(x=iX, y=iY)
		self.dictWidgets["Canvas"] = objCanvas
		self.dictInfo["Canvas"]["PlaceInfo"] = objCanvas.place_info()
		# This helps to resize canvas later
		objCanvas.config(width=iW, height=iH)
		self.dictInfo["Canvas"]["Width"] = iW
		self.dictInfo["Canvas"]["Height"] = iH
	# End of CreateCanvas()

	def CreateCanvasToFitImage(self, objWindow, strImgPath, iCanvasX, iCanvasY, cCanvasBg="#d9d9d9", iImgW=-1, iImgH=-1, strImgName=""):
		self.CreateCanvas(objWindow, iCanvasX, iCanvasY, 1, 1, cCanvasBg)
		self.AddImage(strImgPath, iW=iImgW, iH=iImgH, strImgName=strImgName)

		# Get image dimensions
		objImage = self.dictWidgets["Images"][1]
		iImgW = objImage.width()
		iImgH = objImage.height()

		# Resize canvas
		self.dictWidgets["Canvas"].config(width=iImgW, height=iImgH)
		self.dictInfo["Canvas"]["Width"] = iImgW
		self.dictInfo["Canvas"]["Height"] = iImgH
	# End of CreateCanvasToFitImage()

	def CreateImage(self, strImgPath, iW=-1, iH=-1):
		# Load image
		objImg = objLibImage.open(strImgPath)
		iOriginalImgW = objImg.size[0]
		iOriginalImgH = objImg.size[1]

		# Determine new dimentions as appropriate
		for x in range(1):
			if (iW == -1) and (iH == -1):
				iNewImgW = iOriginalImgW
				iNewImgH = iOriginalImgH
				break
			# End of if

			iNewImgW = iW
			iNewImgH = iH
			if iW == -1:
				iNewImgW = int(iH * iOriginalImgW / iOriginalImgH)
			# End of if

			if iH == -1:
				iNewImgH = int(iW * iOriginalImgH / iOriginalImgW)
			# End of if

			# Resize image
			objImg = objImg.resize((iNewImgW, iNewImgH), objLibImage.LANCZOS)
		# End of for loop
		objImg = objLibImageTk.PhotoImage(objImg)

		return objImg
	# End of GetImage()

	def DeleteImages(self, arrImgNames=[]):
		objCanvas = self.dictWidgets["Canvas"]
		for x in range(1):
			if len(arrImgNames) == 0:
				objCanvas.delete("all")
				self.dictWidgets["Images"].clear()
				self.dictInfo["ImageIDs"].clear()
				break
			# End of if

			# Delete images
			for strImgName in arrImgNames:
				iImgID = self.dictInfo["ImageIDs"][strImgName]
				objCanvas.delete(iImgID)
				self.dictWidgets["Images"].pop(iImgID)
				self.dictInfo["ImageIDs"].pop(strImgName)
			# End of for loop
		# End of for loop
	# End of DeleteImages()

	def GetCanvasDimensions(self):
		iW = self.dictInfo["Canvas"]["Width"]
		iH = self.dictInfo["Canvas"]["Height"]

		return [iW, iH]
	# End of if

	def HandlerBind(self, objEvent):
		objCallback = self.dictInfo["Bind"]["Callback"]
		tParam = self.dictInfo["Bind"]["Params"]

		arrParam = list(tParam)
		if not self.bIgnoreEvent:
			arrParam.insert(0, objEvent)
		# End of if

		objCallback(*arrParam)
	# End of HandlerBind()

	def MoveImage(self, strImgName, iX, iY):
		# Get image ID
		iImgID = self.dictInfo["ImageIDs"][strImgName]

		# Move image
		objCanvas = self.dictWidgets["Canvas"]
		objCanvas.move(iImgID, iX, iY)
	# End of MoveImage()

	def SetBackgroundColour(self, colourBg):
		self.dictWidgets["Canvas"].config(background=colourBg)
	# End of SetBackgroundColour()

	def SetState(self, strState):
		strState = strState.lower()
		match strState:
			case "hide":
				self.dictWidgets["Canvas"].place_forget()
			# End of case

			case "normal":
				dictPlaceInfo = self.dictInfo["Canvas"]["PlaceInfo"]
				self.dictWidgets["Canvas"].place(dictPlaceInfo)
			# End of case
		# End of match
	# End of SetState()
# End of class clCanvas

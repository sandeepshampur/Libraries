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

#********************************************************************************************
# Imports
#********************************************************************************************
from PIL import Image as objLibImage
from PIL import ImageTk as objLibImageTk
from re import sub as objLibRESub
import threading as objLibThreading
import tkinter as objLibTK

class clCanvas:
	def __init__(self, objCommon, objLoggerLog):
		self.objCommon = objCommon
		self.objLoggerLog = objLoggerLog

		self.objCanvas = None
		self.objTooltip = None
		self.objImg = None
		self.iX = -1
		self.iY = -1
		self.iImgW = -1
		self.iImgH = -1
		self.imgID = -1
		self.strTooltip = ""
		self.tpBindArgs = ()
		self.objCallback = None
		self.dictPlaceInfo = None
	# End of __init__()
	
	def AddImage(self, iImgX, iImgY, objImg=None, strTooltip=""):
		if objImg is None:
			self.imgID = self.objCanvas.create_image(iImgX, iImgY, anchor=objLibTK.NW, image=self.objImg)
		else:
			self.imgID = self.objCanvas.create_image(iImgX, iImgY, anchor=objLibTK.NW, image=objImg)
		# End of if

		if len(strTooltip) > 0:
			self.strTooltip = objLibRESub(r"(\w)([A-Z])", r"\1 \2", strTooltip)
		else:
			self.strTooltip = ""
		# End of if

		if self.objTooltip is not None:
			self.objTooltip.SetMessage(self.strTooltip)
		# End of if
		
		return self.imgID
	# End of AddImage()

	def Bind(self, strKey, objCallback=None, tpParam=()):
		self.objCanvas.bind(strKey, lambda _: self.HandlerBind())
		self.objCallback = objCallback
		self.tpBindArgs = tpParam
	# End of Bind()

	def ChangeImage(self, objImg, strTooltip=""):
		if self.objImg is None:
			self.objCanvas.create_image(0, 0, anchor=objLibTK.NW, image=objImg)
		else:
			self.objCanvas.itemconfig(1, image=objImg)
		# End of if
		self.iImgW = objImg.width()
		self.iImgH = objImg.height()
		self.objImg = objImg
		
		if len(strTooltip) > 0:
			self.strTooltip = objLibRESub(r"(\w)([A-Z])", r"\1 \2", strTooltip)
		else:
			self.strTooltip = ""
		# End of if

		if self.objTooltip is not None:
			self.objTooltip.SetMessage(self.strTooltip)
		# End of if
	# End of ChangeImage()

	def ChangeTooltip(self, strTooltip=""):
		self.strTooltip = strTooltip
		if self.objTooltip is not None:
			self.objTooltip.SetMessage(self.strTooltip)
		# End of if
	# End of AddTooltip()

	def Clear(self, iImgID=-1):
		if self.objCanvas is not None:
			if iImgID == -1:
				self.objCanvas.delete("all")
			else:
				self.objCanvas.delete(iImgID)
			# End of if
		# End of if
		
		self.objImg = None
		self.strTooltip = ""
		if self.objTooltip is not None:
			self.objTooltip.SetMessage(self.strTooltip)
		# End of if
	# End of Clear()
	
	def CreateCanvas(self, objWindow, iX, iY, colourBg="white", bTooltip=False, strTooltip="", strTooltipPos="bottom-left", objImg=None, iW=-1, iH=-1):
		self.iX = iX
		self.iY = iY
		if objImg is not None:
			self.iImgW = objImg.width()
			self.iImgH = objImg.height()
			self.objImg = objImg
		# End of if

		if iW == -1:
			iW = self.iImgW
		# End of if
		if iH == -1:
			iH = self.iImgH
		# End of if
		self.objCanvas = objLibTK.Canvas(objWindow, width=iW, height=iH, highlightthickness=0, background=colourBg)
		self.objCanvas.place(x=iX, y=iY)
		self.dictPlaceInfo = self.objCanvas.place_info()
		if self.objImg is not None:
			self.imgID = self.objCanvas.create_image(0, 0, anchor=objLibTK.NW, image=self.objImg)
		else:
			self.imgID = -1
		# End of if

		if bTooltip:
			if len(strTooltip) > 0:
				self.strTooltip = objLibRESub(r"(\w)([A-Z])", r"\1 \2", strTooltip)
			else:
				self.strTooltip = ""
			# End of if

			dictParams = { "objWidget": self.objCanvas, "strMessage": self.strTooltip, "strPosition": strTooltipPos }
			self.objTooltip = self.objCommon.GetLibrary("sdTooltip", **dictParams)
		# End of if
	# End of CreateCanvas()

	def CreateImage(self, strImgPath="", iImgW=-1, iImgH=-1, objImg=None):
		if objImg is None:
			# Open image
			objImg = objLibImage.open(strImgPath)

			# Determine width and height preserving aspect ratio
			for x in range(1):
				if iImgW == -1 and iImgH == -1:
					iImgW = objImg.size[0]
					iImgH = objImg.size[1]
					break
				# End of if

				if iImgW == -1:
					iImgW = int(iImgH * objImg.size[0] / objImg.size[1])
					break
				# End of if

				if iImgH == -1:
					iImgH = int(iImgW * objImg.size[1] / objImg.size[0])
					break
				# End of if
			# End of for loop
			self.iImgW = iImgW
			self.iImgH = iImgH

			objImg = objImg.resize((iImgW, iImgH), objLibImage.LANCZOS)
			self.objImg = objLibImageTk.PhotoImage(objImg)
		else:
			self.iImgW = objImg.width()
			self.iImgH = objImg.height()
			self.objImg = objImg
		# End of if
	# End of CreateImage()

	def GetCoordinates(self, iID):
		return self.objCanvas.coords(iID)
	# End of GetCoordinates()
	
	def GetDimensions(self):
		dictDim = {
			"X": self.iX,			
			"Y": self.iY,
			"Image": self.objImg,
			"Width": self.iImgW,			
			"Height": self.iImgH,
			"imgID": self.imgID,
			"Tooltip": self.strTooltip
		}
		return dictDim
	# End of GetDimensions()

	def HandlerBind(self):
		if self.objCallback is not None:
			objThread = objLibThreading.Thread(target=self.objCallback, args=self.tpBindArgs)
			objThread.start()
		# End of if
	# End of HandlerBind()

	def Hide(self):
		self.objCanvas.place_forget()
	# End of Forget()

	def MoveImage(self, imgID, iX, iY):
		self.objCanvas.move(imgID, iX, iY)
	# End of MoveImage()

	def ResizeImage(self, objImg=None, iImgW=-1, iImgH=-1):
		for x in range(1):
			if iImgW == -1 and iImgH == -1:
				if self.objLoggerLog is not None:
					self.objLoggerLog("Warning: Both iImgW and iImgH are -1. Returning same image without resizing")
				# End of if
				break
			# End of if

			if objImg == None:
				objImg = self.objImg
			# End of if

			try:
				objImg.size[0]
			except:
				objImg = objLibImageTk.getimage(objImg)
			# End of try / except

			if iImgW == -1:
				iImgW = int(iImgH * objImg.size[0] / objImg.size[1])
			# End of if

			if iImgH == -1:
				iImgH = int(iImgW * objImg.size[1] / objImg.size[0])
			# End of if

			objImg = objImg.resize((iImgW, iImgH), objLibImage.LANCZOS)
			# End of try / except

			self.objImg = objLibImageTk.PhotoImage(objImg)
			self.iImgW = iImgW
			self.iImgH = iImgH
		# End of for loop
	# End of ResizeImage()

	def SetBackgroundColour(self, colourBg):
		self.objCanvas.configure(bg=colourBg)
	# End of SetBackgroundColour()

	def Show(self):
		self.objCanvas.place(self.dictPlaceInfo)
	# End of Display()

	def SetItemState(self, iID, strState):
		self.objCanvas.itemconfig(iID, state=strState)
	# End of ClearItem()	
# End of class clCanvas

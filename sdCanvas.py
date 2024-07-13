#
# Created:	 13-January-2022
#
# Enhancement : 15-Feb-2022 : 1. Add parameter "iImgID" to function Clear()
#							  2. Added functions Bind(), AddTooltip(), Show() and Hide()
# 							  3. Added parameters iW and iH to function CreateCanvas()
#							  5. Add parameter "strTooltip" to function AddImage()
#
# Fix 		  :	16-Oct-2023 : Changed deprecated function "ANTIALIAS" with "LANCZOS"
#

#********************************************************************************************
# Imports
#********************************************************************************************
from PIL import Image as objLibImage
from PIL import ImageTk as objLibImageTk
from re import sub as objLibRESub
import sdTooltip as objLibTooltip
import threading as objLibThreading
import tkinter as objLibTK

class clCanvas:
	def __init__(self):
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
		if self.objImg == None:
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
		if self.objCanvas != None:
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
		if objImg != None:
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
		if self.objImg != None:
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

			self.objTooltip = objLibTooltip.clTooltip(self.objCanvas, strPosition=strTooltipPos, strMessage=self.strTooltip)
		# End of if
	# End of CreateCanvas()

	def CreateImage(self, strImgPath="", iImgW=-1, iImgH=-1, objImg=None):
		if objImg == None:
			# Open image
			objImg = objLibImage.open(strImgPath)

			if iImgW == -1:
				iImgW = int(iImgH * objImg.size[0] / objImg.size[1])
			elif iImgH == -1:
				iImgH = int(iImgW * objImg.size[1] / objImg.size[0])
			# End of if
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

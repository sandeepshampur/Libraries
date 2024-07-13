#
# Created : 10-March-2022
#

#********************************************************************************************
# Imports
#********************************************************************************************
from hashlib import sha256 as objSHA256
import os as objLibOS

class clChecksum:
	def __init__(self):
		# 8 MB block size
		self.iBlockSize = 8388608
	# End of __init__()

	def GetChecksum(self, strFile, iSize=0):
		# Get file size if not passed
		if iSize == 0:
			iSize = objLibOS.path.getsize(strFile)
		# End of if

		# Reset block size if file is smaller
		iBlockSize = self.iBlockSize
		if iSize < iBlockSize:
			iBlockSize = iSize
		# End of if

		# Initialise
		objSHA256Inst = objSHA256()
		objSHA256Update = objSHA256Inst.update

		# Generate checksum
		with open(strFile, "rb") as objFile:
			for binBlock in iter(lambda: objFile.read(iBlockSize), b""):
				objSHA256Update(binBlock)
			# End of for loop
		# End of with

		strChecksum = objSHA256Inst.hexdigest()

		return strChecksum
	# End of GetChecksum()

	def SetBlockSize(self, iSize):
		self.iBlockSize = iSize
	# End of SetBlockSize()
# End of class clChecksum
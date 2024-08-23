#
# Started   : 28-June-2024
# Completed : 01-July-2024
#
# Enhancement : 23-Aug-2024 : 1. Revamped logic by adding INI file based query
#							  2. Added function "RegExp()"
#

import os as objLibOS
import re as objLibRE
import sdIniParser as objLibIniParser
import sqlite3 as objSQLite

class clDatabase:
	def __init__(self, strPath, strDatabaseFile, strIniFile, objCommon, objLoggerLog):
		# Initialise
		self.strDatabaseFile = objLibOS.path.join(strPath, strDatabaseFile)
		strIniFile = objLibOS.path.join(strPath, strIniFile)
		self.objCommon = objCommon
		self.objLoggerLog = objLoggerLog

		self.objDatabase = None
		self.objCursor = None

		dictParams = { "strIniFile": strIniFile }
		self.objIniParser = self.objCommon.GetLibrary("sdIniParser", **dictParams)
	# End of __init__()

	def ClearDb(self):
		for x in range(1):
			self.Connect()
			if self.objDatabase is None:
				break
			# End of if

			strDatabaseName = self.objIniParser.GetItem("General", "DatabaseName")
			strQuery = "".join(["delete from ", strDatabaseName])

			# Clear database
			try:
				self.objCursor.execute(strQuery)
			except Exception as strError:
				if self.objLoggerLog is not None:
					self.objLoggerLog("Exception in clearing database", strError)
				# End of if
				break
			# End of try/except

			self.objDatabase.commit()
			self.Close()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Cleared database strDatabaseName", strDatabaseName)
			# End of if
		# End of for loop
	# End of ClearDb()

	def Close(self):
		if self.objDatabase is not None:
			self.objDatabase.close()
			self.objDatabase = None
			self.objCursor = None

			if self.objLoggerLog is not None:
				self.objLoggerLog("Closed database")
			# End of if
		# End of if
	# End of Close()

	def Connect(self):
		for x in range(1):
			try:
				self.objDatabase = objSQLite.connect(self.strDatabaseFile)
			except Exception as strError:
				if self.objLoggerLog is not None:
					self.objLoggerLog("ERROR Exception in connecting to database", strError)
				# End of if
				break
			# End of try/except

			self.objDatabase.create_function("REGEXP", 2, self.RegExp)
			self.objCursor = self.objDatabase.cursor()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Connected to database", self.strDatabaseFile)
			# End of if
		# End of for loop
	# End of Connect()

	def Create(self, strSection, strKey):
		for x in range(1):
			self.Connect()
			if self.objDatabase is None:
				break
			# End of if

			strQuery = self.objIniParser.GetItem(strSection, strKey)

			# Create table
			try:
				self.objCursor.execute(strQuery)
			except Exception as strError:
				if self.objLoggerLog is not None:
					self.objLoggerLog("Exception in creating database", strError)
				# End of if
				break
			# End of try/except

			self.objDatabase.commit()
			self.Close()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Created database")
			# End of if
		# End of for loop
	# End of Create()

	def FetchAll(self, strSection, strKey, arrQueryOptions=[]):
		for x in range(1):
			arrResult = ["Error"]
			self.Connect()
			if self.objDatabase is None:
				break
			# End of if

			strQuery = self.objIniParser.GetItem(strSection, strKey)

			# Read data
			try:
				self.objCursor.execute(strQuery, arrQueryOptions)
			except Exception as strError:
				if self.objLoggerLog is not None:
					self.objLoggerLog("Exception in fetching data", strError)
				# End of if
				break
			# End of try/except

			arrResult = self.objCursor.fetchall()
			self.Close()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Records read:", len(arrResult))
			# End of if
		# End of for loop

		return arrResult
	# End of FetchAll()

	def FetchOne(self, strSection, strKey, arrQueryOptions=[]):
		for x in range(1):
			arrResult = ["Error"]
			self.Connect()
			if self.objDatabase is None:
				break
			# End of if

			strQuery = self.objIniParser.GetItem(strSection, strKey)

			# Read data
			try:
				self.objCursor.execute(strQuery, arrQueryOptions)
			except Exception as strError:
				if self.objLoggerLog is not None:
					self.objLoggerLog("Exception in fetching data", strError)
				# End of if
				break
			# End of try/except

			arrResult = self.objCursor.fetchone()
			self.Close()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Records read: ",  len(arrResult))
			# End of if
		# End of for loop

		return arrResult
	# End of FetchOne()

	def GetIniQuery(self, strSection, strKey):
		return self.objIniParser.GetItem(strSection, strKey)
	# End of GetIniQuery()

	def RegExp(self, strExpression, strItem):
		objRE = objLibRE.compile(strExpression)
		objResult = objRE.search(strItem)
		bReturn = False if objResult is None else True

		return bReturn
	# End of RegExp()

	def WriteMany(self, strSection, strKey, arrRecords):
		'''
		Structure of arrRecords
		arrRecords = [
			["field 1 value", "field 1 value", ...],
			...
		]
		'''
		for x in range(1):
			self.Connect()
			if self.objDatabase is None:
				break
			# End of if

			strQuery = self.objIniParser.GetItem(strSection, strKey)

			strQuestionMarks = ",".join("?" * len(arrRecords[0]))
			arrQuery = strQuery.split("|-?-|")
			strQuery = "".join([arrQuery[0], strQuestionMarks, arrQuery[1]])

			try:
				self.objCursor.executemany(strQuery, arrRecords)
			except Exception as strError:
				if self.objLoggerLog is not None:
					self.objLoggerLog("Exception in writing to database", strError)
				# End of if
				break
			# End of try/except

			self.objDatabase.commit()
			self.Close()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Records written:", len(arrRecords))
			# End of if
		# End of for loop
	# End of WriteMany()

	def WriteOne(self, strSection, strKey, arrRecord):
		'''
		Structure of arrRecord
		arrRecord = [
			["field 1 value", "field 1 value", ...]
		]
		'''

		for x in range(1):
			self.Connect()
			if self.objDatabase is None:
				break
			# End of if

			strQuery = self.objIniParser.GetItem(strSection, strKey)

			strQuestionMarks = ",".join("?" * len(arrRecord[0]))
			arrQuery = strQuery.split("|-?-|")
			strQuery = "".join([arrQuery[0], strQuestionMarks, arrQuery[1]])

			try:
				self.objCursor.execute(strQuery, arrRecord)
			except Exception as strError:
				if self.objLoggerLog is not None:
					self.objLoggerLog("Exception in writing to database", strError)
				# End of if
				break
			# End of try/except

			self.objDatabase.commit()
			self.Close()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Record written: 1")
			# End of if
		# End of for loop
	# End of WriteOne()
# End of class clDatabase

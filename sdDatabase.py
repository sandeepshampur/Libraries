#
# Started   : 28-June-2024
# Completed : 01-July-2024
#

from os.path import join as objOSPathJoin
import sqlite3 as objSQLite

class clDatabase:
	def __init__(self, strDBName="Database.db", strWorkingDir="", objLoggerLog=None):
		# Initialise
		self.DbPath = objOSPathJoin(strWorkingDir, strDBName)
		self.objLoggerLog = objLoggerLog
		self.objDatabase = None
		self.objCursor = None
		self.strDatabaseName = ""
	# End of __init__()

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
		try:
			self.objDatabase = objSQLite.connect(self.DbPath)
			self.objCursor = self.objDatabase.cursor()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Connected to database", self.DbPath)
			# End of if
		except Exception as strError:
			if self.objLoggerLog is not None:
				self.objLoggerLog("Exception in connecting to database", strError)
			# End of if
		# End of try/except
	# End of Connect()

	def Create(self, dictDb):
		"""
		dictDb = {
			"DbName": "Database",
			"Fields": "Field1 text, Field2 Date, Field3 integer, Field 4 real"
		}
		"""
		self.strDatabaseName = dictDb["DbName"]
		self.Connect()

		# Create query string
		strQuery = "".join(["create table if not exists ", dictDb["DbName"], "(", dictDb["Fields"], ");"])

		# Create table
		try:
			self.objCursor.execute(strQuery)
			self.objDatabase.commit()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Created database dictDb:", dictDb)
			# End of if
		except Exception as strError:
			if self.objLoggerLog is not None:
				self.objLoggerLog("Exception in creating database", strError)
			# End of if
		# End of try/except

		self.Close()
	# End of Create()

	def FetchAll(self, strQuery, arrQueryOptions=[]):
		self.Connect()

		# Read data
		try:
			self.objCursor.execute(strQuery, arrQueryOptions)
			arrResult = self.objCursor.fetchall()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Records read:", len(arrResult))
			# End of if
		except Exception as strError:
			arrResult = ["Error"]
			if self.objLoggerLog is not None:
				self.objLoggerLog("Exception in fetching data", strError)
			# End of if
		# End of try/except

		self.Close()
		return arrResult
	# End of Read()

	def FetchOne(self, strQuery, arrQueryOptions=[]):
		# Connect to database
		self.Connect()

		# Read data
		try:
			self.objCursor.execute(strQuery, arrQueryOptions)
			arrResult = self.objCursor.fetchone()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Records read:", len(arrResult))
			# End of if
		except Exception as strError:
			arrResult = ["Error"]
			if self.objLoggerLog is not None:
				self.objLoggerLog("Exception in fetching data", strError)
			# End of if
		# End of try/except

		self.Close()
		return arrResult
	# End of Read()

	def ClearDb(self):
		self.Connect()

		# Clear database
		try:
			strQuery = "".join(["delete from ", self.strDatabaseName])
			self.objCursor.execute(strQuery)
			self.objDatabase.commit()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Cleared database")
			# End of if
		except Exception as strError:
			if self.objLoggerLog is not None:
				self.objLoggerLog("Exception in clearing database", strError)
			# End of if
		# End of try/except

		self.Close()
	# End of ClearDb()

	def WriteMany(self, strQuery, arrRecords):
		self.Connect()

		try:
			self.objCursor.executemany(strQuery, arrRecords)
			self.objDatabase.commit()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Records written:", len(arrRecords))
			# End of if
		except Exception as strError:
			if self.objLoggerLog is not None:
				self.objLoggerLog("Exception in writing to database", strError)
			# End of if
		# End of try/except

		self.Close()
	# End of WriteMany()

	def WriteOne(self, strQuery, arrRecord):
		self.Connect()

		try:
			self.objCursor.execute(strQuery, arrRecord)
			self.objDatabase.commit()

			if self.objLoggerLog is not None:
				self.objLoggerLog("Record written: 1")
			# End of if
		except Exception as strError:
			if self.objLoggerLog is not None:
				self.objLoggerLog("Exception in writing to database", strError)
			# End of if
		# End of try/except

		self.Close()
	# End of WriteOne()
# End of class clDatabase

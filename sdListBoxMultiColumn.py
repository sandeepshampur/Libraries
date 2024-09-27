#
# Completed : 04-December-2021
#
# Enhancement : 17-Feb-2022 : Added colourFg and colourBg parameters to __init__() function
# Fix		  : 01-Mar-2022 : 1. Fixed code to prevent exception when time is blank in "_sort_by_time()"
#							  2. Fixed code to prevent exception when date is blank in "_sort_by_date()"
#							  3. Fixed code to keep blank date in "FormatDate()"
#							  4. Removed duplicate code in "Display()"
#							  5. Added function "Bind()"
# Enhancement : 14-Mar-2022 : Added function "DeleteRow()"
# Enhancement : 21-Jun-2024 : Added function "_sort_by_multidecimal" in clListBoxMultiColumnSort
# Fix		  : 22-Jun-2024 : Added check in clListBoxMultiColumn->FormatDate() to leave date untouched if it is already having hyphens ("-")
# Enhancement : 30-Jun-2024 : Added flag "bSortDescending" to choose order of sorting
# Enhancement : 18-Jul-2024 : Added function "SelectRow()" to select a specific row
# Enhancement : 19-Aug-2024 : 1. Modified "Insert()" to accept position to insert
#							  2. Added function "Move()"
#							  3. Moved colours to dictionary
# Fix		  : 15-Sep-2024 : Removed hardcoded value in "Enable()"
# Enhancement : 24-Sep-2024 : Added functions "_sort_by_datetime()" and "UpdateRow()"
#

import datetime as objDateTime
from functools import partial
import threading as objLibThreading
import tkinter as objTK
from tkinter import ttk as objTTK

class clListBoxMultiColumn:
	def __init__(self, dictTvHdrAttrib, arrDefaultRecords, iSortByColumn, arrFont, dictColours, objLoggerLog):
		self.dictTvHdrAttrib = dictTvHdrAttrib
		self.arrDefaultRecords = arrDefaultRecords
		self.iColumnToSort = iSortByColumn
		self.arrFont = arrFont
		self.dictColours = dictColours
		self.objLoggerLog = objLoggerLog

		# Identify columns with date for formatting later
		self.arrDtCol = []
		iIndex = 0
		arrHdr = self.dictTvHdrAttrib["sortType"]
		if "date" in arrHdr:
			while(1):
				try:
					iIndex = arrHdr.index("date", iIndex)
				except:
					break
				# End of try / except

				self.arrDtCol.append(iIndex)
				iIndex += 1
			# End of while loop
		# End of if
	# End of __init__()
	
	def Display(self, objWindow, strSelectMode, ifrX, ifrY, ifrW, ifrH, arrRecords, bSortDescending=False, strHeader=""):
		objFrame = objTK.LabelFrame(objWindow, text=strHeader, foreground=self.dictColours["colourFg"], background=self.dictColours["colourBg"])
		self.bSortDescending = bSortDescending

		# Set header background colour
		objStyle = objTTK.Style()
		tFont = (self.arrFont[0], self.arrFont[1], "bold")
		objStyle.configure("tvResult.Treeview", background="black", fieldbackground=self.dictColours["tagBgEven"])
		objStyle.configure("tvResult.Treeview.Heading", foreground=self.dictColours["colourFgHdr"], background=self.dictColours["colourBgHdr"], font=tFont)

		self.tvRecords = clListBoxMultiColumnSort(master=objFrame, columns=self.dictTvHdrAttrib["header"], show="headings", selectmode=strSelectMode,
												  style="tvResult.Treeview", tagBgEven=self.dictColours["tagBgEven"], tagBgOdd=self.dictColours["tagBgOdd"],
												  bSortDescending=self.bSortDescending, objLoggerLog=self.objLoggerLog)
		objRWHScr = objTTK.Scrollbar(master=objFrame, orient="horizontal", command=self.tvRecords.xview)
		objRWHScr.grid(column=0, row=1, sticky="ew", in_=objFrame)		
		objRWVScr = objTTK.Scrollbar(master=objFrame, orient="vertical", command=self.tvRecords.yview)
		objRWVScr.grid(column=1, row=0, sticky="ns", in_=objFrame)
		self.tvRecords.configure(yscrollcommand=objRWVScr.set, xscrollcommand=objRWHScr.set)
		
		self.tvRecords.grid(column=0, row=0, sticky="nsew", in_=objFrame)
		objFrame.grid_columnconfigure(0, weight=1)
		objFrame.grid_rowconfigure(0, weight=1)
		
		objFrame.place(x=ifrX, y=ifrY, width=ifrW, height=ifrH)

		# Add header and attributes	
		for iCount in range(len(self.dictTvHdrAttrib["width"])):
			strHdr = self.dictTvHdrAttrib["header"][iCount]
			iHdrW = self.dictTvHdrAttrib["width"][iCount]

			self.tvRecords.heading(strHdr, text=strHdr, sort_by=self.dictTvHdrAttrib["sortType"][iCount])
			self.tvRecords.column(self.dictTvHdrAttrib["header"][iCount], minwidth=iHdrW, width=iHdrW, stretch=False,
								  anchor=self.dictTvHdrAttrib["alignment"][iCount])
		# End of for loop
		
		# Insert data
		self.Insert(arrRecords)
	# End of Display()

	def HandlerBind(self):
		if self.objCallback is not None:
			objThread = objLibThreading.Thread(target=self.objCallback, args=self.tpBindArgs)
			objThread.start()
		# End of if
	# End of HandlerBind()

	def Bind(self, strKey, objCallback=None, tpParam=()):
		self.tvRecords.bind(strKey, lambda _: self.HandlerBind())
		self.objCallback = objCallback
		self.tpBindArgs = tpParam
	# End of Bind()
	
	def ClearAll(self):
		self.tvRecords.delete(*self.tvRecords.get_children(""))
	# End of ClearAll()

	def DeleteRow(self, iRow):
		# iRow is zero-based

		for x in range(1):
			arrIIDs = self.tvRecords.get_children("")
			if len(arrIIDs) == 0:
				break
			# End of if

			if (iRow+1) > len(arrIIDs):
				break
			# End of if

			self.tvRecords.delete(arrIIDs[iRow])
		# End of for loop
	# End of DeleteRow()
	
	def DeleteSelection(self):
		self.tvRecords.delete(*self.tvRecords.selection())
		
		if self.iColumnToSort != -1:
			self.Sort(self.dictTvHdrAttrib["sortType"][self.iColumnToSort], self.dictTvHdrAttrib["header"][self.iColumnToSort], self.bSortDescending)
		# End of if
	# End of DeleteSelection()
	
	def Disable(self):
		self.tvRecords.configure(selectmode="none")
	# End of Disable()

	def Enable(self, strMode):
		# strMode : "browse"|"extended"
		self.tvRecords.configure(selectmode=strMode)
	# End of Enable()
	
	def GetCount(self):
		arrIIDs = self.tvRecords.get_children("")
		return len(arrIIDs)
	# End of GetCount()

	def GetAllEntries(self):
		arrResult = []
		arrIIDs = self.tvRecords.get_children("")
		for objItem in arrIIDs:
			arrResult.append(self.tvRecords.item(objItem)["values"])
			
			# Format date if present
			self.UnFormatDate(arrResult[-1])
		# End of for loop
		
		return arrResult
	# End of GetAllEntries()
	
	def GetSelectionEntries(self):		
		arrResult = []
		arrIIDs = self.tvRecords.selection()
		for objItem in arrIIDs:
			arrResult.append(self.tvRecords.item(objItem)["values"])
			
			self.UnFormatDate(arrResult[-1])
		# End of for loop
		
		return arrResult
	# End of GetSelectionEntries()

	def GetSelectionRows(self):
		arrRows = []
		arrIIDs = self.tvRecords.selection()
		arrListIIDs = self.tvRecords.get_children("")
		for strID in arrIIDs:
			arrRows.append(arrListIIDs.index(strID))
		# End of for loop

		return arrRows
	# End of GetSelectionRows()

	def Insert(self, arrList, strPosition="end"):
		# strPosition is zero-based

		# Initialise
		iTotalRows = self.GetCount()
		if isinstance(strPosition, str):
			iInsertPosition = iTotalRows
		else:
			iInsertPosition = int(strPosition)
		# End of if

		if iInsertPosition < 0:
			iInsertPosition = 0
		elif iInsertPosition > iTotalRows:
			iInsertPosition = iTotalRows
		# End of if

		# Insert values
		for arrRow in arrList:
			self.FormatDate(arrRow)
		
			if iInsertPosition % 2 == 0:
				self.tvRecords.insert("", iInsertPosition, None, values=arrRow, tags="tgEvenRow")
			else:
				self.tvRecords.insert("", iInsertPosition, None, values=arrRow, tags="tgOddRow")
			# End of if

			iInsertPosition += 1
			iTotalRows += 1
		# End of for loop

		# Retag till end of listbox
		arrIIDs = self.tvRecords.get_children("")
		while iInsertPosition < iTotalRows:
			if iInsertPosition % 2 == 0:
				self.tvRecords.item(arrIIDs[iInsertPosition], tags="tgEvenRow")
			else:
				self.tvRecords.item(arrIIDs[iInsertPosition], tags="tgOddRow")
			# End of if
			iInsertPosition += 1
		# End of while loop

		if self.iColumnToSort != -1:
			self.Sort(self.dictTvHdrAttrib["sortType"][self.iColumnToSort], self.dictTvHdrAttrib["header"][self.iColumnToSort], self.bSortDescending)
		# End of if
	# End of Insert()

	def Move(self, strDirection):
		# strDirection "Up" or "Down"

		for x in range(1):
			# Get selected row details
			iCurrentPosition = self.GetSelectionRows()[0]
			arrCurrentIID = self.tvRecords.selection()
			iTotalRows = self.GetCount()

			# Ignore end cases
			if (strDirection.find("Up") == 0) and (iCurrentPosition == 0):
				break
			# End of if
			if (strDirection.find("Down") == 0) and (iCurrentPosition == (iTotalRows-1)):
				break
			# End of if

			# Move row
			if strDirection.find("Up") == 0:
				self.tvRecords.move(arrCurrentIID[0], '', iCurrentPosition-1)
				iCurrentPosition -= 1
			else:
				self.tvRecords.move(arrCurrentIID[0], '', iCurrentPosition+1)
			# End of if

			# Retag rows
			arrIIDs = self.tvRecords.get_children("")
			while iCurrentPosition < iTotalRows:
				if iCurrentPosition % 2 == 0:
					self.tvRecords.item(arrIIDs[iCurrentPosition], tags="tgEvenRow")
				else:
					self.tvRecords.item(arrIIDs[iCurrentPosition], tags="tgOddRow")
				# End of if
				iCurrentPosition += 1
			# End of while loop
		# End of for loop
	# End of GetSelectionIndex()

	def Reset(self):
		self.ClearAll()
		self.Insert(self.arrDefaultRecords)
	# End of Reset()

	def SelectRow(self, iRowPosition):
		for x in range(1):
			# Get records
			arrList = self.tvRecords.get_children("")
			try:
				self.tvRecords.selection_set(arrList[iRowPosition])
			except:
				pass
			# End of try / except
		# End of for loop
	# End of SetSelection()
	
	def Sort(self, strSortType, strColumn, reverse):
		self.tvRecords.SortByFunctionName(strSortType, strColumn, reverse)
	# End of Sort()
	
	def UpdateRow(self, iRow, arrItem):
		# iRow is zero based
		self.FormatDate(arrItem)
		arrIIDs = self.tvRecords.get_children("")

		self.tvRecords.item(arrIIDs[iRow], values=tuple(arrItem))

		if self.iColumnToSort != -1:
			self.Sort(self.dictTvHdrAttrib["sortType"][self.iColumnToSort], self.dictTvHdrAttrib["header"][self.iColumnToSort], self.bSortDescending)
		# End of if
	# End of UpdateRow()

	def UpdateSelectedItem(self, arrItem):
		self.FormatDate(arrItem)
		
		selected = self.tvRecords.focus()
		self.tvRecords.item(selected, values=tuple(arrItem))

		if self.iColumnToSort != -1:
			self.Sort(self.dictTvHdrAttrib["sortType"][self.iColumnToSort], self.dictTvHdrAttrib["header"][self.iColumnToSort], self.bSortDescending)
		# End of if
	# End of UpdateSelectedItem()	
	
	def FormatDate(self, arrRow):
		for iIndex in self.arrDtCol:
			strDate = str(arrRow[iIndex])
			if len(strDate) == 0:
				strDate = ""
			else:
				if strDate.find("-") == -1:
					strDate = "-".join([strDate[:4], strDate[4:6], strDate[6:]])
				# End of if
			# End of if
			arrRow[iIndex] = strDate
		# End of if
	# End of FormatDate()

	def UnFormatDate(self, arrRow):
		for iIndex in self.arrDtCol:
			strDate = str(arrRow[iIndex])
			arrRow[iIndex] = strDate.replace("-", "")
		# End of if
	# End of UnFormatDate()	
# End of class clListBoxMultiColumn

class clListBoxMultiColumnSort(objTTK.Treeview):
	'''
	Sorting customised from
	https://stackoverflow.com/questions/1966929/tk-treeview-column-sort/69294086#69294086

	Sorting types allowed
		Particulars	:	Key				: Description
	===========================================================================================
	1. Date			:	"date"			: Date with zero padding e.g.: 1973-10-03
	2. Data / Time	: 	"datetime"		: Date / time with zero padding e.g. 1973-10-03 07:30 AM
	3. Float		:	"float"			: Float number e.g.: 12.0
	4. Multidecimal	:	"multidecimal" 	: Numbers with multiple periods e.g.: 12.5.7.12
	5. Number		:	"num"			: Integers
	6. Number		:	"numcomma"		: Numbers with comma e.g.: 12,000
	7. Name			:	"name"			: Text
	8. Time			:	"time"			: Time in 12 format with zero padding e.g.: 11:03PM

	Sorting type defaults to "name" for invalid key
	LIMITATION of "multidecimal":
	 			1, works only for two digits or less. It does not work for more than three digits (e.g.: 3.111.1).
	 			2. The maximum decimals allowed is eight. (e.g.: 99.99.99.99.99.99.99.99.99). Any excess is truncated
	'''
	
	def __init__(self, master=None, my_list=[], bSortDescending=False, tagBgEven="#f5f5f5", tagBgOdd="#dcdcff", objLoggerLog=None, **kwargs):
		self.bSortDescending = bSortDescending
		self.objLoggerLog = objLoggerLog

		super(clListBoxMultiColumnSort, self).__init__(master=master, **kwargs)

		# Sorting key array. This has to be updated when any new sorting function is added
		self.arrSortKeys = ["date", "float", "multidecimal", "num", "numcomma", "name", "time", "datetime"]

		# Row colouring
		self.tag_configure("tgEvenRow", background=tagBgEven)
		self.tag_configure("tgOddRow", background=tagBgOdd)
	# End of __init__()
	
	def delete(self, *tiID):
		super(clListBoxMultiColumnSort, self).delete(*tiID)

		# Retag row colours
		for item in self.get_children(""):
			index = self.index(item)
			if index % 2 == 0:
				self.item(item, tags="tgEvenRow")
			else:
				self.item(item, tags="tgOddRow")
			# End of if
		# End of for loop
	# End of delete()
	
	def heading(self, column, sort_by=None, **kwargs):
		if sort_by and not hasattr(kwargs, 'command'):
			func = getattr(self, f"_sort_by_{sort_by}", None)
			if func:
				kwargs['command'] = partial(func, column, False)
			# End of if
		# End of if
		return super().heading(column, **kwargs)
	# End of heading()

	def SortByFunctionName(self, strSortType, strColumnName, reverse):
		# Form function name
		if strSortType in self.arrSortKeys:
			strFunction = "".join(["_sort_by_", strSortType])
		else:
			strFunction = "_sort_by_name"
			if self.objLoggerLog is not None:
				self.objLoggerLog("ERROR: <clListBoxMultiColumnSort> : Defaulting to sort by name strSortType:", strSortType)
			# End of if
		# End of if

		# Get function object
		objFunction = getattr(self, strFunction)
		objFunction(strColumnName, reverse)
	# End of SortByFunctionName()	

	def _sort(self, column, reverse, data_type, callback):
		arrValueIDPair = [(self.set(iID, column), iID) for iID in self.get_children("")]
		arrValueIDPair.sort(key=lambda objValue: data_type(objValue[0]), reverse=reverse)

		# Move and retag row colours
		for iIndex, (_, iID) in enumerate(arrValueIDPair):
			self.move(iID, '', iIndex)
			if iIndex % 2 == 0:
				self.item(iID, tags="tgEvenRow")
			else:
				self.item(iID, tags="tgOddRow")
			# End of if
		# End of for loop
		self.heading(column, command=partial(callback, column, not reverse))
	# End of _sort()

	def _sort_by_date(self, column, reverse):
		def _str_to_date(string):
			if len(string) == 0:
				# Very old date
				string = "1973-10-03"
			# End of if
			return objDateTime.datetime.strptime(string, "%Y-%m-%d")
		# End of _str_to_date()

		self._sort(column, reverse, _str_to_date, self._sort_by_date)
	# End of _sort_by_date()

	def _sort_by_datetime(self, column, reverse):
		def _str_to_datetime(string):
			if len(string) == 0:
				# Very old date / time
				string = "1973-10-03 06:00 AM"
			# End of if
			return objDateTime.datetime.strptime(string.upper(), "%Y-%m-%d %I:%M %p")
		# End of _str_to_datetime()

		self._sort(column, reverse, _str_to_datetime, self._sort_by_datetime)
	# End of _sort_by_datetime()

	def _sort_by_float(self, column, reverse):
		self._sort(column, reverse, float, self._sort_by_float)
	# End of _sort_by_float()

	def _sort_by_multidecimal(self, column, reverse):
		def _multidecimal_to_str(string):
			arrString = string.split(".")
			arrNum = []
			for strString in arrString:
				strValue = f"{int(strString):02}"
				arrNum.append(strValue)
			# End of for loop

			arrNum.append("000000000000000000")
			strNum = "".join(arrNum)

			if self.objLoggerLog is not None:
				if len(strNum) > 36:
					self.objLoggerLog("ERROR: <clListBoxMultiColumnSort> : Number is truncated as it exceeds limit. string:", string)
				# End of if
			# End of if

			return int(strNum[:18])
		# End of _multidecimal_to_str()

		self._sort(column, reverse, _multidecimal_to_str, self._sort_by_multidecimal)
	# End of _sort_by_multidecimal()

	def _sort_by_name(self, column, reverse):
		self._sort(column, reverse, str, self._sort_by_name)
	# End of _sort_by_name()

	def _sort_by_num(self, column, reverse):
		self._sort(column, reverse, int, self._sort_by_num)
	# End of _sort_by_num()

	def _sort_by_numcomma(self, column, reverse):
		def _numcomma_to_num(string):
			return int(string.replace(",", ""))
		# End of _numcomma_to_num()
		
		self._sort(column, reverse, _numcomma_to_num, self._sort_by_numcomma)
	# End of _sort_by_numcomma()

	def _sort_by_time(self, column, reverse):
		def _str_to_time(string):
			if len(string) == 0:
				string = "12:00AM"
			# End of if
			return objDateTime.datetime.strptime(string, "%I:%M%p")
		# End of _str_to_time()

		self._sort(column, reverse, _str_to_time, self._sort_by_time)
	# End of _sort_by_time()
# End of clListBoxMultiColumnSort

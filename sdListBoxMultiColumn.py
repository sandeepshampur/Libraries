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
#
# Fix		  : 22-Jun-2024 : Added check in clListBoxMultiColumn->FormatDate() to leave date untouched if it is already having hyphens ("-")
# Enhancement : 30-Jun-2024 : Added flag "bSortDescending" to choose order of sorting
#

import datetime as objDateTime
from functools import partial
import threading as objLibThreading
import tkinter as objTK
from tkinter import ttk as objTTK

class clListBoxMultiColumn:
	def __init__(self, dictTvHdrAttrib, arrDefaultRecords=[], iSortByColumn=-1, colourFg="black", colourBg="white"):
		self.dictTvHdrAttrib = dictTvHdrAttrib
		self.arrDefaultRecords = arrDefaultRecords
		self.iColumnToSort = iSortByColumn
		self.colourFg = colourFg
		self.colourBg = colourBg

		# Identify columns with date for formatting later
		self.arrDtCol = []
		iIndex = 0
		arrHdr = self.dictTvHdrAttrib["sortType"]
		if "date" in arrHdr:
			for x in range(1000):
				try:
					iIndex = arrHdr.index("date", iIndex)
					self.arrDtCol.append(iIndex)
					iIndex += 1
				except:
					break
				# End of try / except
			# End of for loop
		# End of if
	# End of __init__()
	
	def Display(self, objWindow, strSelectMode, ifrX, ifrY, ifrW, ifrH, arrRecords, bSortDescending=False):
		objFrame = objTK.LabelFrame(objWindow, text="Records", foreground=self.colourFg, background=self.colourBg)
		self.bSortDescending = bSortDescending

		# Set header background colour
		objStyle = objTTK.Style()
		objStyle.configure("tvResult.Treeview.Heading", background="#C3C3C3")

		self.tvRecords = clListBoxMultiColumnSort(master=objFrame, columns=self.dictTvHdrAttrib["header"], show="headings", selectmode=strSelectMode, style="tvResult.Treeview", bSortDescending=self.bSortDescending)
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
			self.tvRecords.column(self.dictTvHdrAttrib["header"][iCount], minwidth=iHdrW, width=iHdrW, stretch=False, anchor=self.dictTvHdrAttrib["alignment"][iCount])
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
		self.tvRecords.delete(*self.tvRecords.get_children())
	# End of ClearAll()

	def DeleteRow(self, iRow):
		self.tvRecords.delete(self.tvRecords.get_children()[iRow])
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

	def Enable(self):
		self.tvRecords.configure(selectmode="extended")
	# End of Enable()
	
	def GetCount(self):
		arrItems = self.tvRecords.get_children()
		return len(arrItems)
	# End of GetCount()

	def GetAllEntries(self):
		arrResult = []
		arrItems = self.tvRecords.get_children()
		for objItem in arrItems:
			arrResult.append(self.tvRecords.item(objItem)["values"])
			
			# Format date if present
			self.UnFormatDate(arrResult[-1])
		# End of for loop
		
		return arrResult
	# End of GetAllEntries()
	
	def GetSelectionEntries(self):		
		arrResult = []		
		arrItems = self.tvRecords.selection()
		for objItem in arrItems:
			arrResult.append(self.tvRecords.item(objItem)["values"])
			
			self.UnFormatDate(arrResult[-1])
		# End of for loop
		
		return arrResult
	# End of GetSelectionEntries()
	
	def Insert(self, arrList):
		# Add to listbox
		iRows = self.GetCount()
		for iCount in range(len(arrList)):		
			arrRow = arrList[iCount]
			
			self.FormatDate(arrRow)
		
			if iRows % 2 == 0:
				self.tvRecords.insert("", "end", values=arrList[iCount], tags="tgEvenRow")
			else:
				self.tvRecords.insert("", "end", values=arrList[iCount], tags="tgOddRow")				
			# End of if
			iRows += 1
		# End of for loop
		
		if self.iColumnToSort != -1:
			self.Sort(self.dictTvHdrAttrib["sortType"][self.iColumnToSort], self.dictTvHdrAttrib["header"][self.iColumnToSort], self.bSortDescending)
		# End of if
	# End of Insert()

	def Reset(self):
		self.ClearAll()
		self.Insert(self.arrDefaultRecords)
	# End of Reset()
	
	def Sort(self, strSortType, strColumn, reverse):
		self.tvRecords.SortByFunctionName(strSortType, strColumn, reverse)
	# End of Sort()
	
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
	# Sorting customised from 
	# https://stackoverflow.com/questions/1966929/tk-treeview-column-sort/69294086#69294086
	
	def __init__(self, master=None, my_list=[], bSortDescending=False, tagBgEven="#FFFFFF", tagBgOdd="#E8E8FF", **kwargs):
		self.bSortDescending = bSortDescending
		super(clListBoxMultiColumnSort, self).__init__(master=master, **kwargs)
		
		# Row colouring
		self.tag_configure("tgEvenRow", background=tagBgEven)				
		self.tag_configure("tgOddRow", background=tagBgOdd)
	# End of __init__()
	
	def delete(self, *items):
		super(clListBoxMultiColumnSort, self).delete(*items)
		
		# Retag row colours
		for item in self.get_children():
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
		strFunction = "".join(["_sort_by_", strSortType])

		# Get function object
		objFunction = getattr(self, strFunction)
		objFunction(strColumnName, reverse)
	# End of SortByFunctionName()	

	def _sort(self, column, reverse, data_type, callback):
		l = [(self.set(k, column), k) for k in self.get_children('')]
		l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
		
		# Move and retag row colours
		for index, (_, k) in enumerate(l):
			self.move(k, '', index)
			if index % 2 == 0:
				self.item(k, tags="tgEvenRow")
			else:
				self.item(k, tags="tgOddRow")
			# End of if
		# End of for loop
		self.heading(column, command=partial(callback, column, not reverse))
	# End of _sort()

	def _sort_by_time(self, column, reverse):
		def _str_to_time(string):
			if len(string) == 0:
				string = "12:00am"
			# End of if
			return objDateTime.datetime.strptime(string, "%I:%M%p")
		# End of _str_to_time()
		
		self._sort(column, reverse, _str_to_time, self._sort_by_time)
	# End of _sort_by_time()

	def _sort_by_date(self, column, reverse):
		def _str_to_date(string):
			if len(string) == 0:
				string = "1973-10-03"
			# End of if

			# End of try / except
			return objDateTime.datetime.strptime(string, "%Y-%m-%d")
		# End of _str_to_date()
		
		self._sort(column, reverse, _str_to_date, self._sort_by_date)
	# End of _sort_by_date()

	def _sort_by_name(self, column, reverse):
		self._sort(column, reverse, str, self._sort_by_name)
	# End of _sort_by_name()

	def _sort_by_num(self, column, reverse):
		self._sort(column, reverse, int, self._sort_by_num)
	# End of _sort_by_num()

	def _sort_by_float(self, column, reverse):
		self._sort(column, reverse, float, self._sort_by_float)
	# End of _sort_by_float()

	def _sort_by_multidecimal(self, column, reverse):
		def _multidecimal_to_str(string):
			arrString = string.split(".")
			strNum = ""
			for iValue in arrString:
				strValue = f"{int(iValue):02}"
				strNum = "".join([strNum, str(strValue)])
			# End of for loop
			strNum = "".join([strNum, "0000000"])
			return int(strNum[:8])
		# End of _multidecimal_to_str()

		self._sort(column, reverse, _multidecimal_to_str, self._sort_by_multidecimal)
	# End of _sort_by_multidecimal()

	def _sort_by_numcomma(self, column, reverse):
		def _numcomma_to_num(string):
			return int(string.replace(",", ""))
		# End of _numcomma_to_num()
		
		self._sort(column, reverse, _numcomma_to_num, self._sort_by_numcomma)
	# End of _sort_by_numcomma()	
# End of clListBoxMultiColumnSort

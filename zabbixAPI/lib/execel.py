#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-24 16:30:08
# @Last Modified by:   ww
# @Last Modified time: 2019-07-24 16:30:33

import xlrd

class MyExcel:

	def __init__(self,file_path):
		try:
			self.xlsdata = xlrd.open_workbook(file_path)
		except Exception as e:
			print e

	def get_execel_table_sheets(self):
		try:
			sheets = self.xlsdata.sheet_names()
			return sheets
		except Exception as e:
			print e

	def get_excel_data(self,sheets_name):
		try:
			data = self.xlsdata
			sname = self.get_execel_table_sheets() 
			if sheets_name in sname:
				table = data.sheet_by_name(sheets_name)
				#获取行数
				nrows = table.nrows
				#获取第一个行的值
				nrows_values =  table.row_values(0)
				list = []
				for rownum in range(1,nrows):
					row = table.row_values(rownum)
					if row:
						info = {}
						for i in range(len(nrows_values)):
							info[nrows_values[i]] = row[i]
						list.append(info)
					else:
						print "表格内容为空"
				return list
			else:
				print "表格中不存在 %s 这个sheet" % sheets_name
		except Exception as e:
			print e
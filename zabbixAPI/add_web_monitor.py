#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-24 16:34:18
# @Last Modified by:   wwu
# @Last Modified time: 2021-10-27 16:55:12

from lib.host import get_hostid_by_hname
from lib.web import *
from lib.execel import MyExcel


def zbx_add_web_monitor(sheet_name):
	"""
		功能说明：批量添加web访问监控
		参数：
			sheet_name: excel表格中的sheet页名称
	"""
	myxls = MyExcel('./conf/webinfo.xlsx')
	mydata = myxls.get_excel_data(sheet_name)

	for i in range(len(mydata)):
		host_name = mydata[i]['host_name']
		scenario_name = mydata[i]['scenario_name']
		url = mydata[i]['url']
		ssl = 0 if mydata[i]['ssl'] == '' else mydata[i]['ssl']
		host_id=get_hostid_by_hname([host_name])[0]
		application_id=get_or_create_application(host_id)
		result=create_web_scenario(scenario_name,url,host_id,application_id,ssl)
		if result == True:
			print "%s %s web Item 添加成功!" % (host_name,scenario_name)
			trigger_result=create_trigger_for_webscenario(host_name,scenario_name,url)
			if trigger_result == True:
			 	print '%s %s web Trigger 添加成功!' % (host_name,scenario_name)
			else:
			 	print '%s %s web Trigger 添加失败!' % (host_name,scenario_name)
		elif result == 'exsits':
			print '%s %s web Item 已经存在!' % (host_name,scenario_name)
		else:
			print "%s %s web Item 添加失败!" % (host_name,scenario_name)


if __name__ == '__main__':
	zbx_add_web_monitor('ha')

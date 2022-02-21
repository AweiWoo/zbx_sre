#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-19 16:26:41
# @Last Modified by:   ww
# @Last Modified time: 2019-07-26 16:07:39


from init import zapi
from pyzabbix import ZabbixAPI

import sys

reload(sys)
sys.setdefaultencoding('utf8')

def get_or_create_application(host_id):
	"""
		功能说明：获取或者创建监控应用项目，默认值为webstat,如果不存在则创建一个，存在则返回该id
		参数：
			host_id: 监控主机id
	"""
	try:
		result = zapi.application.get(hostids=host_id,filter={"name":"webstatus"})
		if result:
			application_id = result[0]['applicationid']
			return application_id
		else:
			application_id = zapi.application.create(hostid=host_id,name="webstatus")
			return application_id
	except Exception as e:
		print e

def create_web_scenario(scenario_name,URL,host_id,application_id,verify_host=0):
	"""
		功能说明：创建web监控http code值监控
		参数：
			scenario_name： web监控的名称，此名称自定义。
			url: 需要监控的web url
			host_id: 监控主机id
			application_id: 建监控应用项目的id，get_or_create_application方法中获取
			verify_host: 1表示url需要进行ssl验证，即https；0表示不验证。默认为0
	"""
	try:
		get_url = zapi.httptest.get(hostids=host_id,filter={"name":scenario_name})
		if get_url:
			return 'exsits'
		else:
			try:
				create_url = zapi.httptest.create(
					name=scenario_name,
					hostid=host_id,
					applicationid=application_id,
					steps=[{"name":"index","url":URL,"status_codes":"200","no":"1"}],
					verify_host=verify_host
					) 
				return True
			except Exception as e:
				print e
				#return False
	except Exception as e:
		print e

def create_trigger_for_webscenario(host_name,scenario_name,URL):
	"""
		功能说明：创建web http code监控告警触发器
		参数：
			host_name：监控主机的显示名称
			scenario_name： web监控项名称，由create_web_scenario方法创建
			URL： 监控的url
	"""
	expression='{'+'{0}:web.test.rspcode[{1},index].count(180,399,"gt")'.format(host_name,scenario_name) + \
		'} >3 or {'+'{0}:web.test.fail[{1}].count(180,0,"ne")'.format(host_name,scenario_name)+'}=3'
	try:
		ZabbixAPI.do_request(zapi, 'trigger.create', 
				params={'description' : '[WEB]-{HOST.NAME} ：'+'{0}无法访问({1})'.format(scenario_name,URL),
			"expression": expression,"priority":3})
		return True
	except Exception :
		return False

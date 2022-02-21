#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-21 17:05:50
# @Last Modified by:   ww
# @Last Modified time: 2019-07-26 10:32:08

from lib.init import zapi,ZabbixAPIException

import json
import sys
reload(sys)

sys.setdefaultencoding('utf8')

def acknowledge_event(eventid,message=None):
	"""
		事件确认
	"""

	try:
		ack_info = zapi.event.acknowledge(eventids=eventid,action=7,message=message)
		return ack_info
	except Exception as e:
		#Error -32602: Invalid params., Incorrect value for field "message": cannot be empty.
		#Error -32500: Application error., Cannot close problem: trigger does not allow manual closing.
		return e[1]

if __name__ == '__main__':	
	result=acknowledge_event('90834228')
	print result
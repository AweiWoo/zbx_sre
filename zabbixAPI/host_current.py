#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-16 15:28:04
# @Last Modified by:   wwu
# @Last Modified time: 2020-03-05 15:52:33

from lib.init import zapi
from lib.host import get_hostid_by_vname
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_current_alarm(hostname):
	hostid = get_hostid_by_vname(hostname)
	current_info = zapi.trigger.get(hostids=hostid,
		only_true=1, #仅返回处于故障状态的触发器
		monitored=1, #触发器状态为启用
		active=1, #主机状态为启用
		selectHosts=['host']
		)

	print json.dumps(current_info,indent=4,ensure_ascii=False) 


if __name__ == '__main__':
	get_current_alarm(['[武汉同济]-192.168.19.128-[qk2-bill-portal-slave1]'])
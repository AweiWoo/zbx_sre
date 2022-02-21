#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-16 10:38:56
# @Last Modified by:   ww
# @Last Modified time: 2019-07-26 10:34:32

from lib.init import zapi
from lib.host import get_hostid
from pyzabbix import ZabbixAPI
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def get_host_problems(hostname,start_time,end_time):
	hostid = get_hostid(hostname)
	problem_info = zapi.problem.get(hostids=hostid,
		output="extend",
		recent="true",
		sortorder="DESC",
		time_from=start_time,
		time_till=end_time
		)

	notrecovery_info = zapi.problem.get(hostids=hostid,
								output="extend",
								sortfield=["eventid"],    
								sortorder="DESC"
								)

if __name__ == '__main__':
	get_host_problems(['[盛博汇]-192.168.10.12-[Nexus]'],1557802716,1557975516)

#1、只查询有问题的，问题恢复后，就查询不出来。不管recent是否为true, problem.get是否存在bug ?
#2、没有selectHost参数，无法获取主机id
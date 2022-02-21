#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-15 11:29:09
# @Last Modified by:   ww
# @Last Modified time: 2019-07-24 16:27:09
# @function: 获取某一个主机的当前预警以及过去N天的历史预警信息，以时间从当前到过去的序列排序

from lib.init import zapi
from lib.host import get_hostid
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def get_host_events(hostname,start_time,end_time):
	hostid = get_hostid(hostname)
	events_info = zapi.event.get(hostids=hostid,
								output="extend",
								sortfield="clock",
								sortorder="DESC",
								time_from=start_time,
								time_till=end_time,
								filter={"value":1}  #value=1表示问题型事件，value=0表示问题恢复型事件。
								)

	recovery_info = zapi.event.get(hostids=hostid,
								output="extend",
								sortfield="clock",
								sortorder="DESC",
								time_from=start_time,
								time_till=end_time,
								selectHosts=['host'],
								filter={"value":0}
								)

	#只获取已经恢复的故障事件信息
	events_list=[]
	for r in recovery_info:
		events_dic={}
		events_dic['hostid']=r['hosts'][0]['hostid']
		#events_dic['hostip']=p['hosts'][0]['host']
		events_dic['name'] = r['name']
		events_dic['end_clock'] = r['clock']

		# for p in events_info:
		# 	if r['eventid'] == p['r_eventid']:
		# 		events_dic['start_clock'] = p['clock']
		# 		events_dic['severity'] = p['severity']

		for i,p in enumerate(events_info):
			if r['eventid'] == p['r_eventid']:
				events_dic['start_clock'] = p['clock']
				events_dic['severity'] = p['severity']
				events_dic['eventid'] = p['eventid']
				events_info.pop(i)
		if len(events_dic) == 6:	
			events_list.append(events_dic)

		# events_list.append(events_dic)
		# while len(events_list[-1]) < 5:
		# 	events_list.pop()
	return events_list

# info = get_host_events(['[盛博汇]-192.168.10.65-[Pro2]'],1557449821,1558054626)
# print json.dumps(info,indent=4,ensure_ascii=False) 

# 1、event.get只能获取范围内（时间，或id）产生的告警事件，如果在不在这个范围内，则不会获取到。
#  例如，某个告警在20天之前产生一直未恢复，设置的范围没有超过20天，则此告警无法获取。
# 2、告警量太多的情况下，api接口查询有些慢，建议在前端查询的时候做分页处理，每页数据不超过一天的数据量。

#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-15 11:29:09
# @Last Modified by:   ww
# @Last Modified time: 2019-07-26 10:32:47
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
								selectHosts=['host'],
								filter={"value":1}  #value=1表示问题型事件，value=0表示问题恢复型事件。
								)

	recovery_info = zapi.event.get(hostids=hostid,
								output="extend",
								sortfield="clock",
								sortorder="DESC",
								time_from=start_time,
								time_till=end_time,
								filter={"value":0}
								)
	events_list=[]
	for p in events_info:
		events_dic={}
		events_dic['hostid']=p['hosts'][0]['hostid']
		#events_dic['hostip']=p['hosts'][0]['host']
		events_dic['eventid']=p['eventid']
		events_dic['name'] = p['name']
		events_dic['start_clock'] = p['clock']
		events_dic['severity'] = p['severity']
		if p['r_eventid'] == "0":
			events_dic['end_clock'] = ""
		else:
			for r in recovery_info:
				if p['r_eventid'] == r['eventid']:
					events_dic['end_clock'] = r['clock']			
		events_list.append(events_dic)

	return events_list

if __name__ == '__main__':
#'[武汉同济]-192.168.19.147-[qk2-inp-portal-slave2]'
	info = get_host_events(['[武汉同济]-192.168.19.147-[qk2-inp-portal-slave2]'],1557802716,1557975516)
	print json.dumps(info,indent=4,ensure_ascii=False) 

#1、说明：event.get只能获取范围内（时间，或id）产生的告警事件，如果在不在这个范围内，则不会获取到。
#2、例如，某个告警在20天之前产生一直未恢复，设置的范围没有超过20天，则此告警无法获取。
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-21 11:16:58
# @Last Modified by:   ww
# @Last Modified time: 2019-07-26 10:34:20

from lib.init import zapi
from lib.host import get_hostid
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def get_groups(hostids=None):
	"""
		return:根据主机id列表查询
	"""
	template_group_info = zapi.hostgroup.get(
							hostids=hostids,
							output=['groupid','name'],
							#real_hosts=1 #仅返回包含主机的主机组
							templated_hosts=1
							)
	group_info = zapi.hostgroup.get(
							hostids=hostids,
							output=['groupid','name']
							)

	for t in template_group_info:
		for i,a in enumerate(group_info):
			if a['groupid'] == t['groupid']:
				group_info.pop(i)

	return group_info


def get_group_agentinfo(groupids):
	agent_info = zapi.hostgroup.get(groupids=groupids,
									#output=['hosts','name'],
									output="extend",
									selectHosts=['host','name']
									)
	return agent_info
	# agent_list=[]
	# for a in agent_info:
	# 	host_list=[ i['host'] for i in a['hosts'] ]
	# 	group_name=a['name']
	# 	groupid=a['groupid']
	# 	host_dic={"host_list":host_list,"group_name":group_name,"group_id":groupid}
	# 	agent_list.append(host_dic)
	# return agent_list

if __name__ == '__main__':
# info = get_groups()
# print json.dumps(info,indent=4,ensure_ascii=False) 
	agent_info = get_group_agentinfo([25,33])
	print json.dumps(agent_info,indent=4,ensure_ascii=False)
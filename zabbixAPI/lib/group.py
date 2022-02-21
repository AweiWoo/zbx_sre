#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-02 15:59:10
# @Last Modified by:   wwu
# @Last Modified time: 2021-08-04 17:59:49
# @Last Modified time: 2020-05-06 09:06:05

from init import zapi
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def get_hostip_bygroupname(groupname):
	
	"""
		功能说明：
			根据zabbix的分组名称获取分组下面的主机名称列表
		参数: 
			groupname: 分组名称，如：[NTRM]南通第一人民医院支撑服务器
		返回值：
			主机名称列表，type:list
	"""
	info = zapi.hostgroup.get(filter={"name":groupname},selectHosts=['host'])
	group_host_name=[ ip['host'] for ip in info[0]['hosts'] ]
	#在分布式架构中，可能存在不同地点相同IP地址的情况，zabbix对于这种情况默认在后面添加“_X”来区分，例如：192.168.10.20_2,下通过你截取方法，之获取前面ip地址部分
	host_info_list = []
	for i in group_host_name:
		host_info_dic = {}
		host_info_dic['host_name'] = i
		host_info_dic['host_ip'] = i.split('_')[0]
		host_info_list.append(host_info_dic)
	return host_info_list


def get_groupid_bygroupname(groupname):

	"""
		功能说明：
			根据zabbix的分组名称获取分组下面的主机组id
		参数: 
			groupname: 分组名称，如：[NTRM]南通第一人民医院支撑服务器
		返回值：
			主机组id表，type:list
	"""
	try:
		group = zapi.hostgroup.get(filter={"name":groupname})
		#print group[0]['groupid']
		group_list=[]
		if group:
			group_dict=dict(groupid=group[0]['groupid'])
			group_list.append(group_dict)
			return group_list			
	except Exception as e:
		print e


def get_groupsinfo(project=None):
    """
    :param hostids: 主机id
    :return: 返回主机组信息，如果为空，则返回所有主机组信息
    """
    group_info = zapi.hostgroup.get(output=['groupid','name'],search={"name":project})
    print group_info


if __name__ == '__main__':
	result=get_hostip_bygroupname('[ZGYGT]秭归医共体HIS生产jboss服务器')
	print result
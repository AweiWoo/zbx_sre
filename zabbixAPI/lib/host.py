#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-15 11:24:11
# @Last Modified by:   wwu
# @Last Modified time: 2021-07-09 11:35:01

from init import zapi
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def get_hostinfo_byid(hostid):
    """
        功能说明：通过主机id获取主机信息
        参数说明：
            hostid：主机id，类型：string
    """
    host_info = zapi.host.get(hostids=hostid,output="extend")
    return host_info

def get_hostid_by_vname(vname):
	"""
		description:
			获取主机id
		arg:
			vname: zabbix上定义的主机名称,类型：str或者list
	"""
	try:
		hosts = zapi.host.get(filter={"name" : vname})
		hostid_list=[]
		hostname_list=[]
		for i in hosts:
			hostid_list.append(i["hostid"])
			hostname_list.append(i["name"])
		items = [item for item in vname if item not in hostname_list]
		if items:
			print "%s 主机不存在" % ', '.join(items)
		return hostid_list
	except ZabbixAPIException as e:
		print e

def get_hostid_by_hname(hname):
	"""
		description:
			获取主机id
		arg:
			hname: zabbix上定义的主机名称,类型：str或者list
	"""
	try:
		hosts = zapi.host.get(filter={"host" : hname})
		hostid_list=[]
		hostname_list=[]
		for i in hosts:
			hostid_list.append(i["hostid"])
			hostname_list.append(i["host"])
		items = [item for item in hname if item not in hostname_list]
		if items:
			print "%s 主机不存在" % ', '.join(items)
		return hostid_list
	except ZabbixAPIException as e:
		print e

def get_hostid_by_group(groupname):
	"""
		功能说明：
			获取组内的所有主机id
		参数说明：
			groupname： 分组名称
		返回值：
			type: 字典 {'hostid': '10105'}
	"""
	try:
		hosts_list = zapi.hostgroup.get(filter={"name" : groupname},selectHosts=groupname)
		if hosts_list:
			return hosts_list[0]['hosts']
		else:
			print "找不到任何主机"
	except Exception as e:
		print e

def add_host_interface(hostid,hostip,type,port,main=1):
	"""
		功能说明：
			添加主机监控接口
		参数说明：
			hostname：主机名称
			type: 接口类型,可选值：1 - agent ， 2 - SNMP , 3 - IPMI , 4 - JMX
			port: 端口号
		返回值：
			type: 列表
	"""
	try:
		add_result = zapi.hostinterface.create(hostid=hostid,dns='',ip=hostip,main=main,port=port,type=type,useip=1)
		return add_result['interfaceids'][0]
	except Exception as e:
		if 'Host cannot have more than one default interface of the same type' in e[0]:
			return 0
		elif 'No default interface' in e[0]:
			return 1

		# -32602: Invalid params., Host cannot have more than one default interface of the same type
		# -32602: Invalid params., No default interface for

# info = get_hostinfo_byid('10305')
# print info

# info = get_hostid_by_hname(['Template_Redis_info_status'])
# print info 

def get_hostinterfaceid(hostid):
    """
        功能说明：通过hostid获取主机接口id
        参数说明：
            hostid:主机id，type:str或list
    """
    info = zapi.hostinterface.get(hostids=hostid)
    return info 

def get_applicationinfo_byname(hostid,appname):
    """
        功能说明：获取主机某个应用集id
        参数说明：
            hostid:主机id,type：list或str
            appname:应用集名称,type：list或str
    """
    info = zapi.application.get(hostids=hostid,filter={"name":appname})
    return info 

def create_application(hostid,appname):
    """
        功能说明：给主机添加一个应用集
        参数说明：
            hostid:主机id,type：list或str
            appname:应用集名称,
    """
    info = zapi.application.create(hostid=hostid,name=appname)
    return info

def host_create(host,ip,name,groupid,port="10050",templates=None):
    """
        功能说明：添加主机到zabbix系统
        参数说明：
            host: 主机的监控名称，与zabbix_agentd.conf中hostname对应，通常为ip地址，类型：str
            name: 监控显示名称，格式通常为[xxxx]-ip-[xxxx]，类型：str
            ip：主机ip地址，类型：str
            port: 监控端口，可选参数，默认10050,类型：str
            groupid：主机分组id,类型:str,这里约定一个主机只绑定一个分组
            templates：模板,类型：dict,例如：{"templateid":"1234"}，此参数可选
    """
    try:
        add_info = zapi.host.create(host=host,
        							name=name,
                                    interfaces=[{"type":1,"main":1,"useip":1,"ip":ip,"dns":"","port":port}],
                                    groups=[{"groupid":groupid}],
                                    templates=templates
                                    )
        return add_info
    except Exception as e:
        error_str=e[0].split(',')[1]
        return {'hostids': [],"error":error_str}


# info = create_application('10547','测试')
# print info['applicationids'] 


# info = get_applicationinfo_byname('10547','端口监控')
# print info[0]['applicationid'] 

# info=get_hostinterfaceid('10693')
# print info

# info = get_hostid_by_vname(["[盛博汇]-192.168.20.204-[zabbix server]"])
# print info 

# info = get_hostinfo_byid('10570')
# print info 

# info = host_create("192.168.10.64","192.168.10.64","[测试]-192.168.10.64-[测试]","107")
# print info 
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-12-24 10:24:34
# @Last Modified by:   wwu
# @Last Modified time: 2021-08-06 11:33:40


from lib.host import get_hostid_by_hname,get_hostid_by_group,add_host_interface
from lib.group import get_hostip_bygroupname


def add_jmx_interface_bygroup(groupname,port,restr):
	"""
		功能说明：
			给分组里面的所有主机添加jmx接口，端口号为2900
		参数说明：
			grouname: 分组名称
	"""
	host_name_ip = get_hostip_bygroupname(groupname)
	for i in host_name_ip:
		host_id = get_hostid_by_hname([i['host_name']])
		ip = i['host_ip'].replace('.'+restr,'')
		result = add_host_interface(host_id[0],ip,4,port)
		if result == 0:
			print "%s JMX接口已经添加，无需再添加" % (i['host_name'])
		elif result == 1:
			print "%s 主机必须要有一个默认接口" % (host)
		else:
			print "%s JMX接口添加成功" % (i['host_name'])

def add_jmx_interface_byhost(hostname,port,restr):
	"""
		功能说明：
			给主机添加jmx接口，端口号为2900
		参数说明：
			grouname: 分组名称
	"""
	for host in hostname:
		host_ip = host.replace('.'+restr,'')
		host_id = get_hostid_by_hname([host])
		result = add_host_interface(host_id[0],host_ip,4,port)
		if result == 0:
			print "%s JMX接口已经添加，无需再添加" % (host)
		elif result == 1:
			print "%s 主机必须要有一个默认接口" % (host)
		else:
			print "%s JMX接口添加成功！" % (host)

def main():
	#给某个分组下面所有主机添加jmx接口，使用端口号为2900
	hostgroup_name = '[TJH]武汉同济IDC生产D环境jboss服务器'
	add_jmx_interface_bygroup(hostgroup_name,2900,'TJH')

	# host_name = ['192.168.8.63.ZGYGT','192.168.8.64.ZGYGT','192.168.8.65.ZGYGT','192.168.8.66.ZGYGT','192.168.8.67.ZGYGT','192.168.8.68.ZGYGT']
	# add_jmx_interface_byhost(host_name,2900,'ZGYGT')

if __name__ == '__main__':
	main()
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-02 15:46:45
# @Last Modified by:   wwu
# @Last Modified time: 2021-08-05 10:39:23

from lib.init import zapi
from lib.host import get_hostid_by_hname,get_hostid_by_group
from lib.group import get_hostip_bygroupname
from lib.sshhost import HostInfo
import re

def update_host_visiblename(hname,newname,groupname,hostname):
	"""	
		功能说明：修改主机别名
		参数：
			hname:主机名称，注意这里指的不是操作系统的主机名称，是zabbix_agentd.conf中定义的hostname,通常是主机的ip地址。
			newname:需要修改的监控主机的显示名称。
	"""
	try:
		host_id = get_hostid_by_hname(hname)[0]
		host_id_list = [ list['hostid'] for list in get_hostid_by_group(groupname) ]
		#判断需要修改名称的主机id是否存在，是否属于对应分组。
		if host_id and host_id in host_id_list:
			update_result = zapi.host.update(hostid=host_id,name=newname,host=hostname)
			return update_result
	except Exception as e:
		print e

def get_os_hostname(ip,host_user,host_passwd):
	"""
		功能说明：获取监控主机的主机名称
		参数：
			ip:监控主机ip地址
			host_user:主机登陆用户
			host_passwd:主机登陆密码
	"""
	h=HostInfo(ip,host_user,host_passwd)
	hname=h.exec_cmd('hostname')
	return hname

def is_ip(ip):
	"""
		功能说明：判断是否是ip地址
	"""
	p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
	if p.match(ip):
		return True
	else:
		return False

def auto_updatebyssh(area_name,host_user,host_passwd,iplist,group_name,project_str):
	"""
		功能说明：通过ssh方式获取主机的主机名称作为后面中括号中的内容来修改主机显示名称。
		参数：
		     area_name：表示区域或者其他自定义内容，通常与分组相关 type:str
		     host_user: 主机登陆账号。 type:str
		     host_passwd: 主机登陆密码。 type:str
		     iplist: 需要修改名称的主机列表。type:list
	"""
	for ip in iplist:
		if is_ip(ip['host_ip']):
			os_name = get_os_hostname(ip['host_ip'],host_user,host_passwd)
			if os_name == 0:
				print "主机%s无法连通" % (ip['host_name'])
			else:
				new_visiblename='[{2}]-{0}-[{1}]'.format(ip['host_ip'],os_name[0],area_name)
				new_host_name='{0}.{1}'.format(ip['host_ip'],project_str)
				result=update_host_visiblename([ip['host_name']],new_visiblename,group_name,new_host_name)
				if result:
	 				print "%s修改为:%s成功" % (ip['host_ip'],new_visiblename)
	 			else:
	 				print "%s修改为:%s失败" % (ip['host_ip'],new_visiblename)
 		else:
 			print "%s 不是一个ip地址" % (ip['host_name'])

def auto_updatebymanual(area_name,host_user,host_passwd,iplist,end_name):
	"""
		功能说明：通过手工方式修改主机显示名称。
		参数：
		     area_name：表示区域或者其他自定义内容，通常与分组相关 type:str
		     host_user: 主机登陆账号。 type:str
		     host_passwd: 主机登陆密码。 type:str
		     iplist: 需要修改名称的主机列表。type:list
		     end_name: 后面中括号中的内容
	"""
	for ip in iplist:
		if is_ip(ip['host_ip']):
			new_visiblename='[{2}]-{0}-[{1}]'.format(ip['host_ip'],end_name,area_name)
			result=update_host_visiblename([ip['host_name']],new_visiblename)
			if result:
 				print "%s修改为:%s成功" % (ip['host_ip'],new_visiblename)
 			else:
 				print "%s修改为:%s失败" % (ip['host_ip'],new_visiblename)
 		else:
 			print "%s 不是一个ip地址" % (ip['host_name'])

def main():
	group_name = '[ZGYGT]秭归医共体互联网医院服务器'
	#批量修改分组下面的主机，要求主机账号密码一致
	group_iplist = get_hostip_bygroupname(group_name)
	auto_updatebyssh('秭归医共体','root','Zgrm@211!',group_iplist,group_name,'ZGYGT')

	#手工修改使用
	# iplist = ['192.168.10.11','192.168.10.12']
	# auto_updatebymanual('测试','root','xxxxx',iplist,'测试')


if __name__ == '__main__':
	main()
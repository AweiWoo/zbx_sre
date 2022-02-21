#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-04 17:09:55
# @Last Modified by:   wwu
# @Last Modified time: 2021-08-05 15:31:28


from lib.init import zapi
from lib.group import get_groupid_bygroupname
from lib.template import get_templateid
from lib.host import get_hostid_by_group,get_hostid_by_hname

def add_template_to_group(templateids,groupid):
	"""
		功能说明：给主机组添加模板
		参数：
			templateids：模板id
			groupid: 主机组id
	"""
	result = zapi.template.massadd(templates=templateids,groups=groupid)
	return result

def add_template_to_host(templateids,hostid):
	"""
		功能说明：给主机添加模板
		参数：
			templateids：模板id
			hostid: 主机d，可以是列表。
	"""
	result = zapi.template.massadd(templates=templateids,hosts=hostid)
	return result

if __name__ == '__main__':
	#给分组下面所有机器添加模板
	t_name = ['Java JMX Generic Template']
	group_name = '[ZGYGT]秭归医共体HIS生产jboss服务器'
	tid=get_templateid(t_name) 
	tid_a = tid['templateid_list']
	tid_b = tid['notin_list']
	if tid_a:
		hosts_id = get_hostid_by_group(group_name)
		add_result=add_template_to_host(tid_a,hosts_id)
		if add_result:
			print "模板添加成功"
	elif tid_b:
		 print "%s 模板不存在" % (tid_b)
	else:
		print "请输入正确的模板名称"

	#给主机添加模板
	# t_name =  ['Java JMX Generic Template']
	# tid = get_templateid(t_name)
	# tid_a = tid['templateid_list']
	# tid_b = tid['notin_list']
	# host_name = ['192.168.8.63.ZGYGT','192.168.8.64.ZGYGT','192.168.8.65.ZGYGT','192.168.8.66.ZGYGT','192.168.8.67.ZGYGT','192.168.8.68.ZGYGT']
	# if tid_a:
	# 	host_id = get_hostid_by_hname(host_name)
	# 	add_result=add_template_to_host(tid_a,host_id)
	# 	if add_result['templateids']:
	# 		print "%s 模板添加成功" % (t_name)
	# elif tid_b:
	# 	print "%s 模板不存在" % (tid_b)
	# else:
	# 	print "添加失败"
	# 	print add_result

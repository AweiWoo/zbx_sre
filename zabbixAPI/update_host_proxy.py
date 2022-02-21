#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-09 09:52:02
# @Last Modified by:   ww
# @Last Modified time: 2019-07-26 10:34:45


from lib.init import zapi
from lib.proxy import get_proxyid
from lib.host import get_hostid_by_group 

def update_proxy_bygroup(groupname,proxyname):

	proxyid = get_proxyid(proxyname)
	hostids = get_hostid_by_group(groupname)
	hostid_list=[]
	for i in hostids:
		hostid_list.append(i['hostid'])

	for id in hostid_list:
		result = zapi.host.update(hostid=id,proxy_hostid=proxyid)
		print result
	
	#proxy.update使用的时候似乎有点bug,给host修改proxy时候，上一个就会消失。
	#update_result =  zapi.proxy.update(proxyid=proxyid,hosts=hostid_list)

	# if update_result['proxyids'][0] == proxyid:
	# 	return "update succeed !"
	# else:
	# 	return "update failed !"

if __name__ == '__main__':
	update_proxy_bygroup('连云港互联互通应用服务器','HIS_Proxy')


#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-09 09:45:26
# @Last Modified by:   ww
# @Last Modified time: 2019-07-09 13:40:08


from init import zapi


def get_proxyid(proxyname):
	"""
		获取代理id
	"""

	info = zapi.proxy.get(filter={'host':proxyname})
	return info[0]['proxyid']

#get_proxyid('HIS_Proxy')
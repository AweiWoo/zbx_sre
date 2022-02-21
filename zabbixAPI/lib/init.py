#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-15 11:22:31
# @Last Modified by:   ww
# @Last Modified time: 2019-08-27 09:36:46

from pyzabbix import ZabbixAPI,ZabbixAPIException

zabbix_server = "http://192.168.20.204/zabbix/"
zabbix_user = "admin"
zabbix_password = "xxxxx"

zapi = ZabbixAPI(zabbix_server)
zapi.login(zabbix_user, zabbix_password)
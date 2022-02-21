#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-04 17:09:07
# @Last Modified by:   wwu
# @Last Modified time: 2021-07-09 11:06:23


from init import zapi
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


# def get_templateid(template_name):
# 	"""
# 		获取模板id
# 	"""
# 	try:
# 		template = zapi.template.get(filter={"host" : template_name})
# 		templates_list=[]
# 		if template:
# 			template_dict =dict(templateid=template[0]['templateid'])
# 			templates_list.append(template_dict)
# 			return templates_list			
# 	except Exception as e:
# 		print e

def get_templateid(templatename):
    """
        说明：通过模板名称获取模板id
        参数说明：
            templatename：模板名称
    """
    try:
        templates = zapi.template.get(filter={"host": templatename})
        templates_list = []
        templatesname_list = []
        for i in templates:
            templates_list.append(i['templateid'])
            templatesname_list.append(i['host'])
        items = [item for item in templatename if item not in templatesname_list]
        templatesid_result = {'templateid_list':templates_list,'notin_list':items}
        return templatesid_result
    except Exception as e:
        error_str=e[0].split(',')[1]
        return {'templateid': [],"error":error_str}


def get_templatename(templateid):
	try:
		info = zapi.template.get(templateids=templateid)
		return info
	except Exception as e:
		print e


def get_iteminfo_byid(itemid):
    """
        功能说明：通过监控项id查询监控信息
        参数说明：
            itemid:监控项id
    """
    item_info = zapi.item.get(itemids=itemid)
    return item_info

# result = get_iteminfo_byid('10305')
# print result

# resut = get_templatename('10305')
# print resut[0]['host']

# name = get_templateid(['Template OS Linux','HIS_Portal'])
# print name
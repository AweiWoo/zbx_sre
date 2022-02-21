#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-05-16 15:28:04
# @Last Modified by:   ww
# @Last Modified time: 2019-07-26 10:33:03
from imp import reload

from lib.init import zapi
from lib.host import get_hostid
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def get_current_alarm(hostname):
    hostid = get_hostid(hostname)
    triggers = zapi.trigger.get(hostids=hostid,
                                    only_true=1,  # 仅返回处于故障状态的触发器
                                    monitored=1,  # 触发器状态为启用
                                    active=1,  # 主机状态为启用
                                    selectHosts=['host','groups'],  # 返回结果中包含主机信息:ip和hostid
                                    output="extend",
                                    expandDescription=1,
                                    selectLastEvent='extend'
                                    )

    # unack_triggers = zapi.trigger.get(only_true=1,
    #                                 skipDependent=1, 
    #                                 monitored=1,
    #                                 active=1,
    #                                 output='extend',
    #                                 expandDescription=1,
    #                                 selectHosts=['host'],
    #                                 selectLastEvent='extend',
    #                                 withLastEventUnacknowledged=1
    #                                 )

    # unack_trigger_ids = [t['triggerid'] for t in unack_triggers]

    # for t in triggers: 
    #     if t['triggerid'] in unack_trigger_ids:
    #         t['unacknowledged'] = True
    #     else:
    #         t['unacknowledged'] = False

    iusse_list=[]
    for t in triggers:
        if t['value'] == "1" and t['lastEvent']:
            iusse_list.append(t)
            # if t['unacknowledged']:
            #      iusse_list.append(t)
    #print current_info

    # current_list = []
    # for c in current_info:
    #     current_dic = {'hostid': c['hosts'][0]['hostid'],
    #                    'name': c['description'],
    #                    'start_clock': c['lastchange'],
    #                    'end_clock': "",
    #                    'severity': c['priority']
    #                    }
    #     current_list.append(current_dic)
    print len(iusse_list)
    print json.dumps(iusse_list, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    get_current_alarm([])

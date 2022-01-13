#!/bin/bash
#脚本名称：difflogChange.sh
#脚本功能：获取日志最后修改时间与系统当前时间对比，得到这个日志多久没有被更新，用于zabbix监控
 
 
fileChangeTime=`stat -c %Y $1`
systemTime=`date +%s`
difftime=$[ $systemTime-$fileChangeTime ]
d=$[ $difftime/60 ]
echo $d

#!/bin/bash
#脚步功能：此脚步用于获取查询文件中的QueryList
#操作方法：sh get_query_list.sh dg_query.props

filename=$1

query_list=$(grep 'Query=' $1 |  awk -F '=' '{ print $1 }' | awk -F '.' '{print $1}' | awk 'BEGIN{ORS=","}{print $0}' | sed 's/,$//')
echo $query_list



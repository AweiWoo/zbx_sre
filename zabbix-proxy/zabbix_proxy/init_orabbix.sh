#!/bin/bash

docker run --name orabbix -d  -e ORB_ZABBIX_LIST="zabbix" -e ORB_ZABBIX_ADDR="192.168.10.214"  -e DB_URL="jdbc:oracle:thin:@192.168.10.89:1521:orcl" -v /opt/conf:/opt/orabbix/conf -v /opt/logs:/opt/orabbix/logs  orabbix:v0.1

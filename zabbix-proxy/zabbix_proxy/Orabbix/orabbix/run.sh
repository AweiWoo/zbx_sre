#!/bin/bash
#author:wwu

export ORABBIX=/opt/orabbix
cd $ORABBIX


CONFILE="./config/config.props"
DEST_CONF="./conf/"

#定义配置文件替换参数
ZabbixList=${ORB_ZABBIX_LIST}
ZabbixAddress=${ORB_ZABBIX_ADDR}
ZabbixPort=${ORB_ZABBIX_PORT:-"10051"}

DBLIST=${DB_LIST:-"DB1"}
DBURL=${DB_URL}
DBUSER=${DB_USER:-"zabbix"}
DBPASSWD=${DB_PASSWD:-"zabbix"}
DBQueryFile=${DB_QueryFile:-"./config/query.props"}

#修改配置文件
config_orabbix_file()
{
	#修改ZabbixServerList
	sed -i  "/^ZabbixServerList=/s/=.*/=${ZabbixList}/" ${CONFILE}
	
	#增加修改ZabbixServerList的ip地址和端口
	sed -i "/^ZabbixServerList=/a\\${ZabbixList}.Address=${ZabbixAddress}\\n${ZabbixList}.Port=${ZabbixPort}" ${CONFILE}

	#修改DatabaseList
	sed -i  "/^DatabaseList=/s/=.*/=${DBLIST}/" ${CONFILE}

	echo "${DBLIST}.Url=${DBURL}" >> ${CONFILE}
	echo "${DBLIST}.User=${DBUSER}" >> ${CONFILE}
	echo "${DBLIST}.Password=${DBPASSWD}" >> ${CONFILE}
 	echo "${DBLIST}.QueryListFile=${DEST_CONF}/query.props" >> ${CONFILE}
}

#启动进程
start_orabbix()
{
	java -Duser.language=en -Duser.country=US -Dlog4j.configuration=./config/log4j.properties -cp $(for i in lib/*.jar ; do echo -n $i: ; done).:./orabbix-1.2.3.jar com.smartmarmot.orabbix.bootstrap start ./conf/config.props 
}



if [ ! -f ${DEST_CONF}/config.props ]; then 
	config_orabbix_file
	if [ $? -eq 0 ]; then
		cp ${CONFILE} ${DEST_CONF}
		cp ${DBQueryFile} ${DEST_CONF}
		start_orabbix
	else
		echo "config file is failed !"
	fi
else
	start_orabbix
fi

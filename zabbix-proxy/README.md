# 1 说明

此项目是用来安装zabbix proxy的docker容器版本。详细文档可以参考：
http://wiki.cenboomh.com:88/pages/viewpage.action?pageId=44469637


# 2 使用说明

## 2.1 修改配置

下载zabbix_proxy，按实际情况修改想配置


指定镜像的来源：
```
image: docker.cenboomh.com/sre/zabbix-proxy-mysql:centos-4.0 
```

指定容器名称：
```
container_name: zabbix_docker_proxy
```

根据实际情况调整参数：
```
environment:
          DB_SERVER_HOST: 192.168.10.214   #数据库地址
          MYSQL_USER: "zabbix"             #数据库用户
          MYSQL_PASSWORD: "Zabbix123!"     #数据库密码
          ZBX_HOSTNAME: "test_docker_proxy"  #zabbix_proxy.conf中hostname
          ZBX_SERVER_HOST: "192.168.20.204"  #zabbix_proxy.conf中server
          ZBX_CONFIGFREQUENCY: "60"          
          ZBX_DATASENDERFREQUENCY: "5"       
```

mysql相关参数 
````
environment:
          MYSQL_DATABASE: "zabbix_proxy"  #数据库名称
          MYSQL_USER: "zabbix"            #数据库用户
          MYSQL_PASSWORD: "Zabbix123!"    #数据库码密码
          MYSQL_ROOT_PASSWORD: "Root123!" #数据库root密码
```

## 2.2 执行安装语句
```
cd docker_proxy
docker-compose -f docker-compose.yml  up -d
```

## 2.3 关于orabbix配置说明
orabbix使用来监控orabbix数据库的插件，在orabbix的容器启动后，在系统的/opt目录下面会映射一个conf目录，里面有orabbix需要的配置文件。主要有两种类型的配置的配置文件：  
### 1）config.props  
文件里面主机配置需要监控的数据库的连接字符串。  
### 2）以.props的文件  
此文件里面主要记录的是查询sql语句。在此项目的Orabbix_conf/query/下面存放了相关标准sql文件，主要分为三类：
```
singleInstances_query.props:用来监控单实例的数据库  
rac1_query.props,rac2.props:用来监控RAC集群数据库  
dg_query.props:用来监控DG数据库  
 ```
以上文件分为oracle11g和oracle12c两个版本，分别放在对应目录
### 3) 修改修改的部分
监控查询语句，有些地方可以根据实际情况：
再使用到ASM管理使用裸设备的时候，ASM中空间使用率和归档日志使用率查询语句中的where条件中的名称需要根据实际情况修改
指标名称：  
```
asm_free.Query=select to_char(free_mb,'FM99999999999999990') as free_disk from v$asm_diskgroup where name='DATADG' 
asm_used.Query=select to_char(TOTAL_MB - FREE_MB,'FM99999999999999990') as used_disk from v$asm_diskgroup where name='DATADG 
asm_arch_used.Query=select round(((t.total_mb-t.free_mb)/t.total_mb)*100,2) as ARCHDG_PERC  from v$asm_diskgroup t where t.name = 'ARCHDG' 
```

### 一、说明
    
    使用ansible role 免编译批量安装zabbix agentd 客户端脚本程序。
    使用操作系统版本：Centos6 
    ansible版本：2.0 +
    
### 二、使用方法
    
    1、修改var/main.yml文件
   
    zabbix_version: 3.2.0.linux2_6_23.amd64   #zabbix客户端版本
    zabbix_dir: /etc/zabbix                   #zabbix安装目录
    zabbix_user: zabbix                       #zabbix运行用户（脚本自动创建）
    zabbix_port: 10050                        #zabbix运行端口
    zabbix_server_ip: 172.20.2.101            #zabbix server或者proxy 地址
    redis_server: ['192.168.10.113','192.168.10.114']    #redis集群地址
    zookeeper_server: ['192.168.10.100','192.168.10.101','192.168.10.102'] #zookeeper集群地址

    
    2、将脚本包上传到ansible的role目录
    
    3、执行下面命令进行批量安装
    
    ansible-playbook zabbix_agent_install.yml -e "host=xxxxx" -u root -k xxxxx
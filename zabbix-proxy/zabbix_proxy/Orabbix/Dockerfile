FROM docker.cenboomh.com/sre/jdk1.8:latest

RUN	mkdir /opt/orabbix
COPY ["orabbix/","/opt/orabbix/"]
VOLUME ["/opt/orabbix/conf","/opt/orabbix/logs"]
WORKDIR "/opt/orabbix/"
CMD  ["./run.sh"]
#!/bin/bash

ps -ef | grep zabbix | grep -v grep | awk '{ print $2 }' | xargs kill -9

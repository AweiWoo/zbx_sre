#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Awei Woo
# @Date:   2019-07-02 15:44:41
# @Last Modified by:   ww
# @Last Modified time: 2019-07-04 10:55:19

import sys,os
import paramiko
from paramiko.ssh_exception import NoValidConnectionsError
from paramiko.ssh_exception import AuthenticationException

class HostInfo:

	def __init__(self,ip,user_name,pass_word,):
		self.ip = ip
		self.user_name = user_name
		self.pass_word = pass_word
		#transport和chanel
		self.ssh = ''
		self.chan = ''

	def conn_host(self):
		try:
			self.ssh = paramiko.SSHClient()
			self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			self.ssh.connect(self.ip,22,self.user_name,self.pass_word,timeout=10)
			#self.chan = self.ssh.get_transport().open_session()
			return self.ip
		except Exception as e:
			print e
			return "Error"

	def close_host(self):
		self.chan.close()
		self.ssh.close()

	def exec_cmd(self,cmd):

		try:
			if self.conn_host() == 'Error':
				return 0
			else:
				stdin,stdout,stderr = self.ssh.exec_command(cmd)
				result = stdout.read().splitlines()
				return result
				# self.chan.exec_command(cmd)
				# return self.chan.recv(1024)
			self.close_host()
		except Exception as e:
			print e


# host=HostInfo('172.20.2.52','root','test!')
# #print host.conn_host()
# print host.exec_cmd('hostname')



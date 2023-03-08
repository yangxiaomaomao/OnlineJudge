'''
Author: your name
Date: 2021-08-09 18:19:26
LastEditTime: 2021-08-13 11:57:48
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \sunConnect\killPort.py
'''
import commands
import os

from conf import globalConf
from conf.globalConf import * 

_, output = commands.getstatusoutput('lsof -i:{} | grep python'.format(globalConf.SOCKET_PORT))
pid = output.split()[1]
os.system("sudo kill -9 {pid}".format(pid = pid))

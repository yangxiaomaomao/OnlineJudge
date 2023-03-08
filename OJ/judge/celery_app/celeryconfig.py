'''
Author: your name
Date: 2021-07-29 17:06:39
LastEditTime: 2021-08-12 22:25:18
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \yjb\celery_app\celeryconfig.py
'''
import sys
sys.path.append("..")
from conf import globalConf


redisIp = globalConf.REDIS_IP
redisPort = globalConf.REDIS_PORT
redisPasswd = globalConf.REDIS_PASSWD

broker_url = "redis://:{passwd}@{ip}:{port}".format(ip = redisIp,port = redisPort,passwd = redisPasswd)

result_backend = "redis://:{passwd}@{ip}:{port}/0".format(ip = redisIp,port = redisPort,passwd = redisPasswd)

result_serializer = 'json'

task_reject_on_worker_lost = True

result_expires = 24 * 60 * 60

timezone = "Asia/Shanghai"

imports = (
    "celery_app.task"
)
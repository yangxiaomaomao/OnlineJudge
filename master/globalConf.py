'''
Author: your name
Date: 2021-08-12 21:14:24
LastEditTime: 2021-10-08 13:07:26
LastEditors: Jingbin Yang
Description: In User Settings Edit
FilePath: \sunConnectyy\celery_app\global.py
'''

#REDIS
REDIS_IP     = "192.168.3.43"
REDIS_PORT   = "6380"
REDIS_PASSWD =  "kGhl@Fdskga"

#SOCKET
SOCKET_IP             = "127.0.0.1"
SOCKET_PORT           = 7777
SOCKET_MAX_CONN       = 100
SOCKET_MAX_RECBYTES   = 1024

#POST_URL
POST_URL = "http://localhost:8080/OnlineJudge/contest/setStatus"

#FILE_RELATED
# if RM_ORIGIN is True, it means that when we finish scoring the specific homework,
# the origin zip_file, which is defined by the json_key "filePath", will be removed, 
# you can find the directory which used to be the origin zip in the directory ./archive/expId/userId
# 
# if RM_PRIGIN is False,it means we don't remove the origin zip, it will still exist in the filePath 
RM_ORIGIN = True

# The path of the code which is uploaded by each student last time
# It supports multiple directory mkdir
CODELIBPATH = "/archive/"

# CODEPATH = "/home/yangxiaomao/shared/sunConnectyy/archive/code"

# RESULTPATH = "/home/yangxiaomao/shared/sunConnectyy/archive/result"

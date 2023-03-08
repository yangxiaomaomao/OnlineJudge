'''
Author: your name
Date: 2021-07-29 17:31:29
LastEditTime: 2021-10-01 09:24:44
LastEditors: Jingbin Yang
Description: In User Settings Edit
FilePath: \yjb\client.py
'''

from FIXED import preprocess
from conf import globalConf
from celery_app import task
import threading
import redis
import urllib2
import os
import socket
import json
from FIXED.preprocess import *
from conf.globalConf import * 
from celery.result import AsyncResult
import time
import logging

global taskList
taskList = []
sig = 0

reload(sys)
sys.setdefaultencoding('utf8')  

# This is the directory of the last-upload homework

def saveArchives(expId,userId,filePath):
    archiveDir = globalConf.CODELIBPATH
    if not os.path.isdir(archiveDir):
        os.makedirs(archiveDir)

    expDir = os.path.join(archiveDir,expId)
    if not os.path.isdir(expDir):
        os.mkdir(expDir)

    standardDir = os.path.join(expDir,"standard")
    if not os.path.isdir(standardDir):
        os.mkdir(standardDir)
    
    codeDir = os.path.join(expDir,"code")
    if not os.path.isdir(codeDir):
        os.mkdir(codeDir)

    resultDir = os.path.join(expDir,"result")
    if not os.path.isdir(resultDir):
        os.mkdir(resultDir)
        
    # We first create the temp dir to save the UNstandard zip 
    # and decompress the zip into it
    userTempDir = os.path.join(expDir,"id" + userId + "_temp")
    if not os.path.isdir(userTempDir):
        os.mkdir(userTempDir)

    preprocess.decompress(filePath,userTempDir)

    # If the userDir has existed, we remove all of it
    userDir = os.path.join(expDir,"id" + userId)
    if os.path.isdir(userDir):
        shutil.rmtree(userDir)
    # Find makefile path
    makefilePath = preprocess.findMakefilePath(userTempDir)
    
    if not makefilePath:
        os.mkdir(userDir)
    else:
        shutil.copytree(makefilePath,userDir)

    shutil.rmtree(userTempDir)

    if globalConf.RM_ORIGIN == True:
        if(os.path.exists(filePath)):
            os.remove(filePath)

def writeLog(log,extraInfo = ""):
    with open("master.log","a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()))
        f.write(extraInfo)
        f.write(log)
        f.write("\n")

def monitorTask():
    # to Sun if you have changed redis configuration, here you can change ip,port,password
    r = redis.Redis(host=globalConf.REDIS_IP,port=globalConf.REDIS_PORT,password=globalConf.REDIS_PASSWD,health_check_interval=30)
    url = globalConf.POST_URL
    while(1): 
        for item in taskList:
            result = AsyncResult(id=item.id, app=task.sendCmdToWorker)
            try: 
                if(result.successful()):
                    try:
                        info = json.loads(item.get())
                    except Exception as err:
                        taskList.remove(item)
                        r.delete("celery-task-meta-{}".format(item.id))
                        writeLog("err:{err}\ntaskId:{taskId}".format(err = err,taskId = item.id))
                    expId = info["expId"]
                    userId = info["userId"]
                    filePath = info["filePath"]
                    del info["filePath"]
                    # We only save the file which is uploaded latest
                    saveFunc = threading.Thread(target = saveArchives,args=(expId,userId,filePath),name = "saveArchives")
                    saveFunc.start()

                    data = {
                        'code': 500,
                        'message': '',
                    }
                    data = json.loads(json.dumps(data))
                    data['data'] = item.get()
                    print("item.get() ",item.get())
                    data = json.dumps(data)
                    print("yjbdata",data)
                    post = urllib2.Request(url = url,data = data, headers={"Content-Type" : "application/json;charset=UTF-8"})
                    
                    #TODO to be handled
                    response = urllib2.urlopen(post)
                    writeLog(item.get(),"Return data:")

                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    print(item.get())
                    #to avoid the list of redis is too long
                    r.delete("celery-task-meta-{}".format(item.id))
                    taskList.remove(item)
                elif result.failed():
                    print("{id} exec failed".format(id = item.id))
                    continue
            except Exception as err:
                taskList.remove(item)
                r.delete("celery-task-meta-{}".format(item.id))
                writeLog("err:{err}\ntaskId:{taskId}".format(err = err,taskId = item.id))


def receivePathAndId():
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.bind((globalConf.SOCKET_IP,globalConf.SOCKET_PORT))
    sock.listen(globalConf.SOCKET_MAX_CONN)
    while(1):
        print("Waiting......({}:{})".format(globalConf.SOCKET_IP,globalConf.SOCKET_PORT))
        conn,addr      = sock.accept()
        data           = conn.recv(globalConf.SOCKET_MAX_RECBYTES)
        writeLog(data,"Recevie data:")
        print("llllllllllllll",data)
        hwData         = json.loads(data)
        fileId         = hwData["fileId"]
        expId          = hwData["expId"]
        userId         = hwData["userId"]
        filePath       = os.path.join(globalConf.CODELIBPATH, "zip", hwData["filePath"])

        taskList.append(task.sendCmdToWorker.delay(fileId,expId,userId,filePath))
        conn.close()

if __name__ == "__main__":
    # task.sendCmdToWorker.delay(1,1,1,"/archive/zip/361.zip")
    # task.sendCmdToWorker.delay(1,1,1,"/archive/zip/364.zip")
    monitor = threading.Thread(target = monitorTask,name = "monitorTask")
    receive = threading.Thread(target = receivePathAndId,name = "receivePathAndId")
    
    monitor.start()
    receive.start()
    #Avoid the monitor thread terminates unexpectedly
    while(1):
        if monitor.isAlive() == False:
            writeLog("Thread terminates due to some unknown reasons,restarting......","Restarting")
            print("Thread terminates due to some unknown reasons,restarting......")
            monitor = threading.Thread(target = monitorTask,name = "monitorTask")
            monitor.start()
        time.sleep(2)



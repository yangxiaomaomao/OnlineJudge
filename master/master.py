# --coding:utf-8--
import socket
import json 
import threading  

import sys
from queue import Queue 
import time
import os 
import requests
import preprocess 
import globalConf
import shutil 
import importlib

# sudo scp yangxiaomao@192.168.2.151:/home/yangxiaomao/worker/mininetTopo.py . && ./run_worker.sh
# sudo scp yangxiaomao@192.168.2.151:/home/yangxiaomao/worker/main.py . && chmod 777 main.py && ./run_worker.sh
# 记得改地址啊
# cd && rm -rf worker && rm -f worker.zip && sudo scp yangxiaomao@192.168.2.151:/home/yangxiaomao/worker.zip . && unzip worker.zip && chmod 777 -R worker && cd worker && ./run_worker.sh
# cd /etc/apt && sudo scp yangxiaomao@192.168.2.151:/home/yangxiaomao/sources.list . && sudo apt update && sudo apt install libssl1.1=1.1.1f-1ubuntu2.12 && sudo apt install libssl-dev
FREE = 0
BUSY = 1 
MAX_QUEUE_SIZE = 65535
DEQUEUE_INTERVAL = 0.5
POST_URL = "http://localhost:8080/OnlineJudge/contest/setStatus"

master_ip = "192.168.0.230"

workerList = [  
    {"ip": "192.168.0.230", "port": 9999, "state": FREE},
    {"ip": master_ip,       "port": 9999, "state": FREE},
]
# receive json type task
taskQueue = Queue(maxsize=MAX_QUEUE_SIZE)
# importlib.reload(sys)
# sys.setdefaultencoding("utf-8")


def writeLog(log, extraInfo=""):
    with open("master.log", "a") as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime()))
        f.write(extraInfo)
        f.write(log)
        f.write("\r\n")


def setWorkerFree(ip):
    print(ip)
    for worker in workerList:
        if worker["ip"] == ip:
            worker["state"] = FREE


def getFreeWorkerAndSetBusy():
    for worker in workerList:
        if worker["state"] == FREE:
            worker["state"] = BUSY
            return worker["ip"], worker["port"]
    return None, None


def saveArchives(expId, userId, filePath):
    archiveDir = globalConf.CODELIBPATH
    if not os.path.isdir(archiveDir):
        os.makedirs(archiveDir)

    expDir = os.path.join(archiveDir, expId)
    if not os.path.isdir(expDir):
        os.mkdir(expDir)
        os.system("sudo chmod 777 -R {}".format(expDir))

    standardDir = os.path.join(expDir, "standard")
    if not os.path.isdir(standardDir):
        os.mkdir(standardDir)

    codeDir = os.path.join(expDir, "code")
    if not os.path.isdir(codeDir):
        os.mkdir(codeDir)

    resultDir = os.path.join(expDir, "result")
    if not os.path.isdir(resultDir):
        os.mkdir(resultDir)

    # We first create the temp dir to save the UNstandard zip
    # and decompress the zip into it
    userTempDir = os.path.join(expDir, "id" + userId + "_temp")
    if not os.path.isdir(userTempDir):
        os.mkdir(userTempDir)

    preprocess.decompress(filePath, userTempDir)

    # If the userDir has existed, we remove all of it
    userDir = os.path.join(expDir, "id" + userId)
    if os.path.isdir(userDir):
        shutil.rmtree(userDir)
    # Find makefile path
    makefilePath = preprocess.findMakefilePath(userTempDir)

    if not makefilePath:
        os.mkdir(userDir)
    else:
        shutil.copytree(makefilePath, userDir)

    shutil.rmtree(userTempDir)

    if globalConf.RM_ORIGIN == True:
        if(os.path.exists(filePath)):
            os.remove(filePath)
            writeLog(filePath, "Remove the file ")
# msg should be a json type


def sendMsgTo(ip, port, msg):
    try:
        print(ip,port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))
    except socket.error as msg:
        print(msg)
        sys.exit(1)
    print("I am sending msg to {}:{}".format(ip, port))
    s.send(msg.encode())
    s.close()

# get path from lyg and enqueue


def receivePathAndEnqueue():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", 7777))
        s.listen(20)
        print("127.0.0.1:7777 listening......")
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    while 1:
        conn, addr = s.accept()
        data = conn.recv(1024)
        data = json.loads(data)
        # get the full path of file
        data["filePath"] = os.path.join("/archive/zip", data["filePath"])
        # data type : json
        taskQueue.put(json.dumps(data, indent=4, ensure_ascii=False))
        writeLog(json.dumps(data, indent=4, ensure_ascii=False), "EnqueueData ")
        conn.close()


def DequeueTaskAndDeliver():
    while 1:
        if taskQueue.empty() == False:
            print("not empty queue")
            ip, port = getFreeWorkerAndSetBusy()
            if ip == None and port == None:
                print("No free worker, waiting......")
            else:
                print("deliver task to ", ip, port)
                data = taskQueue.get()
                writeLog(data, "DequeueData delivered to {}:{}".format(ip, port))
                sendMsgTo(ip, port, data)

        time.sleep(DEQUEUE_INTERVAL)


def receiveResultAndSendback():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", 4320))
        s.listen(20)
        print("192.168.0.230:4320 listening......")
    except socket.error as msg:
        print("4320", msg)
        sys.exit(1)

    while 1:
        conn, addr = s.accept()
        try:
            data = conn.recv(65535)
            rawData = data
            print(data)
            data = json.loads(data)
        except Exception as msg:
            print("recv and load error")
            print(msg)
            sys.exit(1)
        workerIP = data["ip"]
        expId    = data["expId"]
        userId   = data["userId"]
        filePath = data["filePath"]
        writeLog(rawData.decode(), "ReceiveResult ")
        del data["ip"]
        del data["filePath"]
        # We only save the file which is uploaded latest
        setWorkerFree(workerIP)
        saveFunc = threading.Thread(target=saveArchives, args=(
            str(expId), userId, filePath), name="saveArchives")
        saveFunc.start()

        response = {
            "code": 500,
            "message": '',
            "data":rawData.decode()
        }
        response = json.dumps(response)
        print("response to sun ", response)

        post = requests.post(url=POST_URL, data=response, headers={
                               "Content-Type": "application/json;charset=UTF-8"})
        # urllib2.urlopen(post)
        writeLog(response, "ReturnSun ")
        conn.close()


def main():
    receiveTaskAndEnqueueThread = threading.Thread(
        target=receivePathAndEnqueue)
    DequeueTaskAndDeliverThread = threading.Thread(
        target=DequeueTaskAndDeliver)
    receiveResultAndSendbackThread = threading.Thread(
        target=receiveResultAndSendback)

    receiveTaskAndEnqueueThread.start()
    DequeueTaskAndDeliverThread.start()
    receiveResultAndSendbackThread.start()

    if receiveTaskAndEnqueueThread.is_alive() == False:
        receiveTaskAndEnqueueThread = threading.Thread(
            target=receivePathAndEnqueue)
        receiveTaskAndEnqueueThread.start()
    if DequeueTaskAndDeliverThread.is_alive() == False:
        DequeueTaskAndDeliverThread = threading.Thread(
            target=DequeueTaskAndDeliver)
        DequeueTaskAndDeliverThread.start()
    if receiveResultAndSendbackThread.is_alive() == False:
        receiveResultAndSendbackThread = threading.Thread(
            target=receiveResultAndSendback)
        receiveResultAndSendbackThread.start()


if __name__ == "__main__":
    main()

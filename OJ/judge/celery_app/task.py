'''
Author: your name
Date: 2021-07-29 17:06:39
LastEditTime: 2021-10-08 13:07:54
LastEditors: Jingbin Yang
Description: In User Settings Edit
FilePath: \yjb\celery_app\task.py
'''

from celery_app import app
import os
import time
masterAddr = "yangxiaomao@192.168.3.43"
@app.task
#TODO add parameter
def sendCmdToWorker(fileId,expId,userId,filePath):
    #TODO scp file from master to worker
    # if not os.path.exists("./FIXED/test/"):
    #     os.system("mkdir ./FIXED/test/")
    # os.system("sudo scp -r {masterAddr}:{filePath} ./FIXED/test/".format(masterAddr = masterAddr, filePath = filePath))
    # #TODO avoid time too long
    # time.sleep(0.5)
    # #TODO solve the sudo and passwd issues
    # os.system("cd FIXED && sudo python main.py {fileId} {expId} {userId} {filePath}".format(fileId = fileId,expId = expId,userId = userId,filePath = filePath))
    # #os.system("cd FIXED && sudo python main.py")
    # with open("./FIXED/result.json","r") as f:
    #     retJson = f.read()
    # os.system("rm -f ./FIXED/result.json")
    # os.system("rm -rf ./FIXED/test/")
    time.sleep(3)
    return retJson

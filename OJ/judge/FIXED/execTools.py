'''
Author: your name
Date: 2021-08-09 21:26:51
LastEditTime: 2021-10-01 13:57:21
LastEditors: Jingbin Yang
Description: In User Settings Edit
FilePath: \sunConnectyy\FIXED\execTools.py
'''
import os
import time
import logging
import config
import collections
import preprocess

from mininet.net import Mininet
from mininet.link import TCLink

decompressPath = config.getDecompressPath()
downloadDir = config.getDownDir()
 
def downloadFiles(host,addr,fileList,savePath):
    if addr[-1] != "/":
        addr = addr + "/"

    if not os.path.isdir(savePath):
        os.mkdir("./{}".format(savePath))

    succeedDownFileNames = []

    for file in fileList:
        print("wget -O {}/{} {}{}".format(savePath,file,addr,file))
        ret = host.cmd("wget -O {}/{} {}{}".format(savePath,file,addr,file))
        print(ret)
        if "100%" in ret:
            logging.info("{} download success".format(file))
            succeedDownFileNames.append(file)
        else:
            logging.info("{} can't be downloaded for some reasons".format(file))
    return succeedDownFileNames

def getMd5(host, path_to_file):
    ret = host.cmd("md5sum {}".format(path_to_file))
    md5 = ret.split()[0]
    return md5

def compareMd5(host,file1,file2):
    file1Md5 = getMd5(host,file1)
    file2Md5 = getMd5(host,file2)
    return True if file1Md5 == file2Md5 else False
    
def compareMd5Dirs(host,dir1,dir2,file_names):
    result = []
    for file in file_names:
        src1 = dir1+file
        src2 = dir2+file
        print("src",src1,src2)
        result.append(compareMd5(host,src1,src2))
    return result
def getScore(h1,h2,exeFile,makefilePath):
    scores = {"testCase":5,"passedCase":0}
    time.sleep(0.5)
    h1.cmd("{} &".format(exeFile))
    time.sleep(1)

    planDownloadFileNames = ["index.html","10K.dat","100K.dat","1M.dat","10M.dat"]

    succeedDownFileNames = downloadFiles(h2,"http://10.0.0.1/",planDownloadFileNames,"{}/{}".format(makefilePath,downloadDir))

    print("success",succeedDownFileNames)

    verifyResult = compareMd5Dirs(h2, "{}/{}/".format(makefilePath,downloadDir), "./www/", succeedDownFileNames)

    points = len([i for i in verifyResult if i])

    scores["passedCase"] = points

    return scores

def judger(topo,exeFile,makefilePath):
    preprocess.checkScripts()
    
    net = Mininet(topo = topo,link = TCLink,controller = None)

    h1,h2 = net.get("h1","h2")

    h1.cmd("ifconfig h1-eth0 10.0.0.1/24")
    h2.cmd("ifconfig h2-eth0 10.0.0.2/24")

    for h in (h1,h2):
        h.cmd('scripts/disable_ipv6.sh')
        h.cmd('scripts/disable_offloading.sh')
        h.cmd('scripts/disable_tcp_rst.sh')
    
    net.start()

    result = getScore(h1,h2,exeFile,makefilePath)

    net.stop()
    return result
def initDbInfo(fileId,expId,userId,filePath): 
    dbInfo = collections.OrderedDict()
    dbInfo["fileId"] = fileId 
    dbInfo["expId"] = str(expId) 
    dbInfo["userId"] = userId
    dbInfo["filePath"] = filePath
    dbInfo["status"] = None 
    dbInfo["statusDescr"] = None 
    dbInfo["test"] = None
    return dbInfo


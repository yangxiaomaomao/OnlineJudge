# -*- coding: utf-8 -*-
'''
Author: your name
Date: 2021-08-09 20:39:06
LastEditTime: 2021-10-01 09:56:57
LastEditors: Jingbin Yang
Description: In User Settings Edit
FilePath: \sunConnectyy\FIXED\main.py
cdsssssssssssscs  fsd fsdfs
'''
import os
import sys
import shutil
import config
import json
import execHomework
import preprocess
import execTools
import time

decompressPath = config.getDecompressPath()
downloadDir = config.getDownDir()

reload(sys)
sys.setdefaultencoding("utf-8")

preprocessFailCode = config.getExecFailCode()

def main(fileId,expId,userId,filePath):
    preprocess.removeFiles(decompressPath)

    dbInfo = execTools.initDbInfo(fileId,expId,userId,filePath)
    filePath = os.path.join("test",os.path.basename(filePath))
    if not preprocess.decompress(filePath,decompressPath):
        preprocess.removeFiles(decompressPath)
        dbInfo["status"] = preprocessFailCode
        dbInfo["statusDescr"] = "解压失败，请上传正确的文件格式"
        return dbInfo

    makefilePath = preprocess.findMakefilePath(decompressPath)

    if not makefilePath:
        preprocess.removeFiles(decompressPath)

        dbInfo["status"] = preprocessFailCode
        dbInfo["statusDescr"] = "没有检测到Makefile"
        return dbInfo

    shutil.copyfile("./Makefile","{}/Makefile".format(makefilePath))

    makeResult = preprocess.compileMakefile(makefilePath)
    print("makefilePath:",makefilePath)
    if not makeResult:
        preprocess.removeFiles(decompressPath)
        
        dbInfo["status"] = preprocessFailCode
        dbInfo["statusDescr"] = "编译失败"
        return dbInfo

    targetName = preprocess.getTargetName(makefilePath)

    os.system("chmod u+x {}/{}".format(makefilePath,targetName))

    '''
    There you can add other kinds of homework e.g. homework1()
    The definition of the homewwork1() are strongly recommanded 
    in the file "./execHomework.py", among all kinds of homework, 
    the value of expId is the key. 
    '''
    if expId == 1:
        execHomework.homework1(dbInfo,makefilePath,targetName)
    else:
        execHomework.homework1(dbInfo,makefilePath,targetName)
    
    return dbInfo

if __name__ == "__main__":
    dbInfo = main(
                fileId = sys.argv[1],
                expId = int(sys.argv[2]),
                userId = sys.argv[3],
                filePath = sys.argv[4]
            )
    with open("../workerlog.log","a") as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S\n',time.localtime(time.time())))

        f.write(json.dumps(dbInfo,indent = 4,ensure_ascii=False))
        f.write("\n")
    with open("result.json","w") as f:
        f.write(json.dumps(dbInfo,indent = 4,ensure_ascii=False))


'''
Author: your name
Date: 2021-08-09 20:39:06
LastEditTime: 2021-10-01 09:59:26
LastEditors: Jingbin Yang
Description: In User Settings Edit
FilePath: \sunConnectyy\FIXED\preprocess.py
'''
import os

import fnmatch
import glob
import sys
import re
import shutil
decompressPath = "decompressDir"
downloadDir = "downloadDir"

script_deps = ['ethtool', 'arptables', 'iptables']
def removeFiles(decompressPath):
    if os.path.exists(decompressPath):
        os.system("rm -rf {}".format(decompressPath))
    
def getFileType(fileName):
    return fileName.split(".")[-1]

def decompressZipAnd7z(fileName,decompressPath):
    os.system("7z x {} -o{}".format(fileName,decompressPath))
def decompressRar(fileName,decompressPath):
    os.system("unrar x {} {}".format(fileName,decompressPath))

def decompress(fileName,decompressPath):
    fileType = getFileType(fileName)
    print("filetype",decompressPath)
    if fileType == "tar" or fileType == "zip":
        decompressZipAnd7z(fileName,decompressPath)
        return True
    elif fileType == "rar":
        decompressRar(fileName,decompressPath)
        return True
    else:
        return False

def findMakefilePath(dirName):
    for dirPath,dirNames,fileName in os.walk(dirName):
        if len(fnmatch.filter(fileName, "Makefile")) > 0:
            return dirPath
    return None
def checkScripts():
    dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    for fname in glob.glob(dir + '/' + 'scripts/*.sh'):
        if not os.access(fname, os.X_OK):
            print('%s should be set executable by using `chmod +x $script_name`' % (fname))
            sys.exit(1)

    for program in script_deps:
        found = False
        for path in os.environ['PATH'].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if os.path.isfile(exe_file) and os.access(exe_file, os.X_OK):
                found = True
                break
        if not found:
            print('`%s` is required but missing, which could be installed via `apt` or `aptitude`' % (program))
            sys.exit(2)
def compileMakefile(makefilePath):
    print("make -C {}".format(makefilePath))
    return True if os.system("make -C {}".format(makefilePath)) == 0 else False

def isTargetLine(line):
    return True if re.match("\s*TARGET.*=",line) else False

def getTargetName(makefilePath):
    makefileF = makefilePath + "/Makefile"
    targetName = None
    with open(makefileF,"r") as f:
        for line in f.readlines():
            if(isTargetLine(line)):
                targetName = line.strip().split("=")[1].strip()
    return targetName
# WARNING: Please use the function very cautiously 
def clearDirContent(dir):
    fileList = os.listdir(dir)
    for f in fileList:
        filePath = os.path.join(dir,f)
        if os.path.isfile(filePath):
            os.remove(filePath)
        elif os.path.isdir(filePath):
            shutil.rmtree(filePath)

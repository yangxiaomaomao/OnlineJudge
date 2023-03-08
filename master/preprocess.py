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


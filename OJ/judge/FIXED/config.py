'''
Author: your name
Date: 2021-08-03 12:09:18
LastEditTime: 2021-08-12 11:32:09
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \yjb\FIXED\config.py
'''
import sys
if sys.version_info < (3,0):
    import ConfigParser
else:
    import configparser as ConfigParser

cf = ConfigParser.ConfigParser()
cf.read("config.conf")

def getDecompressPath():
    return cf.get("PATH","decompressPath").replace("\"","")
def getDownDir():
    return cf.get("PATH","downloadDir").replace("\"","")
def getExecFailCode():
    return cf.get("STATUS_CODE","execFail").replace("\"","")
def getAllPassedCode():
    return cf.get("STATUS_CODE","allPassed").replace("\"","")
def getSolveFailCode():
    return cf.get("STATUS_CODE","solveFail").replace("\"","")
    #return cf.get("REDIS","ip").replace("\"","")

#TO ADD CONSTANT
    
    
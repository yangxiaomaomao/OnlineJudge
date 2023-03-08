# -*- coding:UTF-8 -*-
import config
import preprocess

from mininetTopo import TCPGeneralTopo
from mininetTopo import TCPLossTopo
import execTools

decompressPath = config.getDecompressPath()
downloadDir = config.getDownDir()

def homework1(dbInfo,makefilePath,targetName):
    GeneralTopo = TCPGeneralTopo()
    LossTopo = TCPLossTopo()
    print(makefilePath,targetName)
    # students result
    scores = {"GeneralTopo":None,"LossTopo":None}

    for (casename, topo) in [("GeneralTopo",GeneralTopo),("LossTopo",LossTopo)]:
        scores[casename] = execTools.judger(topo,"{}/{}".format(makefilePath,targetName),makefilePath)
      
    if scores["GeneralTopo"]["testCase"] == scores["GeneralTopo"]["passedCase"] and\
       scores["LossTopo"]["testCase"] == scores["LossTopo"]["passedCase"]:
        #dbInfo["status"] = config.getAllPassedCode()
        dbInfo["status"] = "100"
    else:
        dbInfo["status"] = "300"
    dbInfo["statusDescr"] = "常规拓扑通过：{}/{}; 丢包拓扑通过：{}/{}".\
           format(
               scores["GeneralTopo"]["passedCase"],scores["GeneralTopo"]["testCase"],\
               scores["LossTopo"]["passedCase"],scores["LossTopo"]["testCase"]
           )
    dbInfo["test"] = "{},{},{},{}".\
           format(
               scores["GeneralTopo"]["passedCase"],scores["GeneralTopo"]["testCase"],\
               scores["LossTopo"]["passedCase"],scores["LossTopo"]["testCase"]
           )
    preprocess.removeFiles(decompressPath)

def homework2(dbInfo,makefilePath,targetName):
    pass
def homework3(dbInfo,makefilePath,targetName):
    pass
'''
ADD HOMEWORK function
'''
def homeworkx(dbInfo,makefilePath,targetName):
    dbInfo["status"] = "100"
    dbInfo["statusDescr"] = "未定义作业，请令expId = 1"
    preprocess.removeFiles(decompressPath)

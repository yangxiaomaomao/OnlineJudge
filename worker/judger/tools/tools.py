
import os
import fnmatch
import shutil
import re

# preprocess


def getFileType(fileName):
    return fileName.split(".")[-1]


def decompress(fileName, path):
    if getFileType(fileName) == "zip":
        os.system("7z x {} -o{}".format(fileName, path))
        return True
    else:
        return False


def findMakefilePath(dirName):
    for dirPath, dirNames, fileName in os.walk(dirName):
        if len(fnmatch.filter(fileName, "Makefile")) > 0:
            return dirPath
    return None


def removeDir(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)


def isTargetLine(line):
    return True if re.match("\s*TARGET.*=", line) else False


def getTargetName(makefilePath):
    makefileF = makefilePath + "/Makefile"
    targetName = None
    with open(makefileF, "r") as f:
        for line in f.readlines():
            if(isTargetLine(line)):
                targetName = line.strip().split("=")[1].strip()
    return targetName


def compileMakefile(makefilePath):
    print("make -C {}".format(makefilePath))
    return True if os.system("make -C {}".format(makefilePath)) == 0 else False

# run the execFile


def getPingResult(hSrc, dstIP):
    pingResult = hSrc.cmd("ping {dstIP} -c 2".format(dstIP=dstIP))
    return pingResult


def fillInInfo(scores, info):
    info["status"] = "100"
    info["statusDescr"] = ""
    for key, value in scores.items():
        if value != True:
            info["status"] = "300"
        info["statusDescr"] += "{key}_test:{descr};".format(
            key=key, descr="Pass" if value == True else "Fail") + "   "


def clearIP(n):
    for iface in n.intfList():
        n.cmd('ifconfig %s 0.0.0.0' % (iface))


def getTraceroutePath(hSrc, dstIP):
    tracerouteResult = hSrc.cmd("traceroute {dstIP}".format(dstIP=dstIP))
    lines = tracerouteResult.split("\n")[1:]
    print("result: ", tracerouteResult)
    ret = []
    for line in lines:
        if line:
            ret.append(line.split()[1].strip())
    print("path: ", ret)
    return ret

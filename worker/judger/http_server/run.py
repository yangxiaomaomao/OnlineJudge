from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import OVSBridge
import sys
import os
import time
import json
sys.path.append("..")
from tools.tools import getPingResult,fillInInfo,clearIP
from tools.topos import httpServerTopo
import ast

DEBUG = 0

def generateHttpTopo(topo):
    net = Mininet(topo = topo, switch = OVSBridge, link = TCLink, controller = None)

    h1, h2 = net.get('h1', 'h2')
    
    return net, h1, h2

def testAllInOnce(execFile):
    net, h1, h2 = generateHttpTopo(httpServerTopo())
    net.start()
    
    time.sleep(0.5)
    h1.cmd("./%s &" % execFile)
    scores = h2.cmd("python3 test/test.py")

    scores = eval(scores)
    net.stop()
    
    return scores
     

if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "http-server"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}

    scores = testAllInOnce(exec_file)
    # sys.exit(0)
    if not DEBUG:
        os.remove(exec_file)

    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
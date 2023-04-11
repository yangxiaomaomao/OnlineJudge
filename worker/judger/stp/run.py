from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
import sys
import os
import time
import json
import filecmp
sys.path.append("..")
from tools.tools import fillInInfo,clearIP
from tools.topos import ringTopo4,ringHubAndStpTopo,ringTopo8
DEBUG = 0

def compareRingResult(file, standardFile, nodeNum):
    ret = filecmp.cmp(standardFile, file)
    # rm output file
    for i in range(nodeNum):
        os.system("rm -f b{}-output.txt".format(i + 1))
    os.system("rm -f {}".format("testRing%sResult.txt" % nodeNum))
    print("=================Test Ring%d:%s======================" % (nodeNum,ret))
    return ret


def generateRing4Topo(topo):
    net = Mininet(topo=topo, controller=None)

    for idx in range(4):
        name = 'b' + str(idx+1)
        node = net.get(name)
        clearIP(node)
        node.cmd('./scripts/disable_offloading.sh')
        node.cmd('./scripts/disable_ipv6.sh')

        # set mac address for each interface
        for port in range(len(node.intfList())):
            intf = '%s-eth%d' % (name, port)
            mac = '00:00:00:00:0%d:0%d' % (idx+1, port+1)
            node.setMAC(mac, intf=intf)
    b1, b2, b3, b4 = net.get("b1", "b2", "b3", "b4")
    return net, b1, b2, b3, b4


def generateRing8Topo(topo):
    net = Mininet(topo=topo, controller=None)

    for idx in range(8):
        name = 'b' + str(idx+1)
        node = net.get(name)
        clearIP(node)
        node.cmd('./scripts/disable_offloading.sh')
        node.cmd('./scripts/disable_ipv6.sh')

        # set mac address for each interface
        for port in range(len(node.intfList())):
            intf = '%s-eth%d' % (name, port)
            mac = '00:00:00:00:0%d:0%d' % (idx+1, port+1)
            node.setMAC(mac, intf=intf)
    b1, b2, b3, b4, b5, b6, b7, b8 = net.get(
        "b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8")

    return net, b1, b2, b3, b4, b5, b6, b7, b8


def generateStpHubTopo(topo):
    net = Mininet(topo=topo, controller=None)

    h1, h2, b1, b2, b3, b4, b5, b6 = net.get(
        "h1", "h2", "b1", "b2", "b3", "b4", "b5", "b6")

    idx = 0
    for node in [h1, h2, b1, b2, b3, b4, b5, b6]:
        clearIP(node)
        node.cmd('./scripts/disable_offloading.sh')
        node.cmd('./scripts/disable_ipv6.sh')
        # set mac address for each interface
        if node in [b1, b2, b3, b4, b5, b6]:
            for port in range(len(node.intfList())):
                intf = '%s-eth%d' % (node.name, port)
                mac = '00:00:00:00:0%d:0%d' % (idx+1, port+1)
                node.setMAC(mac, intf=intf)
            idx = idx + 1
    return net, h1, h2, b1, b2, b3, b4, b5, b6


def ring4Test(execFile):
    net, b1, b2, b3, b4 = generateRing4Topo(ringTopo4())
    net.start()
    for b in [b1, b2, b3, b4]:
        b.cmd('./%s > %s-output.txt 2>&1 &' % (execFile, b.name))
    time.sleep(5)

    os.system("sudo pkill -SIGTERM stp")
    time.sleep(1)
    net.stop()

    os.system("./dump_output.sh 4")

    return compareRingResult("testRing4Result.txt", "ring4_ref_result.txt", 4)


def ring8Test(execFile):
    net, b1, b2, b3, b4, b5, b6, b7, b8 = generateRing8Topo(ringTopo8())
    net.start()
    for b in [b1, b2, b3, b4, b5, b6, b7, b8]:
        b.cmd('./%s > %s-output.txt 2>&1 &' % (execFile, b.name))
    time.sleep(10)

    os.system("sudo pkill -SIGTERM stp")
    time.sleep(1)
    net.stop()

    os.system("./dump_output.sh 8")
    return compareRingResult("testRing8Result.txt", "ring8_ref_result.txt", 8)


def stpHubTest(execFile):
    net, h1, h2, b1, b2, b3, b4, b5, b6 = generateStpHubTopo(
        ringHubAndStpTopo())
    net.start()
    for h in [h1, h2]:
        h.cmd("./hub-reference &")
    for b in [b1, b2, b3, b4, b5, b6]:
        b.cmd('./%s > %s-output.txt 2>&1 &' % (execFile, b.name))
    time.sleep(10)

    os.system("sudo pkill -SIGTERM stp")
    os.system("sudo pkill -SIGTERM hub-reference")
    time.sleep(1)
    net.stop()

    os.system("./dump_output.sh 6")
    return compareRingResult("testRing6Result.txt", "stp_hub_ref_result.txt", 6)


if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "stp-reference"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}

    scores = {
        "ring4": ring4Test(exec_file),
        "ring8": ring8Test(exec_file),
        "stpHub": stpHubTest(exec_file)
    }
    if not DEBUG:
        os.remove(exec_file)

    fillInInfo(scores, info)
    
    print(scores)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))

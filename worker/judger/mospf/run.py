#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
import sys
import os
import time
import json
sys.path.append("..")
from tools.tools import getPingResult,fillInInfo,getTraceroutePath,clearIP
from tools.topos import simpleOSPFTopo,switchOSPFTopo
DEBUG = 0

def generateOspfSimpleTopo(topo):
    net = Mininet(topo=topo, controller=None)

    h1, h2, r1, r2, r3, r4 = net.get('h1', 'h2', 'r1', 'r2', 'r3', 'r4')
    h1.cmd('ifconfig h1-eth0 10.0.1.11/24')

    r1.cmd('ifconfig r1-eth0 10.0.1.1/24')
    r1.cmd('ifconfig r1-eth1 10.0.2.1/24')
    r1.cmd('ifconfig r1-eth2 10.0.3.1/24')

    r2.cmd('ifconfig r2-eth0 10.0.2.2/24')
    r2.cmd('ifconfig r2-eth1 10.0.4.2/24')

    r3.cmd('ifconfig r3-eth0 10.0.3.3/24')
    r3.cmd('ifconfig r3-eth1 10.0.5.3/24')

    r4.cmd('ifconfig r4-eth0 10.0.4.4/24')
    r4.cmd('ifconfig r4-eth1 10.0.5.4/24')
    r4.cmd('ifconfig r4-eth2 10.0.6.4/24')

    h2.cmd('ifconfig h2-eth0 10.0.6.22/24')

    h1.cmd('route add default gw 10.0.1.1')
    h2.cmd('route add default gw 10.0.6.4')

    for h in (h1, h2):
        h.cmd('./scripts/disable_offloading.sh')
        h.cmd('./scripts/disable_ipv6.sh')

    for r in (r1, r2, r3, r4):
        r.cmd('./scripts/disable_arp.sh')
        r.cmd('./scripts/disable_icmp.sh')
        r.cmd('./scripts/disable_ip_forward.sh')
        r.cmd('./scripts/disable_ipv6.sh')
    return net, h1, h2, r1, r2, r3, r4


def generateOspfSwitchTopo(topo):
    net = Mininet(topo=topo, controller=None)

    h1, h2, r1, r2, r3, r4, r5, s1 = net.get(
        'h1', 'h2', 'r1', 'r2', 'r3', 'r4', "r5", "s1")
    h1.cmd('ifconfig h1-eth0 10.0.1.11/24')
    # h1.setIP("10.0.8.9/24")
    r1.cmd("ifconfig r1-eth0 10.0.1.1/24")
    r1.cmd("ifconfig r1-eth1 10.0.2.1/24")
    r1.cmd("ifconfig r1-eth2 10.0.3.1/24")

    r2.cmd("ifconfig r2-eth0 10.0.2.2/24")
    r2.cmd("ifconfig r2-eth1 10.0.4.2/24")
    r2.cmd("ifconfig r2-eth2 10.0.5.2/24")

    r3.cmd("ifconfig r3-eth0 10.0.3.3/24")
    r3.cmd("ifconfig r3-eth1 10.0.4.3/24")

    r4.cmd("ifconfig r4-eth0 10.0.4.4/24")
    r4.cmd("ifconfig r4-eth1 10.0.6.4/24")
    r4.cmd("ifconfig r4-eth2 10.0.7.4/24")

    r5.cmd("ifconfig r5-eth0 10.0.5.5/24")
    r5.cmd("ifconfig r5-eth1 10.0.6.5/24")

    h2.cmd("ifconfig h2-eth0 10.0.7.77/24")

    h1.cmd("route add default gw 10.0.1.1")
    h2.cmd("route add default gw 10.0.7.4")
    for h in (h1, h2, s1):
        h.cmd('./scripts/disable_offloading.sh')
        h.cmd('./scripts/disable_ipv6.sh')

    for r in (r1, r2, r3, r4, r5):
        r.cmd('./scripts/disable_arp.sh')
        r.cmd('./scripts/disable_icmp.sh')
        r.cmd('./scripts/disable_ip_forward.sh')
        r.cmd('./scripts/disable_ipv6.sh')
    clearIP(s1)
    return net, h1, h2, r1, r2, r3, r4, r5, s1


def simpleOspfTopoTest(execFile):
    net, h1, h2, r1, r2, r3, r4 = generateOspfSimpleTopo(simpleOSPFTopo())

    net.start()
    for r in [r1, r2, r3, r4]:
        r.cmd("./%s &" % execFile)

    time.sleep(40)

    pingResult = getPingResult(h1, "10.0.6.22")

    originPath = getTraceroutePath(h1, "10.0.6.22")

    print("origin_path", originPath)
    ret = [False, False]

    # The first test don't pass, so we don't need to expriment test2
    if "0% packet loss" not in pingResult:
        net.stop()
        return ret
    print("origin_path", originPath)

    ret[0] = True
    # Test 1 pass, continue test2
    # why there may exist the path ["10.0.1.1", "10.0.2.2", "10.0.5.4", "10.0.6.22"],yes,there exists
    path1 = ["10.0.1.1", "10.0.2.2", "10.0.4.4", "10.0.6.22"]
    path2 = ["10.0.1.1", "10.0.3.3", "10.0.5.4", "10.0.6.22"]
    path3 = ["10.0.1.1", "10.0.2.2", "10.0.5.4", "10.0.6.22"]
    path4 = ["10.0.1.1", "10.0.3.3", "10.0.4.4", "10.0.6.22"]

    
    if originPath in [path1, path3]:
        CLI(net, script="r1r2_down.txt")
    elif originPath in [path2, path4]:
        CLI(net, script="r1r3_down.txt")
    else:
        net.stop()
        return [False, False]
    print("begin_test2")
    time.sleep(40)
    pingResult = getPingResult(h1, "10.0.6.22")
    ret[1] = "0% packet loss" in pingResult

    net.stop()
    return ret


def switchOspfTopoTest(execFile):
    net, h1, h2, r1, r2, r3, r4, r5, s1 = generateOspfSwitchTopo(
        switchOSPFTopo())

    net.start()
    for r in [r1, r2, r3, r4]:
        r.cmd("./%s &" % execFile)
    s1.cmd("./switch-reference &")

    time.sleep(30)

    pingResult = getPingResult(h1, "10.0.7.77")

    net.stop()

    return "0% packet loss" in pingResult


if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "mospfd"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}
    print(result_path,exec_file)
    os.system("chmod 775 %s" % exec_file)
    scores = {
        "simple_topo": simpleOspfTopoTest(exec_file),
        "switch_topo": switchOspfTopoTest(exec_file)
    }
    if not DEBUG:
        os.remove(exec_file)

    scores["simple_ping"] = scores["simple_topo"][0]
    scores["unlink_ping"] = scores["simple_topo"][1]
    del scores["simple_topo"]

    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))

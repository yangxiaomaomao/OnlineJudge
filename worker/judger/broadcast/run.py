from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink

import sys
import os
import time
import json
from itertools import permutations
sys.path.append("..")
from tools.tools import getPingResult,fillInInfo,clearIP
from tools.topos import hubLoopTopo,hubTopo

DEBUG = 0

def generateHubTopo(topo):
    net = Mininet(topo=topo, link=TCLink, controller=None)

    h1, h2, h3, b1 = net.get('h1', 'h2', 'h3', 'b1')
    h1.cmd('ifconfig h1-eth0 10.0.0.1/8')
    h2.cmd('ifconfig h2-eth0 10.0.0.2/8')
    h3.cmd('ifconfig h3-eth0 10.0.0.3/8')
    clearIP(b1)

    for h in [h1, h2, h3, b1]:
        h.cmd('./scripts/disable_offloading.sh')
        h.cmd('./scripts/disable_ipv6.sh')
    return net, h1, h2, h3, b1


def generateHubLoopTopo(topo):
    net = Mininet(topo=topo, link=TCLink, controller=None)
    h1, h2, b1, b2, b3 = net.get('h1', 'h2', 'b1', 'b2', 'b3')
    h1.cmd('ifconfig h1-eth0 10.0.0.1/8')
    h2.cmd('ifconfig h2-eth0 10.0.0.2/8')
    clearIP(b1)
    clearIP(b2)
    clearIP(b3)

    for h in [h1, h2, b1, b2, b3]:
        h.cmd('./scripts/disable_offloading.sh')
        h.cmd('./scripts/disable_ipv6.sh')
    return net, h1, h2, b1, b2, b3


def getBWThroughIperf(iperfFile):
    with open(iperfFile, "r") as f:
        lines = f.readlines()
        # print("iiiiiiiiiiiiiiiii", lines)

    os.system("rm -f {}".format(iperfFile))
    if len(lines) == 0:
        return -1
    # Avoid the file format is not standard
    try:
        BW = float(lines[-1].split()[-2])
    except Exception as msg:
        BW = -1
    return BW


def getBWInTopo(file):
    os.system("sudo chmod 777 %s" % file)
    net, h1, h2, h3, b1 = generateHubTopo(hubTopo())

    net.start()
    time.sleep(1)

    # h23 iperf h1
    b1.cmd("./%s &" % file)
    time.sleep(1)

    h1.cmd("iperf -s &")
    time.sleep(1)
    h2_iperf_h1_res = "h2_iperf_h1.txt"
    h3_iperf_h1_res = "h3_iperf_h1.txt"

    h2.cmd("iperf -c 10.0.0.1 > %s &" % h2_iperf_h1_res)
    h3.cmd("iperf -c 10.0.0.1 > %s &" % h3_iperf_h1_res)
    time.sleep(6) # fix
    os.system("sudo pkill -SIGTERM iperf")
    time.sleep(1)

    # h1 iperf h2h3
    h2.cmd("iperf -s &")
    h3.cmd("iperf -s &")
    time.sleep(1)
    h1_iperf_h2_res = "h1_iperf_h2.txt"
    h1_iperf_h3_res = "h1_iperf_h3.txt"

    h1.cmd("iperf -c 10.0.0.2 > %s &" % h1_iperf_h2_res)
    h1.cmd("iperf -c 10.0.0.3 > %s &" % h1_iperf_h3_res)
    # wait 6s to finish the file writing
    time.sleep(6)# fix
    os.system("sudo pkill -SIGTERM iperf")

    time.sleep(1)
    net.stop()

    h2_h1_BW = getBWThroughIperf(h2_iperf_h1_res)
    h3_h1_BW = getBWThroughIperf(h3_iperf_h1_res)
    h1_h2_BW = getBWThroughIperf(h1_iperf_h2_res)
    h1_h3_BW = getBWThroughIperf(h1_iperf_h3_res)

    # print("ppppppppppppppp", h2_h1_BW, h3_h1_BW, h1_h2_BW, h1_h3_BW)

    return h1_h2_BW + h1_h3_BW, h2_h1_BW + h3_h1_BW


def hubPingTest(execFile):
    net, h1, h2, h3, b1 = generateHubTopo(hubTopo())
    net.start()
    time.sleep(0.5)
    b1.cmd("{} &".format(execFile))
    time.sleep(1)

    host_list = [h1, h2, h3]
    for src, dst in list(permutations(host_list, 2)):
        if dst == h1:
            dstIP = "10.0.0.1"
        elif dst == h2:
            dstIP = "10.0.0.2"
        elif dst == h3:
            dstIP = "10.0.0.3"
        else:
            print("Unknown dstIP,exiting......")
            sys.exit(1)
        if "0% packet loss" not in getPingResult(src, dstIP):
            net.stop()
            return False
    net.stop()
    return True


def hubIperfTest(execFile):
    h1_iperf_h2h3_standardBW, h2h3_iperf_h1_standardBW = getBWInTopo(
        "hub-reference")
    time.sleep(1)
    h1_iperf_h2h3_testBW, h2h3_iperf_h1_testBW = getBWInTopo(execFile)

    h1_iperf_h2h3 = (h1_iperf_h2h3_testBW >= 0 and abs(
        h1_iperf_h2h3_standardBW - h1_iperf_h2h3_testBW) < 2)
    h2h3_iperf_h1 = (h2h3_iperf_h1_testBW >= 0 and abs(
        h2h3_iperf_h1_standardBW - h2h3_iperf_h1_testBW) < 2)

    return [h1_iperf_h2h3, h2h3_iperf_h1]


def hubPingLoopTest(execFile):
    net, h1, h2, b1, b2, b3 = generateHubLoopTopo(hubLoopTopo())

    net.start()
    for b in (b1, b2, b3):
        b.cmd("./%s &" % execFile)
    time.sleep(1)

    dumpFile = "h2_tcpdump.txt"
    h1.cmd("ping 10.0.0.2 -c 2 &")
    h2.cmd("tcpdump -c 10 -i h2-eth0 arp -Q in > %s &" % dumpFile)
    time.sleep(1)
    h1.cmd("sudo pkill -SIGTERM ping")
    h2.cmd("sudo pkill -SIGTERM tcpdump")
    time.sleep(1)
    net.stop()

    with open(dumpFile, "r") as f:
        lines = f.readlines()
        pktNum = len(lines)
    os.system("rm -f {}".format(dumpFile))

    return True if (pktNum > 2) else False


if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "hub-reference"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}

    scores = {
        "ping": hubPingTest(exec_file),
        "iperf": hubIperfTest(exec_file),
        "ping_loop": hubPingLoopTest(exec_file)
    }

    if not DEBUG:
        os.remove(exec_file)
        
    scores["h1_iperf_h2h3"] = scores["iperf"][0]
    scores["h2h3_iperf_h1"] = scores["iperf"][1]
    del scores["iperf"]

    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))

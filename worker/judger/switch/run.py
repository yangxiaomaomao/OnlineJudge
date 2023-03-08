from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import sys
import os
import time
import json
sys.path.append("..")
from tools.tools import fillInInfo,clearIP
from tools.topos import switchTopo
DEBUG = 0

def generateSwitchTopo(topo):
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
    net, h1, h2, h3, b1 = generateSwitchTopo(switchTopo())

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
    time.sleep(7)
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
    time.sleep(7)
    os.system("sudo pkill -SIGTERM iperf")

    time.sleep(1)
    net.stop()

    h2_h1_BW = getBWThroughIperf(h2_iperf_h1_res)
    h3_h1_BW = getBWThroughIperf(h3_iperf_h1_res)
    h1_h2_BW = getBWThroughIperf(h1_iperf_h2_res)
    h1_h3_BW = getBWThroughIperf(h1_iperf_h3_res)

    # print("ppppppppppppppp", h2_h1_BW, h3_h1_BW, h1_h2_BW, h1_h3_BW)

    return h1_h2_BW + h1_h3_BW, h2_h1_BW + h3_h1_BW


def switchIperfTest(execFile):
    h1_iperf_h2h3_standardBW, h2h3_iperf_h1_standardBW = getBWInTopo(
        "switch-reference")
    time.sleep(1)
    h1_iperf_h2h3_testBW, h2h3_iperf_h1_testBW = getBWInTopo(execFile)

    h1_iperf_h2h3 = (h1_iperf_h2h3_testBW >= 0 and abs(
        h1_iperf_h2h3_standardBW - h1_iperf_h2h3_testBW) < 2)
    h2h3_iperf_h1 = (h2h3_iperf_h1_testBW >= 0 and abs(
        h2h3_iperf_h1_standardBW - h2h3_iperf_h1_testBW) < 2)

    return [h1_iperf_h2h3, h2h3_iperf_h1]


if __name__ == '__main__':
    if DEBUG:
        result_path = "result"
        exec_file = "switch-reference"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}

    scores = {
        "iperf": switchIperfTest(exec_file)
    }

    scores["h1_iperf_h2h3"] = scores["iperf"][0]
    scores["h2h3_iperf_h1"] = scores["iperf"][1]
    del scores["iperf"]
    
    if not DEBUG:
        os.remove(exec_file)
        
    fillInInfo(scores, info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))

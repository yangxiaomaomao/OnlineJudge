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
from tools.topos import TCPTopo


DEBUG = 0

def generateHttpTopo(topo):
    net = Mininet(topo = topo, switch = OVSBridge, link = TCLink, controller = None)

    h1, h2 = net.get('h1', 'h2')
    
    h1.cmd('ifconfig h1-eth0 10.0.0.1/24')
    h2.cmd('ifconfig h2-eth0 10.0.0.2/24')

    for h in (h1, h2):
        # h.cmd('scripts/disable_arp.sh')
        # h.cmd('scripts/disable_icmp.sh')
        # h.cmd('scripts/disable_ip_forward.sh')
        h.cmd('scripts/disable_ipv6.sh')
        h.cmd('scripts/disable_offloading.sh')
        h.cmd('scripts/disable_tcp_rst.sh')
    
    return net, h1, h2
 
def detectKernelPort(h,port):
    detect_ports = h.cmd("netstat -tunlp")
    
    if detect_ports.find("0.0.0.0:%s" % port) == -1:
        return False # not find the port 80
    else:
        return True #True # find students' trick, the process is using 80 port of the kernel, not its own!

def finalTest(execFile):
    net, h1, h2 = generateHttpTopo(TCPTopo())
    net.start()
    # CLI(net)
    # return 0
    time.sleep(0.5)
    h1.cmd("./%s &" % execFile)
    #h1.cmd("python3 del.py")

    time.sleep(0.5)
    
    scores = {}
    if detectKernelPort(h1,80):
        scores = scores = {
            "http_200":False,
            "http_404":False,
            "http_in_dir":False,
            "http_range1":False,
            "http_range2":False
        }
    else:
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
    scores = {}

    scores = finalTest(exec_file)
    
    print(scores)
    # sys.exit(0)
    if not DEBUG:
        os.remove(exec_file)

    fillInInfo(scores, info)
    print(info)

    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))
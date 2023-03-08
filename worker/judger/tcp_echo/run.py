from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
import sys
import os
import time
import json
import tcp_echo
sys.path.append("..")
from tools.tools import fillInInfo
from tools.topos import TCPTopo

DEBUG = 0

data = tcp_echo.data

client_res = "client_res.log"

uniform_cmp_data = []
for i in range(10):
    uniform_cmp_data.append(data[i:] + data[:i + 1])


def uniformData(file):
    with open(file, "r") as f:
        res = f.readlines()

    ret = []
    for item in res:
        if item[0:15] == "server echoes: ":
            ret.append(item[15:].replace("\n", ""))

    #os.remove(file)
    return ret


def generateEchoTopo(topo):
    net = Mininet(topo=topo, controller=None, link=TCLink)

    h1, h2 = net.get('h1', 'h2')
    h1.cmd('ifconfig h1-eth0 10.0.0.1/24')
    h2.cmd('ifconfig h2-eth0 10.0.0.2/24')

    for h in (h1, h2):
        h.cmd('scripts/disable_offloading.sh')
        h.cmd('scripts/disable_tcp_rst.sh')

    return net, h1, h2


def CEchoCTest(execFile):
    net, h1, h2 = generateEchoTopo(TCPTopo())

    net.start()

    h1.cmd("./%s server 10001 &" % execFile)

    h2.cmd("./%s client 10.0.0.1 10001 > %s &" % (execFile, client_res))

    time.sleep(5)

    net.stop()

    res = uniformData(client_res)
    
    if res == []:
        return False

    cmp_data = [item[:len(res[0])] for item in uniform_cmp_data[:len(res)]]

    return res == cmp_data

# server C


def CEchoPythonTest(execFile):
    net, h1, h2 = generateEchoTopo(TCPTopo())

    net.start()

    h1.cmd("./%s server 10001 &" % execFile)

    h2.cmd("python tcp_echo.py client 10.0.0.1 10001 > %s &" % client_res)

    time.sleep(5)

    net.stop()

    res = uniformData(client_res)
    
    if res == []:
        return False

    cmp_data = [item[:len(res[0])] for item in uniform_cmp_data[:len(res)]]

    return res == cmp_data
# server Python


def pythonEchoCTest(execFile):
    net, h1, h2 = generateEchoTopo(TCPTopo())

    net.start()

    h1.cmd("python tcp_echo.py server 10001 &")
    
    res = h2.cmd("./%s client 10.0.0.1 10001 > %s &" % (execFile, client_res))

    time.sleep(5)

    net.stop()

    res = uniformData(client_res)
    
    if res == []:
        return False

    cmp_data = [item[:len(res[0])] for item in uniform_cmp_data[:len(res)]]
    print("res",res)
    print("cmp_data",cmp_data)
    return res == cmp_data


if __name__ == "__main__":
    if DEBUG:
        result_path = "result"
        exec_file = "tcp_echo"
    else:
        result_path = sys.argv[1]
        exec_file = sys.argv[2]
    info = {}

    # 3 tests (client sends data to server, server echos to client)
    # 1: client: C server: C
    # 2: client: python server: C
    # 3: client: C server: python
    # h1: server
    # h2: client
    scores = {
        "CEchoC": CEchoCTest(exec_file),
        "CEchoPython": CEchoPythonTest(exec_file),
        "pythonEchoC": pythonEchoCTest(exec_file)
    }
    if not DEBUG:
        os.remove(exec_file)

    fillInInfo(scores, info)
    
    with open(os.path.join(result_path, "result.json"), "w") as f:
        f.write(json.dumps(info, indent=4, ensure_ascii=False))

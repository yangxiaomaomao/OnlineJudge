
from mininet.topo import Topo

class TCPGeneralTopo(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        self.addLink(h1,h2,delay = "1ms")
        
class TCPLossTopo(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        self.addLink(h1,h2,delay = "1ms",loss = 2)
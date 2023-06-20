from mininet.topo import Topo

class httpServerTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')

        self.addLink(h1, s1, bw=100, delay='10ms')
        self.addLink(h2, s1)
    

# hub


class hubTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        b1 = self.addHost('b1')

        self.addLink(h1, b1, bw=20)
        self.addLink(h2, b1, bw=10)
        self.addLink(h3, b1, bw=10)


class hubLoopTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        b1 = self.addHost('b1')
        b2 = self.addHost('b2')
        b3 = self.addHost('b3')

        self.addLink(h1, b1, bw=10)
        self.addLink(h2, b2, bw=10)
        self.addLink(b1, b2, bw=10)
        self.addLink(b2, b3, bw=10)
        self.addLink(b1, b3, bw=10)
# switch


class switchTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        b1 = self.addHost('b1')

        self.addLink(h1, b1, bw=20)
        self.addLink(h2, b1, bw=10)
        self.addLink(h3, b1, bw=10)
# router


class simpleRouterTopo(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        h3 = self.addHost("h3")
        r1 = self.addHost("r1")

        self.addLink(h1, r1)
        self.addLink(h2, r1)
        self.addLink(h3, r1)


class hop3RouterTopo(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        r1 = self.addHost("r1")
        r2 = self.addHost("r2")

        self.addLink(h1, r1)
        self.addLink(r1, r2)
        self.addLink(r2, h2)
# stp


class ringTopo4(Topo):
    def build(self):
        b1 = self.addHost('b1')
        b2 = self.addHost('b2')
        b3 = self.addHost('b3')
        b4 = self.addHost('b4')

        self.addLink(b1, b2)
        self.addLink(b1, b3)
        self.addLink(b2, b4)
        self.addLink(b3, b4)


class ringTopo8(Topo):
    def build(self):
        b1 = self.addHost('b1')
        b2 = self.addHost('b2')
        b3 = self.addHost('b3')
        b4 = self.addHost('b4')
        b5 = self.addHost('b5')
        b6 = self.addHost('b6')
        b7 = self.addHost('b7')
        b8 = self.addHost('b8')

        self.addLink(b1, b2)
        self.addLink(b2, b3)
        self.addLink(b3, b4)
        self.addLink(b4, b5)
        self.addLink(b5, b6)
        self.addLink(b6, b7)
        self.addLink(b7, b8)
        self.addLink(b1, b8)
        self.addLink(b1, b3)
        self.addLink(b1, b7)
        self.addLink(b2, b5)
        self.addLink(b3, b7)
        self.addLink(b4, b6)
        self.addLink(b6, b8)


class ringHubAndStpTopo(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        b1 = self.addHost("b1")
        b2 = self.addHost("b2")
        b3 = self.addHost("b3")
        b4 = self.addHost("b4")
        b5 = self.addHost("b5")
        b6 = self.addHost("b6")

        self.addLink(h1, b1)
        self.addLink(h1, b2)
        self.addLink(h1, b3)
        self.addLink(h1, b6)
        self.addLink(h2, b2)
        self.addLink(h2, b3)
        self.addLink(h2, b4)
        self.addLink(h2, b5)
# mospf


class simpleOSPFTopo(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        r1 = self.addHost("r1")
        r2 = self.addHost("r2")
        r3 = self.addHost("r3")
        r4 = self.addHost("r4")

        self.addLink(h1, r1)
        self.addLink(r1, r2)
        self.addLink(r1, r3)
        self.addLink(r2, r4)
        self.addLink(r3, r4)
        self.addLink(r4, h2)


class switchOSPFTopo(Topo):
    def build(self):
        h1 = self.addHost("h1")
        h2 = self.addHost("h2")
        r1 = self.addHost("r1")
        r2 = self.addHost("r2")
        r3 = self.addHost("r3")
        r4 = self.addHost("r4")
        r5 = self.addHost("r5")
        s1 = self.addHost("s1")

        self.addLink(h1, r1)
        self.addLink(r1, r2)
        self.addLink(r1, r3)

        self.addLink(s1, r2)
        self.addLink(s1, r3)
        self.addLink(s1, r4)

        self.addLink(r5, r2)
        self.addLink(r5, r4)
        self.addLink(r4, h2)
# NAT


class NATTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        n1 = self.addHost('n1')

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(n1, s1)
        self.addLink(h3, n1)


class NATNATTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        n1 = self.addHost('n1')
        n2 = self.addHost('n2')

        self.addLink(h1, n1)
        self.addLink(h2, n2)
        self.addLink(n1, n2)
        
# tcp stack echo
class TCPTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        self.addLink(h1, h2, delay='10ms')
        
# tcp stack loss transfer
class TCPLossTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')

        self.addLink(h1, h2, delay='10ms', loss=2)
        

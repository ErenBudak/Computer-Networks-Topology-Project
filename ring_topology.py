from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI
import time                   # <‑‑ eklendi

class RingTopology(Topo):
    def build(self):
        switches = []
        s1=self.addSwitch('s1',cls=OVSKernelSwitch,failMode='standalone',stp=True)
        switches.append(s1)
        s2=self.addSwitch('s2',cls=OVSKernelSwitch,failMode='standalone',stp=True)
        switches.append(s2)
        s3=self.addSwitch('s3',cls=OVSKernelSwitch,failMode='standalone',stp=True)
        switches.append(s3)
        s4=self.addSwitch('s4',cls=OVSKernelSwitch,failMode='standalone',stp=True)
        switches.append(s4)
        s5=self.addSwitch('s5',cls=OVSKernelSwitch,failMode='standalone',stp=True)
        switches.append(s5)
        s6=self.addSwitch('s6',cls=OVSKernelSwitch,failMode='standalone',stp=True)
        switches.append(s6)
        h1=self.addHost('h1')
        h2=self.addHost('h2')
        h3=self.addHost('h3')
        h4=self.addHost('h4')
        h5=self.addHost('h5')
        h6=self.addHost('h6')
        self.addLink(h1, s1, cls=TCLink, bw=75, delay='1ms')
        self.addLink(h2, s2, cls=TCLink, bw=75, delay='1ms')
        self.addLink(h3, s3, cls=TCLink, bw=75, delay='1ms')
        self.addLink(h4, s4, cls=TCLink, bw=75, delay='1ms')
        self.addLink(h5, s5, cls=TCLink, bw=75, delay='1ms')
        self.addLink(h6, s6, cls=TCLink, bw=75, delay='1ms')
        for i in range(6):                                   
            self.addLink(switches[i], switches[(i + 1) % 6],
                         cls=TCLink, bw=100, delay='2ms')

        for a, b in [(0, 3), (1, 4), (2, 5)]:                # chords
            self.addLink(switches[a], switches[b],
                         cls=TCLink, bw=100, delay='2ms')


if __name__ == '__main__':
    topo = RingTopology()
    net = Mininet(topo=topo,
                  link=TCLink,
                  build=True,
                  autoSetMacs=True,
                  autoStaticArp=True,
                  controller=None)
    net.start()
    time.sleep(30)
    net.pingAll() 
    CLI(net)
    net.stop()
    

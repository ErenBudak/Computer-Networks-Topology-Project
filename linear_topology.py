from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSController
from mininet.link import TCLink
from mininet.cli import CLI

class LinearTopology(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

        self.addLink(h1, s1, bw=75, delay='1ms')
        self.addLink(h2, s1, bw=75, delay='1ms')
        self.addLink(h3, s2, bw=75, delay='1ms')
        self.addLink(h4, s2, bw=75, delay='1ms')
        self.addLink(h5, s3, bw=75, delay='1ms')
        self.addLink(h6, s3, bw=75, delay='1ms')
        self.addLink(s1, s2, bw=100, delay='2ms')
        self.addLink(s2, s3, bw=100, delay='2ms')

if __name__ == '__main__':
    topo = LinearTopology()
    net = Mininet(topo=topo, link=TCLink, controller=OVSController)
    net.start()
    CLI(net)
    net.stop()

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller
from mininet.link import TCLink
from mininet.cli import CLI

class StarTopology(Topo):
    def build(self):
        s1 = self.addSwitch('s1')

        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')

     
        for h in [h1, h2, h3, h4, h5, h6]:
            self.addLink(h, s1, cls=TCLink, bw=75, delay='1ms')

       

if __name__ == '__main__':
    topo = StarTopology()
    net = Mininet(topo=topo, link=TCLink, controller=Controller)
    net.start()
    CLI(net)
    net.stop()

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch,Controller 
from mininet.link import TCLink
from mininet.cli import CLI
import time

class SpineLeafTopology(Topo):
    def build(self):
        spine1 = self.addSwitch('spine1', cls=OVSKernelSwitch, stp=True,failMode='standalone')
        spine2 = self.addSwitch('spine2', cls=OVSKernelSwitch, stp=True,failMode='standalone')

        leaf1 = self.addSwitch('leaf1', cls=OVSKernelSwitch, stp=True,failMode='standalone')
        leaf2 = self.addSwitch('leaf2', cls=OVSKernelSwitch, stp=True,failMode='standalone')
        leaf3 = self.addSwitch('leaf3', cls=OVSKernelSwitch, stp=True,failMode='standalone')

       
        for leaf in [leaf1, leaf2, leaf3]:
            for spine in [spine1, spine2]:
                self.addLink(leaf, spine, bw=100, delay='2ms')

        # Hosts
        hosts = {
            'h1': leaf1,
            'h2': leaf1,
            'h3': leaf2,
            'h4': leaf2,
            'h5': leaf3,
            'h6': leaf3,
            'h_loadgen': leaf1
        }

        for h, sw in hosts.items():
            self.addHost(h)
            self.addLink(h, sw, bw=75, delay='1ms')

if __name__ == '__main__':
    topo = SpineLeafTopology()
    
    net = Mininet(topo=topo, 
                  link=TCLink, 
                  controller=None, 
                  autoStaticArp=True)
    
    net.start()
    time.sleep(40) 
    net.pingAll()
    CLI(net)
    net.stop()
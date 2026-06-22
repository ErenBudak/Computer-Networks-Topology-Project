from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI

class BondedStarTopology(Topo):
    """
    Star topology with host-side bonding (active-backup) for fast failover.
    Each host bonds its two links (to s1 and s2) into bond0.
    """
    def build(self):
        # Central switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        hosts = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        # Connect hosts to both switches
        for hname in hosts:
            h = self.addHost(hname)
            self.addLink(h, s1, cls=TCLink, bw=75, delay='1ms')
            self.addLink(h, s2, cls=TCLink, bw=75, delay='1ms')
        # Inter-switch link
        self.addLink(s1, s2, cls=TCLink, bw=100, delay='2ms')

if __name__ == '__main__':
    topo = BondedStarTopology()
    net = Mininet(topo=topo, switch=OVSKernelSwitch, link=TCLink,
                  controller=Controller, autoSetMacs=True, autoStaticArp=False)
    net.start()
    # Configure host-side bonding
    for idx, hname in enumerate(['h1','h2','h3','h4','h5','h6'], start=1):
        host = net.get(hname)
        # Enable Linux bonding module
        host.cmd('modprobe bonding')
        # Create bond0 in active-backup mode
        host.cmd('ip link add bond0 type bond mode active-backup miimon 100')
        # Move interfaces into bond
        host.cmd(f'ip link set {hname}-eth0 down')
        host.cmd(f'ip link set {hname}-eth1 down')
        host.cmd(f'ip link set {hname}-eth0 master bond0')
        host.cmd(f'ip link set {hname}-eth1 master bond0')
        # Assign IP to bond0, remove from eth*
        host.cmd(f'ip addr add 10.0.0.{idx}/24 dev bond0')
        host.cmd(f'ip addr flush dev {hname}-eth0')
        host.cmd(f'ip addr flush dev {hname}-eth1')
        host.cmd('ip link set bond0 up')
    # Give switches a moment
    net.waitConnected()
    CLI(net)
    net.stop()

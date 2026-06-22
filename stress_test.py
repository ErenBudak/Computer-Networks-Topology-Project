#!/usr/bin/env python3
import re
import time
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.link import TCLink
from mininet.cli import CLI

class SpineLeafTopology(Topo):
    def build(self):
        spine1 = self.addSwitch('spine1', cls=OVSKernelSwitch, stp=True, failMode='standalone')
        spine2 = self.addSwitch('spine2', cls=OVSKernelSwitch, stp=True, failMode='standalone')

        leaf1 = self.addSwitch('leaf1', cls=OVSKernelSwitch, stp=True, failMode='standalone')
        leaf2 = self.addSwitch('leaf2', cls=OVSKernelSwitch, stp=True, failMode='standalone')
        leaf3 = self.addSwitch('leaf3', cls=OVSKernelSwitch, stp=True, failMode='standalone')

        
        for leaf in [leaf1, leaf2, leaf3]:
            for spine in [spine1, spine2]:
                self.addLink(leaf, spine, cls=TCLink, bw=100, delay='2ms')

        
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
            self.addLink(h, sw, cls=TCLink, bw=75, delay='1ms')


def parse_iperf_output(output: str) -> float:
    # First attempt: CSV (iperf2 with -y C), last field is bits/sec
    lines = [l.strip() for l in output.strip().splitlines() if l.strip()]
    if not lines:
        return 0.0
    # Try CSV style: comma-separated and last field numeric
    last = lines[-1]
    if ',' in last:
        parts = last.split(',')
        try:
            bw_bits = float(parts[-1])
            return bw_bits / 1e6  # to Mbps
        except Exception:
            pass
    
    for line in reversed(lines):
        m = re.search(r'([\d\.]+)\s+Mbits/sec', line)
        if m:
            return float(m.group(1))
        m2 = re.search(r'([\d\.]+)\s+Kbits/sec', line)
        if m2:
            return float(m2.group(1)) / 1000.0
        m3 = re.search(r'([\d\.]+)\s+Gbits/sec', line)
        if m3:
            return float(m3.group(1)) * 1000.0
    return 0.0

def cleanup_iperf(net):
    for h in ['h4', 'h6', 'h2', 'h5', 'h6', 'h1', 'h3']:
        try:
            host = net.get(h)
            host.cmd('pkill -f iperf')
        except Exception:
            pass

def run_test(net, pairs, name):
    print(f"\n===== {name} =====")
    # Burada farklı serverlar belirlenir
    servers = sorted(set(server for _, server in pairs))
    cleanup_iperf(net)
    time.sleep(1)

    for server in servers:
        h = net.get(server)
        # '-s' server için
        h.cmd('iperf -s &')  
    time.sleep(1)

    # clientlar eşzamanlı başlıyor
    client_procs = {}
    for client, server in pairs:
        client_host = net.get(client)
        server_ip = net.get(server).IP()
        proc = client_host.popen(['iperf', '-c', server_ip, '-t', '30', '-f', 'm'])
        client_procs[(client, server)] = proc

    
    results = {}
    for (client, server), proc in client_procs.items():
        try:
            out, err = proc.communicate(timeout=40)
            if out is None:
                out = ''
            if isinstance(out, bytes):
                out = out.decode(errors='ignore')
            bw = parse_iperf_output(out)
        except Exception as e:
            proc.kill()
            bw = 0.0
        results[(client, server)] = bw
        print(f"{client} -> {server}: {bw:.2f} Mbps")

    total = sum(results.values())
    print(f"Total aggregate throughput for {name}: {total:.2f} Mbps")

    cleanup_iperf(net)
    time.sleep(1)
    return results, total

if __name__ == '__main__':
    topo = SpineLeafTopology()
    net = Mininet(topo=topo, link=TCLink, controller=None,
                  autoSetMacs=True, autoStaticArp=True)
    net.start()
    net.waitConnected()
    time.sleep(2)
    net.pingAll()

    testA_pairs = [('h1', 'h4'), ('h3', 'h6'), ('h5', 'h2')]
    testB_pairs = [('h1', 'h5'), ('h2', 'h6')]

    # A testi
    resultsA, totalA = run_test(net, testA_pairs, "Test A (balanced across leaves)")
    #B testi
    resultsB, totalB = run_test(net, testB_pairs, "Test B (bottleneck on leaf1)")
    CLI(net)
    net.stop()
   

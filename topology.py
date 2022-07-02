#!/usr/bin/python3

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink


class FVTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        hconfig = {"inNamespace": True}
        std_link_config = {"bw": 1000}  # IoT
        http_link_config = {}  # normal hosts
        host_link_config = {}

        # Create switch nodes
        for i in range(4):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        # Create host nodes
        for i in range(7):
            self.addHost("h%d" % (i + 1), **hconfig)

        # Add switch links
        self.addLink("s1", "s4", **std_link_config) # port 1 - port 1
        self.addLink("s1", "s2", **std_link_config) # port 2 - port 1
        self.addLink("s2", "s3", **std_link_config) # port 2 - port 1
        self.addLink("s3", "s1", **std_link_config) # port 2 - port 3

        # Add host links

        # Hosts
        # -------------------------------------------
        self.addLink("h1", "s4", **host_link_config) # port 0 - port 2
        self.addLink("h2", "s4", **host_link_config) # port 0 - port 3
        self.addLink("h3", "s4", **host_link_config) # port 0 - port 4

        # Machineries
        # -------------------------------------------
        self.addLink("h4", "s2", **host_link_config) # port 0 - port 3
        self.addLink("h5", "s2", **host_link_config) # port 0 - port 4

        # IoT
        # -------------------------------------------
        self.addLink("h6", "s3", **host_link_config) # port 0 - port 3
        self.addLink("h7", "s3", **host_link_config) # port 0 - port 4


topos = {"fvtopo": (lambda: FVTopo())}

if __name__ == "__main__":
    topo = FVTopo()
    net = Mininet(
        topo=topo,
        switch=OVSKernelSwitch,
        build=False,
        autoSetMacs=True,
        autoStaticArp=True,
        link=TCLink,
    )
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)
    net.build()
    net.start()
    CLI(net)
    net.stop()

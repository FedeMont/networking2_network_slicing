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
        machinary_link_config = {"bw": 1000}  # IoT
        mqtt_link_config = {"bw": 100}
        std_link_config = {}

        # Create switch nodes
        for i in range(11):
            sconfig = {"dpid": "%016x" % (i + 1)}
            self.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)

        # Create host nodes
        for i in range(12):
            self.addHost("h%d" % (i + 1), **hconfig)

        # Iot
        # -------------------------------------------
        self.addLink("s4", "s6", **mqtt_link_config)
        self.addLink("s6", "s5", **mqtt_link_config)
        self.addLink("s4", "s3", **std_link_config)
        self.addLink("s5", "s3", **std_link_config)
        self.addLink("h12", "s4", **std_link_config)
        self.addLink("h11", "s4", **std_link_config)
        self.addLink("h1", "s5", **std_link_config)
        self.addLink("h2", "s5", **std_link_config)

        # Hosts
        # -------------------------------------------
        self.addLink("s7", "s3", **std_link_config)
        self.addLink("s3", "s8", **std_link_config)
        self.addLink("s7", "s1", **std_link_config)
        self.addLink("s1", "s8", **std_link_config)
        self.addLink("s7", "s2", **std_link_config)
        self.addLink("s2", "s8", **std_link_config)
        self.addLink("h10", "s7", **std_link_config)
        self.addLink("h9", "s7", **std_link_config)
        self.addLink("h3", "s8", **std_link_config)
        self.addLink("h4", "s8", **std_link_config)

        # Machineries
        # -------------------------------------------
        self.addLink("s10", "s2", **std_link_config)
        self.addLink("s2", "s9", **std_link_config)
        self.addLink("s10", "s11", **machinary_link_config)
        self.addLink("s11", "s9", **machinary_link_config)
        self.addLink("h8", "s10", **std_link_config)
        self.addLink("h7", "s10", **std_link_config)
        self.addLink("h5", "s9", **std_link_config)
        self.addLink("h6", "s9", **std_link_config)



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

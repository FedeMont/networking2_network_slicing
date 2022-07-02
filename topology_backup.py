#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from comnetsemu.cli import CLI, spawnXtermDocker
from comnetsemu.net import Containernet, VNFManager
from mininet.link import TCLink
from mininet.log import info, setLogLevel
from mininet.node import Controller, RemoteController

if __name__ == "__main__":

    # Only used for auto-testing.
    AUTOTEST_MODE = os.environ.get("COMNETSEMU_AUTOTEST_MODE", 0)

    # Create template host, switch, and link
    hconfig = {"inNamespace": True}
    std_link_config = {"bw": 1000}  # IoT
    http_link_config = {}  # normal hosts
    host_link_config = {}

    setLogLevel("info")

    net = Containernet(
        controller=Controller,
        link=TCLink,
        xterms=False,
        autoSetMacs=True,
        autoStaticArp=True,
    )
    mgr = VNFManager(net)

    info("*** Add controller\n")
    controller = RemoteController("c1", ip="127.0.0.1", port=6633)
    net.addController(controller)

    info("*** Adding switch, hosts and links\n")

    # Create switch nodes
    for i in range(4):
        sconfig = {"dpid": "%016x" % (i + 1)}
        net.addSwitch("s%d" % (i + 1),
                      protocols="OpenFlow10", **sconfig)

    for i in range(7):
        net.addDockerHost("h%d" % (i+1), dimage="dev_test",
                          ip="10.0.0.%d" % (i+1),
                          docker_args={"hostname": "h%d" % (i+1)})

    net.addLink("s1", "s2", **std_link_config)
    net.addLink("s2", "s3", **std_link_config)
    net.addLink("s3", "s1", **std_link_config)

    # Add host links

    # Hosts
    # -------------------------------------------
    net.addLink("h1", "s1", **host_link_config)
    net.addLink("h2", "s1", **host_link_config)
    net.addLink("h1", "s4", **host_link_config)
    net.addLink("h2", "s4", **host_link_config)
    net.addLink("h3", "s4", **host_link_config)

    # Machineries
    # -------------------------------------------
    net.addLink("h5", "s2", **host_link_config)
    net.addLink("h4", "s2", **host_link_config)

    # IoT
    # -------------------------------------------
    net.addLink("h7", "s3", **host_link_config)
    net.addLink("h6", "s3", **host_link_config)

    info("\n*** Starting network\n")
    net.start()

    srv5 = mgr.addContainer(
        "srv5",
        "h5",
        "echo_server",
        "python /home/server.py",
        docker_args={},
    )
    srv6 = mgr.addContainer(
        "srv6",
        "h6",
        "echo_server",
        "python /home/server.py",
        docker_args={},
    )

    srv1 = mgr.addContainer("srv1", "h1", "dev_test", "bash", docker_args={})
    srv2 = mgr.addContainer("srv2", "h2", "dev_test", "bash", docker_args={})
    srv3 = mgr.addContainer("srv3", "h3", "dev_test", "bash", docker_args={})
    srv4 = mgr.addContainer("srv4", "h4", "dev_test", "bash", docker_args={})
    srv7 = mgr.addContainer("srv7", "h7", "dev_test", "bash", docker_args={})
    srv8 = mgr.addContainer("srv8", "h8", "dev_test", "bash", docker_args={})
    srv9 = mgr.addContainer("srv9", "h9", "dev_test", "bash", docker_args={})
    srv10 = mgr.addContainer(
        "srv10", "h10", "dev_test", "bash", docker_args={})
    srv11 = mgr.addContainer(
        "srv11", "h11", "dev_test", "bash", docker_args={})
    srv12 = mgr.addContainer(
        "srv12", "h12", "dev_test", "bash", docker_args={})

    if not AUTOTEST_MODE:
        # Cannot spawn xterm for srv1 since BASH is not installed in the image:
        # echo_server.
        spawnXtermDocker("srv3")
        CLI(net)

    mgr.removeContainer("srv1")
    mgr.removeContainer("srv2")
    mgr.removeContainer("srv3")
    mgr.removeContainer("srv4")
    mgr.removeContainer("srv5")
    mgr.removeContainer("srv6")
    mgr.removeContainer("srv7")
    mgr.removeContainer("srv8")
    mgr.removeContainer("srv9")
    mgr.removeContainer("srv10")
    mgr.removeContainer("srv11")
    mgr.removeContainer("srv12")
    net.stop()
    mgr.stop()

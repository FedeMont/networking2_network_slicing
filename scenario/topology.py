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
    mqtt_link_config = {"bw":1} #IoT
    http_link_config = {"bw": 1000} #normal hosts
    grpc_link_config = {"bw": 100} #machines
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

    info("*** Creating hosts\n")
    h1 = net.addDockerHost(
        "h1",
        dimage="dev_test",
        ip="10.0.0.1",
        docker_args={"hostname": "h1"},
    )
    h2 = net.addDockerHost(
        "h2",
        dimage="dev_test",
        ip="10.0.0.2",
        docker_args={"hostname": "h2"},
    )
    h3 = net.addDockerHost(
        "h3",
        dimage="dev_test",
        ip="10.0.0.3",
        docker_args={"hostname": "h3"},
    )
    h4 = net.addDockerHost(
        "h4",
        dimage="dev_test",
        ip="10.0.0.4",
        docker_args={"hostname": "h4"},
    )
    h5 = net.addDockerHost(
        "h5",
        dimage="dev_test",
        ip="10.0.0.5",
        docker_args={"hostname": "h5"},
    )
    h6 = net.addDockerHost(
        "h6",
        dimage="dev_test",
        ip="10.0.0.6",
        docker_args={"hostname": "h6"},
    )
    h7 = net.addDockerHost(
        "h7",
        dimage="dev_test",
        ip="10.0.0.7",
        docker_args={"hostname": "h7"},
    )
    h8 = net.addDockerHost(
        "h8",
        dimage="dev_test",
        ip="10.0.0.8",
        docker_args={"hostname": "h8"},
    )
    h9 = net.addDockerHost(
        "h9",
        dimage="dev_test",
        ip="10.0.0.9",
        docker_args={"hostname": "h9"},
    )
    h10 = net.addDockerHost(
        "h10",
        dimage="dev_test",
        ip="10.0.0.10",
        docker_args={"hostname": "h10"},
    )
    h11 = net.addDockerHost(
        "h11",
        dimage="dev_test",
        ip="10.0.0.11",
        docker_args={"hostname": "h11"},
    )
    h12 = net.addDockerHost(
        "h12",
        dimage="dev_test",
        ip="10.0.0.12",
        docker_args={"hostname": "h12"},
    )
    
    info("*** Adding switch and links\n")

    for i in range(12):
        sconfig = {"dpid": "%016x" % (i + 1)}
        net.addSwitch("s%d" % (i + 1), protocols="OpenFlow10", **sconfig)


    # Host slice
    #-------------------------------------------
    net.addLink("s1", "s8", **http_link_config)
    net.addLink("s1", "s7", **http_link_config)
    #-------------------------------------------

    # Iot Slice 
    #-------------------------------------------
    net.addLink("s3", "s4", **mqtt_link_config)
    net.addLink("s3", "s5", **mqtt_link_config)

    # TODO: Da verifiare
    net.addLink("s3", "s7", **mqtt_link_config)
    net.addLink("s3", "s8", **mqtt_link_config)
    # 

    net.addLink("s4", "s6", **mqtt_link_config)
    net.addLink("s5", "s6", **mqtt_link_config)
    #-------------------------------------------

    # Machines Slice
    #-------------------------------------------
    # TODO: Da verifiare
    net.addLink("s2", "s8", **grpc_link_config)
    net.addLink("s2", "s7", **grpc_link_config)
    #

    net.addLink("s2", "s9", **grpc_link_config)
    net.addLink("s2", "s10", **grpc_link_config)
    net.addLink("s11", "s9", **grpc_link_config)
    net.addLink("s11", "s10", **grpc_link_config)
    #-------------------------------------------


    # Add host links

    # Hosts
    #-------------------------------------------
    net.addLink("h3", "s8", **host_link_config)
    net.addLink("h4", "s8", **host_link_config)
    net.addLink("h9", "s7", **host_link_config)
    net.addLink("h10", "s7", **host_link_config)

    # Machines
    #-------------------------------------------
    net.addLink("h5", "s9", **host_link_config)
    net.addLink("h6", "s9", **host_link_config)
    net.addLink("h7", "s10", **host_link_config)
    net.addLink("h8", "s10", **host_link_config)

    # IoT Slice
    #-------------------------------------------
    net.addLink("h1", "s5", **host_link_config)
    net.addLink("h2", "s5", **host_link_config)
    net.addLink("h11", "s4", **host_link_config)
    net.addLink("h12", "s4", **host_link_config)

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
    srv10 = mgr.addContainer("srv10", "h10", "dev_test", "bash", docker_args={})
    srv11 = mgr.addContainer("srv11", "h11", "dev_test", "bash", docker_args={})
    srv12 = mgr.addContainer("srv12", "h12", "dev_test", "bash", docker_args={})

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

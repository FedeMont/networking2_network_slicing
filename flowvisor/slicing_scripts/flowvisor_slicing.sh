#!/bin/bash

# Start FlowVisor service
echo "Starting FlowVisor service..."
sudo /etc/init.d/flowvisor start

echo "Waiting for service to start..."
sleep 10
echo "Done."

# Get FlowVisor current config
echo "FlowVisor initial config:"
fvctl -f /etc/flowvisor/flowvisor.passwd get-config

# Get FlowVisor current defined slices
echo "FlowVisor initially defined slices:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Get FlowVisor current defined flowspaces
echo "FlowVisor initially defined flowspaces:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace

# Get FlowVisor connected switches
echo "FlowVisor connected switches:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-datapaths

# Get FlowVisor connected switches links up
echo "FlowVisor connected switches links:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-links

# Define the FlowVisor slices
echo "Definition of FlowVisor slices..."
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice iot tcp:localhost:10001 admin@iotslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice machineries tcp:localhost:10002 admin@machineriesslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice hosts tcp:localhost:10003 admin@hostsslice

# Check defined slices
echo "Check slices just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Define flowspaces
echo "Definition of flowspaces..."
# add-flowspace: <flowspace-name> <dpid> <priority> <match> <slice-perm>
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7 7 1 any hosts=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1 1 1 any hosts=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid8 8 1 any hosts=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3 3 1 any hosts=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2 2 1 any hosts=7

# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port3 3 1 in_port=3 hosts=7
# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port4 3 1 in_port=4 hosts=7
# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port1 2 1 in_port=1 hosts=7
# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port2 2 1 in_port=2 hosts=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid10 10 1 any machineries=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid11 11 1 any machineries=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid9 9 1 any machineries=7
# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port3 2 1 in_port=3 machineries=7
# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port4 2 1 in_port=4 machineries=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6 6 1 any iot=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4 4 1 any iot=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 1 any iot=7
# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port1 3 1 in_port=1 hosts=7
# fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port2 3 1 in_port=2 hosts=7


# Check all the flowspaces added
echo "Check all flowspaces just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace

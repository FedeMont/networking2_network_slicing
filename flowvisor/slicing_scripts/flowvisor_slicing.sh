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
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice upper tcp:localhost:10001 admin@upperslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice middle tcp:localhost:10002 admin@middleslice
fvctl -f /etc/flowvisor/flowvisor.passwd add-slice lower tcp:localhost:10003 admin@lowerslice

# Check defined slices
echo "Check slices just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-slices

# Define flowspaces
echo "Definition of flowspaces..."
# add-flowspace: <flowspace-name> <dpid> <priority> <match> <slice-perm>
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid1 1 1 any middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port1 2 1 in_port=1 middle=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port4 2 1 in_port=4 middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port2 2 1 in_port=2 lower=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid2-port3 2 1 in_port=3 lower=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port1 3 1 in_port=1 upper=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port2 3 1 in_port=2 upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port3 3 1 in_port=3 middle=7
fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid3-port4 3 1 in_port=4 middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid4 4 1 any upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid5 5 1 any upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid6 6 1 any upper=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid7 7 1 any middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid8 8 1 any middle=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid9 9 1 any lower=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid10 10 1 any lower=7

fvctl -f /etc/flowvisor/flowvisor.passwd add-flowspace dpid11 11 1 any lower=7

# Check all the flowspaces added
echo "Check all flowspaces just defined:"
fvctl -f /etc/flowvisor/flowvisor.passwd list-flowspace

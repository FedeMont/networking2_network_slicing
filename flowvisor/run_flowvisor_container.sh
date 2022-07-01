#!/bin/bash
#
# About: Run FlowVisor docker image with host networking and interactive mode
#

docker run -v /home/vagrant/comnetsemu/app/networking2_network_slicing/flowvisor/slicing_scripts:/root/slicing_scripts -it --rm --network host flowvisor:latest /bin/bash

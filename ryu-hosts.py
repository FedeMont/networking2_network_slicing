from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_0

from ryu.lib.mac import haddr_to_bin
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types


class HostSlicing(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_0.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(HostSlicing, self).__init__(*args, **kwargs)

        # out_port = slice_to_port[dpid][mac_address]
        self.mac_to_port = {
            2: {
                "00:00:00:00:00:03": 2, 
                "00:00:00:00:00:04": 2,
                "00:00:00:00:00:05": 4,
                "00:00:00:00:00:06": 4,
                "00:00:00:00:00:07": 3,
                "00:00:00:00:00:08": 3,
                "00:00:00:00:00:09": 1,
                "00:00:00:00:00:0a": 1
            },
            7: {
                "00:00:00:00:00:01": 1, 
                "00:00:00:00:00:02": 1,
                "00:00:00:00:00:03": 2, 
                "00:00:00:00:00:04": 2,
                "00:00:00:00:00:09": 5,
                "00:00:00:00:00:0a": 4
            },
            8: {
                "00:00:00:00:00:01": 1, 
                "00:00:00:00:00:02": 1,
                "00:00:00:00:00:03": 4, 
                "00:00:00:00:00:04": 5, 
                "00:00:00:00:00:09": 2,
                "00:00:00:00:00:0a": 2
            }
        }

        # out_port = slice_to_port[dpid][in_port]
        self.slice_to_port = {
            1: {1: 2, 2: 1},
            3: {3: 2, 4: 2},
            # 7: {4: 2, 5: 2},
            # 8: {4: 2, 5: 2}
        }

        self.end_switches = [1, 2, 3, 7, 8]
    
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # install the table-miss flow entry.
        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(ofproto.OFPP_CONTROLLER)
        ]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        # construct flow_mod message and send it.
        mod = parser.OFPFlowMod(
            datapath=datapath,
            match=match,
            cookie=0,
            command=ofproto.OFPFC_ADD,
            idle_timeout=0,
            hard_timeout=0,
            priority=priority,
            flags=ofproto.OFPFF_SEND_FLOW_REM,
            actions=actions,
        )
        datapath.send_msg(mod)

    def _send_package(self, msg, datapath, in_port, actions):
        data = None
        ofproto = datapath.ofproto
        if msg.buffer_id == ofproto.OFP_NO_BUFFER:
            data = msg.data

        out = datapath.ofproto_parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=data,
        )
        # self.logger.info("send_msg %s", out)
        datapath.send_msg(out)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        in_port = msg.in_port
        dpid = datapath.id

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        dst = eth.dst
        src = eth.src

        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            # ignore lldp packet
            # self.logger.info("LLDP packet discarded.")
            return

        if dst[:2] == '33':
            return

        print(dst, dpid, in_port)
        self.logger.info("INFO packet arrived in s%s (in_port=%s), dst=%s, src=%s", dpid, in_port, dst, src)

        if dpid in self.end_switches:
            in_slice = dpid in self.slice_to_port
            in_in_port = in_slice and (in_port in self.slice_to_port[dpid])
            in_mac = dpid in self.mac_to_port
            in_dst = in_mac and (dst in self.mac_to_port[dpid])

            if not in_in_port and in_dst:
                out_port = self.mac_to_port[dpid][dst]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s), dst=%s, src=%s w/ mac-to-port rule",
                    dpid,
                    out_port,
                    dst,
                    src
                )

                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                # match = datapath.ofproto_parser.OFPMatch(in_port=in_port)
                # self.logger.info("INFO sending packet from s%s (out_port=%s)", dpid, out_port)
                match = datapath.ofproto_parser.OFPMatch(dl_dst=dst)
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)

            elif in_in_port and not in_dst:
                out_port = self.slice_to_port[dpid][in_port]
                self.logger.info(
                    "INFO sending packet from s%s (out_port=%s), dst=%s, src=%s w/ slice-to-port rule",
                    dpid,
                    out_port,
                    dst,
                    src
                )
                actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
                match = datapath.ofproto_parser.OFPMatch(in_port = in_port)
                self.add_flow(datapath, 1, match, actions)
                self._send_package(msg, datapath, in_port, actions)
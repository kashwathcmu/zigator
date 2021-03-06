# Copyright (C) 2020 Dimitrios-Georgios Akestoridis
#
# This file is part of Zigator.
#
# Zigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 only,
# as published by the Free Software Foundation.
#
# Zigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zigator. If not, see <https://www.gnu.org/licenses/>.

import struct

from scapy.all import Dot15d4AuxSecurityHeader
from scapy.all import Dot15d4Beacon
from scapy.all import Dot15d4Cmd
from scapy.all import Dot15d4CmdAssocReq
from scapy.all import Dot15d4CmdAssocResp
from scapy.all import Dot15d4CmdCoordRealign
from scapy.all import Dot15d4CmdCoordRealignPage
from scapy.all import Dot15d4CmdDisassociation
from scapy.all import Dot15d4CmdGTSReq
from scapy.all import Dot15d4Data
from scapy.all import Dot15d4FCS
from scapy.all import ZigBeeBeacon
from scapy.all import ZigbeeNWK

from .. import config
from .nwk_fields import nwk_fields


def get_mac_frametype(pkt):
    mac_frametypes = {
        0: "MAC Beacon",
        1: "MAC Data",
        2: "MAC Acknowledgment",
        3: "MAC Command"
    }
    frametype_id = pkt[Dot15d4FCS].fcf_frametype
    return mac_frametypes.get(frametype_id, "Unknown MAC frame type")


def get_mac_security(pkt):
    mac_security_states = {
        0: "MAC Security Disabled",
        1: "MAC Security Enabled"
    }
    sec_state = pkt[Dot15d4FCS].fcf_security
    return mac_security_states.get(sec_state, "Unknown MAC security state")


def get_mac_framepending(pkt):
    mac_framepending_states = {
        0: "No additional packets are pending for the receiver",
        1: "Additional packets are pending for the receiver"
    }
    fp_state = pkt[Dot15d4FCS].fcf_pending
    return mac_framepending_states.get(fp_state, "Unknown MAC FP state")


def get_mac_ackreq(pkt):
    mac_ackreq_states = {
        0: "The sender does not request a MAC Acknowledgment",
        1: "The sender requests a MAC Acknowledgment"
    }
    ar_state = pkt[Dot15d4FCS].fcf_ackreq
    return mac_ackreq_states.get(ar_state, "Unknown MAC AR state")


def get_mac_panidcomp(pkt):
    mac_panidcomp_states = {
        0: "Do not compress the source PAN ID",
        1: "The source PAN ID is the same as the destination PAN ID"
    }
    pc_state = pkt[Dot15d4FCS].fcf_panidcompress
    return mac_panidcomp_states.get(pc_state, "Unknown MAC PC state")


def get_mac_dstaddrmode(pkt):
    mac_dstaddr_modes = {
        0: "No destination MAC address",
        2: "Short destination MAC address",
        3: "Extended destination MAC address"
    }
    dstaddr_mode = pkt[Dot15d4FCS].fcf_destaddrmode
    return mac_dstaddr_modes.get(dstaddr_mode, "Unknown MAC DA mode")


def get_mac_frameversion(pkt):
    mac_frame_versions = {
        0: "IEEE 802.15.4-2003 Frame Version",
        1: "IEEE 802.15.4-2006 Frame Version",
        2: "IEEE 802.15.4-2015 Frame Version"
    }
    fv_id = pkt[Dot15d4FCS].fcf_framever
    return mac_frame_versions.get(fv_id, "Unknown MAC frame version")


def get_mac_srcaddrmode(pkt):
    mac_srcaddr_modes = {
        0: "No source MAC address",
        2: "Short source MAC address",
        3: "Extended source MAC address"
    }
    srcaddr_mode = pkt[Dot15d4FCS].fcf_srcaddrmode
    return mac_srcaddr_modes.get(srcaddr_mode, "Unknown MAC SA mode")


def get_mac_command(pkt):
    mac_commands = {
        1: "MAC Association Request",
        2: "MAC Association Response",
        3: "MAC Disassociation Notification",
        4: "MAC Data Request",
        5: "MAC PAN ID Conflict Notification",
        6: "MAC Orphan Notification",
        7: "MAC Beacon Request",
        8: "MAC Coordinator Realignment",
        9: "MAC GTS Request"
    }
    command_id = pkt[Dot15d4Cmd].cmd_id
    return mac_commands.get(command_id, "Unknown MAC Command")


def get_mac_assocreq_apc(pkt):
    apc_states = {
        0: "The sender is not capable of becoming a PAN coordinator",
        1: "The sender is capable of becoming a PAN coordinator"
    }
    apc_state = pkt[Dot15d4CmdAssocReq].alternate_pan_coordinator
    return apc_states.get(apc_state, "Unknown APC state")


def get_mac_assocreq_devtype(pkt):
    device_types = {
        0: "Reduced-Function Device",
        1: "Full-Function Device"
    }
    devtype_id = pkt[Dot15d4CmdAssocReq].device_type
    return device_types.get(devtype_id, "Unknown device type")


def get_mac_assocreq_powsrc(pkt):
    power_sources = {
        0: "The sender is not a mains-powered device",
        1: "The sender is a mains-powered device"
    }
    pwrsrc_id = pkt[Dot15d4CmdAssocReq].power_source
    return power_sources.get(pwrsrc_id, "Unknown power source")


def get_mac_assocreq_rxidle(pkt):
    rxidle_states = {
        0: "Disables the receiver to conserve power when idle",
        1: "Does not disable the receiver to conserve power"
    }
    rxidle_state = pkt[Dot15d4CmdAssocReq].receiver_on_when_idle
    return rxidle_states.get(rxidle_state, "Unknown RX state when idle")


def get_mac_assocreq_seccap(pkt):
    seccap_states = {
        0: "Cannot transmit and receive secure MAC frames",
        1: "Can transmit and receive secure MAC frames"
    }
    seccap_state = pkt[Dot15d4CmdAssocReq].security_capability
    return seccap_states.get(seccap_state, "Unknown MAC security capacity")


def get_mac_assocreq_allocaddr(pkt):
    allocaddr_states = {
        0: "Does not request a short address",
        1: "Requests a short address"
    }
    allocaddr_state = pkt[Dot15d4CmdAssocReq].allocate_address
    return allocaddr_states.get(allocaddr_state, "Unknown address allocation")


def get_mac_assocrsp_status(pkt):
    assoc_statuses = {
        0: "Association successful",
        1: "PAN at capacity",
        2: "PAN access denied"
    }
    assoc_status = pkt[Dot15d4CmdAssocResp].association_status
    return assoc_statuses.get(assoc_status, "Unknown association status")


def get_mac_disassoc_reason(pkt):
    disassoc_reasons = {
        1: "The coordinator wishes the device to leave the PAN",
        2: "The device wishes to leave the PAN"
    }
    reason_id = pkt[Dot15d4CmdDisassociation].disassociation_reason
    return disassoc_reasons.get(reason_id, "Unknown disassociation reason")


def get_mac_gtsreq_dir(pkt):
    gts_direction = {
        0: "Transmit-Only GTS",
        1: "Receive-Only GTS"
    }
    dir_id = pkt[Dot15d4CmdGTSReq].gts_dir
    return gts_direction.get(dir_id, "Unknown GTS direction")


def get_mac_gtsreq_chartype(pkt):
    charact_types = {
        0: "GTS Deallocation",
        1: "GTS Allocation"
    }
    chartype_id = pkt[Dot15d4CmdGTSReq].charact_type
    return charact_types.get(chartype_id, "Unknown GTS characteristics type")


def get_mac_beacon_pancoord(pkt):
    panc_states = {
        0: "The sender is not the PAN coordinator",
        1: "The sender is the PAN coordinator"
    }
    panc_state = pkt[Dot15d4Beacon].sf_pancoord
    return panc_states.get(panc_state, "Unknown PAN coordinator state")


def get_mac_beacon_assocpermit(pkt):
    assocp_states = {
        0: "The sender is currently not accepting association requests",
        1: "The sender is currently accepting association requests"
    }
    assocp_state = pkt[Dot15d4Beacon].sf_assocpermit
    return assocp_states.get(assocp_state, "Unknown Association Permit state")


def mac_assocreq(pkt):
    # Capability Information field (1 byte)
    config.entry["mac_assocreq_apc"] = get_mac_assocreq_apc(pkt)
    config.entry["mac_assocreq_devtype"] = get_mac_assocreq_devtype(pkt)
    config.entry["mac_assocreq_powsrc"] = get_mac_assocreq_powsrc(pkt)
    config.entry["mac_assocreq_rxidle"] = get_mac_assocreq_rxidle(pkt)
    config.entry["mac_assocreq_seccap"] = get_mac_assocreq_seccap(pkt)
    config.entry["mac_assocreq_allocaddr"] = get_mac_assocreq_allocaddr(pkt)

    return


def mac_assocrsp(pkt):
    # Short Address field (2 bytes)
    config.entry["mac_assocrsp_shortaddr"] = "0x{:04x}".format(
        pkt[Dot15d4CmdAssocResp].short_address)

    # Association Status field (1 byte)
    config.entry["mac_assocrsp_status"] = get_mac_assocrsp_status(pkt)

    return


def mac_disassoc(pkt):
    # Disassociation Reason field (1 byte)
    config.entry["mac_disassoc_reason"] = get_mac_disassoc_reason(pkt)

    return


def mac_realign(pkt):
    # PAN Identifier field (2 bytes)
    config.entry["mac_realign_panid"] = "0x{:04x}".format(
        pkt[Dot15d4CmdCoordRealign].panid)

    # Coordinator Short Address field (2 bytes)
    config.entry["mac_realign_coordaddr"] = "0x{:04x}".format(
        pkt[Dot15d4CmdCoordRealign].coord_address)

    # Channel Number field (1 byte)
    config.entry["mac_realign_channel"] = pkt[Dot15d4CmdCoordRealign].channel

    # Short Address field (2 bytes)
    config.entry["mac_realign_shortaddr"] = "0x{:04x}".format(
        pkt[Dot15d4CmdCoordRealign].dev_address)

    # Channel Page field (0/1 byte)
    if pkt.haslayer(Dot15d4CmdCoordRealignPage):
        config.entry["mac_realign_page"] = (
            pkt[Dot15d4CmdCoordRealignPage].channel_page
        )


def mac_gtsreq(pkt):
    # GTS Characteristics field (1 byte)
    config.entry["mac_gtsreq_length"] = pkt[Dot15d4CmdGTSReq].gts_len
    config.entry["mac_gtsreq_dir"] = get_mac_gtsreq_dir(pkt)
    config.entry["mac_gtsreq_chartype"] = get_mac_gtsreq_chartype(pkt)

    return


def mac_command(pkt, msg_queue):
    # Destination Addressing fields (0/4/10 bytes)
    if (config.entry["mac_dstaddrmode"]
            == "Short destination MAC address"):
        config.entry["mac_dstpanid"] = "0x{:04x}".format(
            pkt[Dot15d4Cmd].dest_panid)
        config.entry["mac_dstshortaddr"] = "0x{:04x}".format(
            pkt[Dot15d4Cmd].dest_addr)
    elif (config.entry["mac_dstaddrmode"]
            == "Extended destination MAC address"):
        config.entry["mac_dstpanid"] = "0x{:04x}".format(
            pkt[Dot15d4Cmd].dest_panid)
        config.entry["mac_dstextendedaddr"] = format(
            pkt[Dot15d4Cmd].dest_addr, "016x")
    elif (config.entry["mac_dstaddrmode"]
            != "No destination MAC address"):
        config.entry["error_msg"] = "Unknown MAC DA mode"
        return

    # Source Addressing fields (0/2/4/8/10 bytes)
    if (config.entry["mac_srcaddrmode"]
            == "Short source MAC address"):
        if (config.entry["mac_panidcomp"]
                == "Do not compress the source PAN ID"):
            config.entry["mac_srcpanid"] = "0x{:04x}".format(
                pkt[Dot15d4Cmd].src_panid)
        elif (config.entry["mac_panidcomp"]
                != "The source PAN ID is the same as the destination PAN ID"):
            config.entry["error_msg"] = "Unknown MAC PC state"
            return
        config.entry["mac_srcshortaddr"] = "0x{:04x}".format(
            pkt[Dot15d4Cmd].src_addr)
    elif (config.entry["mac_srcaddrmode"]
            == "Extended source MAC address"):
        if (config.entry["mac_panidcomp"]
                == "Do not compress the source PAN ID"):
            config.entry["mac_srcpanid"] = "0x{:04x}".format(
                pkt[Dot15d4Cmd].src_panid)
        elif (config.entry["mac_panidcomp"]
                != "The source PAN ID is the same as the destination PAN ID"):
            config.entry["error_msg"] = "Unknown MAC PC state"
            return
        config.entry["mac_srcextendedaddr"] = format(
            pkt[Dot15d4Cmd].src_addr, "016x")
    elif (config.entry["mac_srcaddrmode"]
            != "No source MAC address"):
        config.entry["error_msg"] = "Unknown MAC SA mode"
        return

    # Command Frame Identifier field (1 byte)
    config.entry["mac_cmd_id"] = get_mac_command(pkt)

    # Compute the MAC Command Payload Length
    # The constant 6 was derived by summing the following:
    #  2: MAC Frame Control
    #  1: MAC Sequence Number
    #  1: MAC Command Frame Identifier
    #  2: MAC Frame Check Sequence
    config.entry["mac_cmd_payloadlength"] = config.entry["phy_length"] - 6
    # Compute the length of the MAC Destination Addressing fields
    if (config.entry["mac_dstaddrmode"]
            == "Short destination MAC address"):
        config.entry["mac_cmd_payloadlength"] -= 4
    elif (config.entry["mac_dstaddrmode"]
            == "Extended destination MAC address"):
        config.entry["mac_cmd_payloadlength"] -= 10
    elif (config.entry["mac_dstaddrmode"]
            != "No destination MAC address"):
        config.entry["error_msg"] = "Unknown MAC DA mode"
        return
    # Compute the length of the MAC Source Addressing fields
    if (config.entry["mac_srcaddrmode"]
            == "Short source MAC address"):
        if (config.entry["mac_panidcomp"]
                == "Do not compress the source PAN ID"):
            config.entry["mac_cmd_payloadlength"] -= 2
        elif (config.entry["mac_panidcomp"]
                != "The source PAN ID is the same as the destination PAN ID"):
            config.entry["error_msg"] = "Unknown MAC PC state"
            return
        config.entry["mac_cmd_payloadlength"] -= 2
    elif (config.entry["mac_srcaddrmode"]
            == "Extended source MAC address"):
        if (config.entry["mac_panidcomp"]
                == "Do not compress the source PAN ID"):
            config.entry["mac_cmd_payloadlength"] -= 2
        elif (config.entry["mac_panidcomp"]
                != "The source PAN ID is the same as the destination PAN ID"):
            config.entry["error_msg"] = "Unknown MAC PC state"
            return
        config.entry["mac_cmd_payloadlength"] -= 8
    elif (config.entry["mac_srcaddrmode"]
            != "No source MAC address"):
        config.entry["error_msg"] = "Unknown MAC SA mode"
        return
    # Compute the length of the MAC Auxiliary Security Header field
    if config.entry["mac_security"] == "MAC Security Enabled":
        msg_queue.put(
            (config.DEBUG_MSG,
             "Ignored packet #{} in {} because it utilizes "
             "security services on the MAC layer"
             "".format(config.entry["pkt_num"],
                       config.entry["pcap_filename"])))
        config.entry["error_msg"] = (
            "Ignored MAC command with enabled MAC-layer security"
        )
        return
    elif config.entry["mac_security"] != "MAC Security Disabled":
        config.entry["error_msg"] = "Unknown MAC security state"
        return

    # Command Payload field (variable)
    if config.entry["mac_cmd_id"] == "MAC Association Request":
        mac_assocreq(pkt)
        return
    elif config.entry["mac_cmd_id"] == "MAC Association Response":
        mac_assocrsp(pkt)
        return
    elif config.entry["mac_cmd_id"] == "MAC Disassociation Notification":
        mac_disassoc(pkt)
        return
    elif config.entry["mac_cmd_id"] == "MAC Data Request":
        # MAC Data Requests do not contain any other fields
        return
    elif config.entry["mac_cmd_id"] == "MAC PAN ID Conflict Notification":
        # MAC PAN ID Conflict Notifications do not contain any other fields
        return
    elif config.entry["mac_cmd_id"] == "MAC Orphan Notification":
        # MAC Orphan Notifications do not contain any other fields
        return
    elif config.entry["mac_cmd_id"] == "MAC Beacon Request":
        # MAC Beacon Requests do not contain any other fields
        return
    elif config.entry["mac_cmd_id"] == "MAC Coordinator Realignment":
        mac_realign(pkt)
        return
    elif config.entry["mac_cmd_id"] == "MAC GTS Request":
        mac_gtsreq(pkt)
        return
    else:
        config.entry["error_msg"] = "Unknown MAC Command"
        return


def mac_beacon(pkt, msg_queue):
    if config.entry["mac_panidcomp"] != "Do not compress the source PAN ID":
        config.entry["error_msg"] = (
            "The source PAN ID of MAC Beacons should not be compressed"
        )
        return
    elif config.entry["mac_dstaddrmode"] != "No destination MAC address":
        config.entry["error_msg"] = (
            "MAC Beacons should not contain a destination PAN ID and address"
        )
        return

    # Addressing fields (4/10 bytes)
    config.entry["mac_srcpanid"] = "0x{:04x}".format(
        pkt[Dot15d4Beacon].src_panid)
    if config.entry["mac_srcaddrmode"] == "Short source MAC address":
        config.entry["mac_srcshortaddr"] = "0x{:04x}".format(
            pkt[Dot15d4Beacon].src_addr)
    elif config.entry["mac_srcaddrmode"] == "Extended source MAC address":
        config.entry["mac_srcextendedaddr"] = format(
            pkt[Dot15d4Beacon].src_addr, "016x")
    elif config.entry["mac_srcaddrmode"] == "No source MAC address":
        config.entry["error_msg"] = (
            "MAC Beacons should contain a source PAN ID and address"
        )
        return
    else:
        config.entry["error_msg"] = "Unknown MAC SA mode"
        return

    # Superframe Specification field (2 bytes)
    config.entry["mac_beacon_beaconorder"] = pkt[Dot15d4Beacon].sf_beaconorder
    config.entry["mac_beacon_sforder"] = pkt[Dot15d4Beacon].sf_sforder
    config.entry["mac_beacon_finalcap"] = pkt[Dot15d4Beacon].sf_finalcapslot
    config.entry["mac_beacon_ble"] = pkt[Dot15d4Beacon].sf_battlifeextend
    config.entry["mac_beacon_pancoord"] = get_mac_beacon_pancoord(pkt)
    config.entry["mac_beacon_assocpermit"] = get_mac_beacon_assocpermit(pkt)

    # GTS Specification field (1 byte)
    config.entry["mac_beacon_gtsnum"] = pkt[Dot15d4Beacon].gts_spec_desccount
    config.entry["mac_beacon_gtspermit"] = pkt[Dot15d4Beacon].gts_spec_permit

    # GTS Directions Mask field (0/1 byte)
    if config.entry["mac_beacon_gtsnum"] > 0:
        config.entry["mac_beacon_gtsmask"] = pkt[Dot15d4Beacon].gts_dir_mask

    # GTS List field (variable)
    if config.entry["mac_beacon_gtsnum"] > 0:
        msg_queue.put(
            (config.DEBUG_MSG,
             "Packet #{} in {} contains a GTS List field "
             "which could not be processed"
             "".format(config.entry["pkt_num"],
                       config.entry["pcap_filename"])))
        config.entry["error_msg"] = "Could not process the GTS List"
        return

    # Pending Address Specification field (1 byte)
    config.entry["mac_beacon_nsap"] = pkt[Dot15d4Beacon].pa_num_short
    config.entry["mac_beacon_neap"] = pkt[Dot15d4Beacon].pa_num_long

    # Address List field (variable)
    config.entry["mac_beacon_shortaddresses"] = ",".join("0x{:04x}".format(
        addr) for addr in pkt[Dot15d4Beacon].pa_short_addresses)
    config.entry["mac_beacon_extendedaddresses"] = ",".join(format(
        addr, "016x") for addr in pkt[Dot15d4Beacon].pa_long_addresses)

    # Beacon Payload field (variable)
    if pkt.haslayer(ZigBeeBeacon):
        nwk_fields(pkt, msg_queue)
        return
    else:
        config.entry["error_msg"] = (
            "There is no beacon payload from the Zigbee NWK layer"
        )
        return


def mac_data(pkt, msg_queue):
    # Destination Addressing fields (0/4/10 bytes)
    if (config.entry["mac_dstaddrmode"]
            == "Short destination MAC address"):
        config.entry["mac_dstpanid"] = "0x{:04x}".format(
            pkt[Dot15d4Data].dest_panid)
        config.entry["mac_dstshortaddr"] = "0x{:04x}".format(
            pkt[Dot15d4Data].dest_addr)
    elif (config.entry["mac_dstaddrmode"]
            == "Extended destination MAC address"):
        config.entry["mac_dstpanid"] = "0x{:04x}".format(
            pkt[Dot15d4Data].dest_panid)
        config.entry["mac_dstextendedaddr"] = format(
            pkt[Dot15d4Data].dest_addr, "016x")
    elif (config.entry["mac_dstaddrmode"]
            != "No destination MAC address"):
        config.entry["error_msg"] = "Unknown MAC DA mode"
        return

    # Source Addressing fields (0/2/4/8/10 bytes)
    if (config.entry["mac_srcaddrmode"]
            == "Short source MAC address"):
        if (config.entry["mac_panidcomp"]
                == "Do not compress the source PAN ID"):
            config.entry["mac_srcpanid"] = "0x{:04x}".format(
                pkt[Dot15d4Data].src_panid)
        elif (config.entry["mac_panidcomp"]
                != "The source PAN ID is the same as the destination PAN ID"):
            config.entry["error_msg"] = "Unknown MAC PC state"
            return
        config.entry["mac_srcshortaddr"] = "0x{:04x}".format(
            pkt[Dot15d4Data].src_addr)
    elif (config.entry["mac_srcaddrmode"]
            == "Extended source MAC address"):
        if (config.entry["mac_panidcomp"]
                == "Do not compress the source PAN ID"):
            config.entry["mac_srcpanid"] = "0x{:04x}".format(
                pkt[Dot15d4Data].src_panid)
        elif (config.entry["mac_panidcomp"]
                != "The source PAN ID is the same as the destination PAN ID"):
            config.entry["error_msg"] = "Unknown MAC PC state"
            return
        config.entry["mac_srcextendedaddr"] = format(
            pkt[Dot15d4Data].src_addr, "016x")
    elif (config.entry["mac_srcaddrmode"]
            != "No source MAC address"):
        config.entry["error_msg"] = "Unknown MAC SA mode"
        return

    # Data Payload field (variable)
    if pkt.haslayer(ZigbeeNWK):
        nwk_fields(pkt, msg_queue)
        return
    else:
        config.entry["error_msg"] = "There are no Zigbee NWK fields"
        return


def mac_fields(pkt, msg_queue):
    """Parse IEEE 802.15.4 MAC fields."""
    if pkt[Dot15d4FCS].fcs is None:
        config.entry["error_msg"] = (
            "PE201: The frame check sequence (FCS) field is not included"
        )
        return

    comp_fcs = struct.unpack("<H", pkt.compute_fcs(bytes(pkt)[:-2]))[0]
    if pkt[Dot15d4FCS].fcs != comp_fcs:
        msg_queue.put(
            (config.DEBUG_MSG,
             "The received FCS (0x{:04x}), for packet #{} in {}, "
             "does not match the computed FCS (0x{:04x})"
             "".format(pkt[Dot15d4FCS].fcs,
                       config.entry["pkt_num"],
                       config.entry["pcap_filename"],
                       comp_fcs)))
        config.entry["error_msg"] = (
            "PE202: Incorrect frame check sequence (FCS)"
        )
        return

    # Frame Check Sequence field (2 bytes)
    config.entry["mac_fcs"] = "0x{:04x}".format(pkt[Dot15d4FCS].fcs)

    # Frame Control field (2 bytes)
    config.entry["mac_frametype"] = get_mac_frametype(pkt)
    config.entry["mac_security"] = get_mac_security(pkt)
    config.entry["mac_framepending"] = get_mac_framepending(pkt)
    config.entry["mac_ackreq"] = get_mac_ackreq(pkt)
    config.entry["mac_panidcomp"] = get_mac_panidcomp(pkt)
    config.entry["mac_dstaddrmode"] = get_mac_dstaddrmode(pkt)
    config.entry["mac_frameversion"] = get_mac_frameversion(pkt)
    config.entry["mac_srcaddrmode"] = get_mac_srcaddrmode(pkt)

    # Sequence Number field (1 byte)
    config.entry["mac_seqnum"] = pkt[Dot15d4FCS].seqnum

    if config.entry["mac_security"] == "MAC Security Enabled":
        # Auxiliary Security Header field (0/5/6/10/14 bytes)
        if pkt.haslayer(Dot15d4AuxSecurityHeader):
            # Zigbee does not utilize any security services on the MAC layer
            msg_queue.put(
                (config.DEBUG_MSG,
                 "The packet #{} in {} is utilizing "
                 "security services on the MAC layer"
                 "".format(config.entry["pkt_num"],
                           config.entry["pcap_filename"])))
            config.entry["error_msg"] = (
                "Ignored the MAC Auxiliary Security Header"
            )
            return
        else:
            config.entry["error_msg"] = (
                "The MAC Auxiliary Security Header is not included"
            )
            return
    elif config.entry["mac_security"] == "MAC Security Disabled":
        # MAC Payload field (variable)
        if config.entry["mac_frametype"] == "MAC Acknowledgment":
            # MAC Acknowledgments do not contain any other fields
            return
        elif config.entry["mac_frametype"] == "MAC Command":
            if pkt.haslayer(Dot15d4Cmd):
                mac_command(pkt, msg_queue)
                return
            else:
                config.entry["error_msg"] = (
                    "There are no MAC Command fields"
                )
                return
        elif config.entry["mac_frametype"] == "MAC Beacon":
            if pkt.haslayer(Dot15d4Beacon):
                mac_beacon(pkt, msg_queue)
                return
            else:
                config.entry["error_msg"] = (
                    "There are no MAC Beacon fields"
                )
                return
        elif config.entry["mac_frametype"] == "MAC Data":
            if pkt.haslayer(Dot15d4Data):
                mac_data(pkt, msg_queue)
                return
            else:
                config.entry["error_msg"] = (
                    "There are no MAC Data fields"
                )
                return
        else:
            config.entry["error_msg"] = "Unknown MAC frame type"
            return
    else:
        config.entry["error_msg"] = "Unknown MAC security state"
        return

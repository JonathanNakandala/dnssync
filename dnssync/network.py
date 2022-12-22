"""
Network Operations
"""
import sys


from structlog import get_logger

import ifaddr
from scapy.all import srp
from scapy.layers.l2 import ARP
from scapy.layers.inet import Ether

from .models import HostDataModel

log = get_logger()


def get_interface_address(name: str):
    """
    Get the ip and subnet for a network
    """
    adapters = ifaddr.get_adapters()
    interface = next(filter(lambda x: x.name == name, adapters))
    log.info("Found interface", interface=interface)
    for iface_ip in interface.ips:
        if iface_ip.is_IPv4:
            return iface_ip.ip, iface_ip.network_prefix
    raise ValueError("Interface was not found")


def scan_arp(address, prefix) -> list[HostDataModel]:
    """
    Send a Broadcast (ff:ff:ff:ff:ff:ff) ethernet frame
    Collect the responses
    Requires root or CAP_NET_RAW to use raw sockets
    """
    try:
        log.info("Scanning ARP")
        replied_ips, _ = srp(
            Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=f"{address}/{prefix}"), timeout=10
        )
    except PermissionError:
        log.critical(
            "Scapy requires raw socket access. Either CAP_NET_RAW or root required"
        )
        sys.exit()
    answers = [x.answer for x in replied_ips]

    hosts: list[HostDataModel] = []
    for answer in answers:
        hosts.append(HostDataModel(mac=answer.src, ip=answer.psrc))
    return hosts

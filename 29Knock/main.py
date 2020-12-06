#!/usr/bin/python3

import os
import datetime
import struct
import socket
import pcapy
import iptc

sessions = {}
connections = []

secret_key = [5678, 5679, 5678, 5679]
secret_port = "22"
open_period = datetime.timedelta(0, 60)
knock_interval = datetime.timedelta(0, 1)


def select_device():
    devices = pcapy.findalldevs()
    for i, dev in enumerate(devices):
        print("%d. %s" % (i, dev))
    print('Enter interface number:', end=' ')
    num = int(input())
    assert num in range(len(devices)), "Incorrect interface number"
    return devices[num]

def block_port():
    rule = iptc.Rule()
    rule.protocol = "tcp"
    match = iptc.Match(rule, "tcp")
    match.dport = secret_port
    rule.add_match(match)
    target = iptc.Target(rule, "REJECT")
    target.set_parameter("reject-with", "tcp-reset")
    rule.target = target
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)
    print("Port", secret_port, "was blocked")
    return (chain, rule)

def unblock_port(ip_address):
    rule = iptc.Rule()
    rule.protocol = "tcp"
    rule.src = ip_address
    match = iptc.Match(rule, "tcp")
    match.dport = secret_port
    rule.add_match(match)
    rule.target = iptc.Target(rule, "ACCEPT")
    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)
    print("Port", secret_port, "was unblocked for", ip_address)
    return (chain, rule)

def parse(packet):
    ethernet_protocol = hex(socket.ntohs(struct.unpack('H', packet[12:14])[0]))
    if ethernet_protocol == "0x800":
        desc = "IPv4"
    else:
        desc = "Unknown"
    print('Protocol:', ethernet_protocol, '-', desc)
    if desc == "Unknown":
        return None
    ip_header = struct.unpack('!BH4s', packet[23:30])
    src_addr = socket.inet_ntoa(ip_header[2])
    print("IP address:", src_addr)
    ip_protocol = ip_header[0]
    if ip_protocol == 6:
        desc = "TCP"
    elif ip_protocol == 17:
        desc = "UDP"
    else:
        desc = "Unknown"
    print("Protocol:", ip_protocol, '-', desc)
    if desc == "Unknown":
        return None
    port = struct.unpack('!HH', packet[34:38])[1]
    print("Port:", port)
    return (src_addr, port)

def sniff(time, ip_address, port):
    if ip_address in sessions:
        last_knock = sessions[ip_address]
        if last_knock[0] + knock_interval < time or port != secret_key[sessions[ip_address][1]]:
            del sessions[ip_address]
            return
        sessions[ip_address] = (time, last_knock[1] + 1)
    elif port != secret_key[0]:
        return
    else:
        sessions[ip_address] = (time, 1)
    session = sessions[ip_address]
    if session[1] == len(secret_key):
        print("Got right sequence!")
        connections.append((unblock_port(ip_address), time))
        del sessions[ip_address]

def cleanup(now):
    global sessions
    sessions = {k: v for k, v in sessions.items() if v[0] + knock_interval >= now}
    while len(connections) > 0 and connections[0][1] + open_period < now:
        connections[0][0][0].delete_rule(connections[0][0][1])
        connections.pop(0)

def main():
    assert os.getuid() == 0, "Root permissions required"
    device = select_device()
    cap = pcapy.open_live(device, 65536, 1, 50)
    assert cap.datalink() == pcapy.DLT_EN10MB, "Unsupported link type"
    chain, rule = block_port()
    try:
        while True:
            _, packet = cap.next()
            time = datetime.datetime.now()
            print(time, ": packet was captured")
            parsed = parse(packet)
            if parsed:
                sniff(time, parsed[0], parsed[1])
            cleanup(time)
    finally:
        chain.delete_rule(rule)
        for i in connections:
            i[0][0].delete_rule(i[0][1])

if __name__ == "__main__":
    main()

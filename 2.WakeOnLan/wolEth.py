#!/usr/bin/python3
import socket
import sys
import uuid

TYPE = '0842'

mac1 = '0897986f6866';
mac0 = '207918644ff6'


magic = bytes(bytearray.fromhex(''.join(['FFFFFFFFFFFF', mac1 * 16])))
packet = bytes(bytearray.fromhex(''.join([mac0, mac1, TYPE])))+magic

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
sock.bind(('wlp0s20f3',0))
sock.send(packet)
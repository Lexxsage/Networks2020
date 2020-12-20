# -*- coding: utf-8 -*-
from scapy.config import conf
conf.ipv6_enabled = False
from scapy.all import *
from scapy.layers.inet import IP, TCP
import time

class TCPstream:
    def __init__ (self, src, dport, data):
        self.src = src
        self.dport = dport
        self.data = data

streams = []  # array of TCPstream objects

def saveImage(src, format_name, image):
    file_name = str(time.time()) + '.' + format_name
    with open(file_name, 'wb') as file:
        print('File ', file_name, 'created!')
        file.write(image)
        file.close()

def handleStream (stream):
    while True:
        data = stream.data
        content_ptr = data.find(b'\r\n\r\n')
        if content_ptr == -1:
            return  # пакет еще не полный
        content_ptr += len(b'\r\n\r\n')
    
        ### определяем размер даных
        ptr = data.find(b'Content-Length: ')
        if ptr == -1:
            stream.data = data[content_ptr:]  # вырезаем пакет без контента
            continue  # начинаем заново
        string = data[ptr : ptr + 35]
        ptr += len(b'Content-Length: ')
        end = data.find(b'\r\n', ptr)
        content_length = int(data[ptr : end])
    
        ### определяем формат изображения
        ptr = data.find(b'Content-Type: image/')
        if ptr == -1:
            stream.data = data[content_ptr + content_length + 1: ]  # вырезаем пакет без картинки
            continue  # начинаем заново
        ptr += len(b'Content-Type: image/')
        end = data.find(b'\r\n', ptr)
        format_bytes = data[ptr : end]
        format_name = ''
        for c in format_bytes:
            format_name += str(c)

        ### сохраняем изображение
        image = data[content_ptr : content_ptr + content_length]
        if len(image) < content_length:
            return  # пакет еще не полный
        #print('\'Content-dispodition search:', data.find(b'Content-Disposition'))
        saveImage(stream.src, format_name, image)
        stream.data = data[content_ptr + content_length : ]  # вырезаем обработанный пакет

def handlePacket (packet):
    src = packet[IP].src
    dport = packet[TCP].dport
    data = bytes(packet[TCP].payload)
    flag = False
    for stream in streams:
        if src == stream.src and dport == stream.dport:
            stream.data += data
            handleStream(stream)
            flag = True
            break
    if flag == False:
        stream = TCPstream(src, dport, data)
        streams.append(stream)
        handleStream(stream)

print('Sniffing...')
sniff(prn = handlePacket, filter = 'tcp')

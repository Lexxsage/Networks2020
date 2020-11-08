#!/usr/bin/python3
import os
os.sys.path.append('/home/alex/.local/bin/scapy')
os.sys.path.append('/usr/local/lib/python2.7/site-packages')
from scapy import sendrecv
import time

# steals PNG, GIF and JPEG image if it is not fragmented

def small_stealer(packet):
    packet_bytes = bytes(packet)
    begin = packet_bytes.find('\x89PNG'.encode())
    ### PNG ###
    if begin > -1:  # if found PNG beginning
        print ('Found \'\x89PNG\' at', begin)
        end = packet_bytes.find('IEND'.encode())
        if end > -1:  # if found PNG end
            print('---Found \'IEND\' at', end)
            file_name = str(time.time()) + '.png'
            with open(file_name, 'wb') as image_file:
                print('File', file_name, 'created\n')
                image_file.write(packet_bytes[begin:])
                image_file.close()
    ### GIF ###
    begin = packet_bytes.find('GIF8'.encode())
    if begin > -1:  # if found GIF beginning
        print ('Found \'GIF8\' at', begin)
        end = packet_bytes.find(';'.encode())
        if end > -1:  # if found GIF end
            print ('---Found \';\' at', end)
            file_name = str(time.time()) + '.gif'
            with open(file_name, 'wb') as image_file:
                print ('File', file_name, 'created\n')
                image_file.write(packet_bytes[begin:])
                image_file.close()
    ### JPEG ###
    begin = packet_bytes.find((chr(0xFF) + chr(0xD8)).encode())
    if begin > -1:  # if found JPEG beginning
        print ('Found 0xFFD8 at', begin)
        end = packet_bytes.find((chr(0xFF) + chr(0xD9)).encode())
        if end > -1:  # if found JPEG end
            print ('---Found 0xFFD9 at', end)
            file_name = str(time.time()) + '.jpg'
            with open(file_name, 'wb') as image_file:
                print ('File', file_name, 'created\n')
                image_file.write(packet_bytes[begin:])
                image_file.close()


print ('Started sniffing...')
sendrecv.sniff(prn=small_stealer)
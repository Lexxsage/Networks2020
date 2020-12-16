import socket
import time

msg = "Hello!"

host = 'localhost'
port = 11223
addr = (host, port)
socket0 = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
#socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
socket0.connect(addr)
socket0.sendto(msg.encode(), addr)
data = socket0.recv(1024)
print(data.decode())
socket0.sendto(msg.encode(), addr)
data = socket0.recv(1024)
socket0.close()

socket1 = socket.socket()
socket1.connect(addr)
msg = "HTTP1.1"
socket1.sendto(msg.encode(), addr)
socket1.close()

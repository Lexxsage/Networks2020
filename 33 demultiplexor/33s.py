import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 44444))
sock.listen(10)
conn, addr = sock.accept()
data = conn.recv(1024)
print(data.decode())
msg = "Hi"
conn.send(msg.encode())
data = conn.recv(1024)
print(data.decode())
conn.send(msg.encode())
conn.close()

sock1 = socket.socket()
sock1.bind(('localhost', 11111))
sock1.listen(10)
conn1, addr1 = sock1.accept()
data1 = conn1.recv(1024)
print(data1.decode())
conn1.close()
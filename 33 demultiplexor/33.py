import socket
import sys
import threading
import time

class MyThread(threading.Thread):
     def __init__(self, sock1, sock2, msg):
         threading.Thread.__init__(self)
         self.source = sock1
         self.destination = sock2
         self.message = msg

     def run(self):
         forward(self.source, self.destination, self.message)

def server():
    dock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dock_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    dock_socket.bind(('localhost', 11223))
    dock_socket.listen(10)
    while True:
        client_socket = dock_socket.accept()[0]
        client_socket.settimeout(2.0)
        try:
            string = client_socket.recv(1024)
        except socket.timeout:
            string = "-"
            port = 55555
        else:
            port = parse(string.decode())

        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.connect(('', port))
        server_socket.sendall(string)
        tc = MyThread(client_socket, server_socket, string)
        ts = MyThread(server_socket, client_socket, "-")
        tc.start()
        ts.start()

def forward(source, destination, message):
    if (message != "-"):
        destination.sendall(message)
    string = ' '
    while string:
        try:
            string = source.recv(1024)
            if string:
                destination.sendall(string)
            else:
                try:
                    source.shutdown(socket.SHUT_RD)
                    destination.shutdown(socket.SHUT_WR)
                except BaseException:
                    source.close()
                    destination.close()
        except BaseException:
            break

#Проверка наличия ключевого слова
def parse(message):
    for msg in key_words:
        if msg in message:
            return protocols[msg]
    return 44444#Отправляем туда все остальное

key_words = []
key_words.append('HTTP')
key_words.append('USER')
key_words.append('www')

#Таблица соответсвия ключевое слово - порт
protocols = {}
protocols['HTTP'] = 11111
protocols['USER'] = 22222
protocols['www'] = 33333

while True:
    server()
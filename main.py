import socket
import threading
import os
from queue import Queue
import gui


sock = socket.socket()
ip = input('ip:')
sock.connect((ip, 21414))
nickname = input('nickname:')
sock.send(nickname.encode('utf-8'))
msgs = Queue()


def receive():
    while sock:
        data = sock.recv(1024)
        if data:
            msgs.put(data.decode('utf-8'))


def send(text):
    sock.send(text.encode('utf-8'))
    print(f"sent {text}")


rec = threading.Thread(target=receive)
rec.start()

chat = gui.Chat(msgs, send, name="Lanity's irc", size=(800, 600))
chat.run()

sock.close()

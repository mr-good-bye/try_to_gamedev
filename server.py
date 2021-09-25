import socket
import threading

sock = socket.socket()
sock.bind(('192.168.0.103', 21414))
sock.listen()


clients = []
threads = []


def handler(conn, addr, nickname):
    send(conn, addr[0] + ' connected as ' + nickname)
    while 'fisting is 300 bucks':
        try:
            data = conn.recv(1024).decode('utf-8')
        except ConnectionResetError:
            data = 'exit'
        if 'exit' in data:
            break
        send(conn, nickname + ': ' + data)
    conn.close()
    send(conn, nickname + ' Disconnected!')


def send(conn, data):
    for cl in clients:
        try:
            cl.send(data.encode('utf-8'))
        except Exception:
            clients.remove(cl)
    print(data)



while True:
    conn, addr = sock.accept()
    clients.append(conn)
    nickname = conn.recv(1024).decode('utf-8')
    print(addr[0] + ' connected as ' + str(nickname))
    handle = threading.Thread(target=handler, args=(conn, addr, nickname))
    handle.start()
    threads.append(handle)


for i in threads:
    i.join()

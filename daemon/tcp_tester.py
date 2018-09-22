import socket

from daemon.config import Config
config = Config()
while True:
    sock = socket.socket()
    sock.connect((config.tcp_host, config.tcp_port))
    command = input('>')
    cmdstr = command.encode('utf-8')
    prefix = str(len(cmdstr)).zfill(5)
    bts = bytes(prefix.encode()+cmdstr)
    print(bts)
    sock.send(bts)
    print('sent')
    length = sock.recv(5)
    print('response:', sock.recv(int(length)).decode('utf-8'))
    sock.close()
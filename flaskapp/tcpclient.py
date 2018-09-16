import socket


def send_request(host, port, command, need_answer = False):
    sock = socket.socket()
    sock.connect((host, port))
    if need_answer:
        command = '1 '+command
    else:
        command = '0 '+command
    cmdstr = command.encode('utf-8')
    prefix = str(len(cmdstr)).zfill(5)
    bts = bytes(prefix.encode()+cmdstr)
    sock.send(bts)
    length = sock.recv(5)
    rt = sock.recv(int(length)).decode('utf-8')
    sock.close()
    return rt
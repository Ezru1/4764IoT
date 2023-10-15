import socket

addr = ('192.168.1.160',9999)
s = socket.socket()
s.bind(addr)
s.listen(5)
s.setblocking(True)
while True:
    try:
        (conn,address) = s.accept()
    except OSError:
        print("Nothing")
    else:
        rec = conn.recv(4096)
        
        rec = rec.split(b'\r\n\r\n')
        print(rec)
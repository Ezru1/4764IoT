import socket
import time
pos = 1
while True:
    try:
        client = socket.socket()
        client.connect(('6.tcp.ngrok.io',14961))
        s = str(pos);pos += 1
        client.send(s.encode('utf-8'))
        client.close()
        time.sleep(10)
        print(s)
    except:
        print("Connection refused by the server(%s).."%str(pos))
        time.sleep(3)
        continue
    
    
    
    
import socket
import json
import time

data = "test123"

test = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8080))
while test:
    s.send(json.dumps(data))
    result = json.loads(s.recv(1024))
    print result
    test -= 1
    time.sleep(1)

s.close()

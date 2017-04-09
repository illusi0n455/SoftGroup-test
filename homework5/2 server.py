import socket
import json
import threading


def client(conn, addr, clname):
    while 1:
        try:
            reply = conn.recv(4048)
        except:
            break
        if not reply:
            break
        # reply = json.loads(reply)
        print(reply)
        conn.sendall(reply)
    names.pop(clname)

name = "Server"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 80
limit = 10

s.bind((host, port))
s.listen(limit)
names = []
while True:
    conn, addr = s.accept()
    clname = json.loads(conn.recv(4048).decode())["name"]
    if clname not in names:
        names.append(clname)
        j = json.dumps({"name": name, "message": "Welcome " + clname})
        conn.sendall(str.encode(j))
        my_thread = threading.Thread(target=client, args=(conn, addr, clname))
        my_thread.start()
    else:
        j = json.dumps({"name": name, "message": "Name is already taken"})
        conn.sendall(str.encode(j))

import socket
import json
import threading


clients = {}


def sendtoeveryone(msg, name="Server", exceptfor=None):
    if exceptfor:
        for k in clients.keys():
            if k != exceptfor:
                msg = json.dumps({"name": name, "message": msg})
                sendjson(k, msg)
    else:
        for k in clients.keys():
            msg = json.dumps({"name": name, "message": msg})
            sendjson(k, msg)


def getjson(conn):
    msg = conn.recv(50)
    while b"<end>" not in msg:
        msg += conn.recv(50)
    msg = json.loads(msg.decode().split("<end>")[0])
    return msg


def sendjson(conn, msg):
    msg = msg + "<end>"
    conn.sendall(str.encode(msg))


def client(conn):
    clname = getjson(conn)
    print(clname)
    clname = clname["name"]
    if clname not in clients.values():
        clients[conn] = clname
        j = json.dumps({"name": name, "message": "Welcome " + clname})
        sendjson(conn, j)
        sendtoeveryone(clname + " connected", exceptfor=conn)
        while 1:
            try:
                reply = getjson(conn)
                print(reply)
            except:
                break
            if not reply:
                break
            msg = reply["message"]
            if msg.startswith("user:"):
                to, msg = msg.split(" ", 1)
                to = to[4:]
                for k, v in clients.items():
                    if to == v:
                        j = json.dumps({"name": reply["name"], "message": msg})
                        sendjson(k, j)
                        break
            sendtoeveryone(msg, name=reply["name"], exceptfor=conn)
    else:
        j = json.dumps({"name": name, "message": "Name is already taken"})
        sendjson(conn, j)
        conn.close()
        return
    clients.pop(conn)
    sendtoeveryone(clname + " left chatroom")
    print(clname + " left chatroom")

name = "Server"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1024
limit = 10

s.bind((host, port))
s.listen(limit)
while True:
    conn, addr = s.accept()
    my_thread = threading.Thread(target=client, args=(conn,))
    my_thread.start()

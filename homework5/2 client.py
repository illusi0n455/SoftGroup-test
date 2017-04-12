import socket
import json
import threading


def getjson(conn):
    """Я міг винести цю функцію в окремий файл але не став"""
    msg = conn.recv(50)
    while b"<end>" not in msg:
        msg += conn.recv(50)
    msg = json.loads(msg.decode().split("<end>")[0])
    return msg


def sendjson(conn, msg):
    """Я міг винести цю функцію в окремий файл але не став"""
    msg = msg + "<end>"
    conn.sendall(str.encode(msg))


def reader(s):
    while 1:
        try:
            reply = getjson(s)
            print("{0}: {1}".format(reply["name"], reply["message"]))
        except:
            r = input('Disconnected from chat room. Press <enter> to exit.')
            break


def sender(s):
    while 1:
        message = input()
        if message == "<exit>":
            break
        j = json.dumps({"name": name, "message": message})
        try:
            sendjson(s, j)
        except:
            break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 1024
s.connect((host, port))
name = input("Enter your name: ").strip()

if name:
    j = json.dumps({"name": name, "message": ""})
    sendjson(s, j)
    reply = getjson(s)["message"]
    print(reply)
    if "Welcome" in reply:
        r_thread = threading.Thread(target=reader, args=(s,))
        s_thread = threading.Thread(target=sender, args=(s,))
        r_thread.start()
        s_thread.start()
        r_thread.join()
        s_thread.join()
s.close()
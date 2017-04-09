import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '127.0.0.1'
port = 80
s.connect((host, port))

name = input("Enter your name: ").strip()
if name:
    j = json.dumps({"name": name, "message": ""})
    s.sendall(str.encode(j))
    reply = s.recv(4048)
    reply = json.loads(reply.decode())
    print(reply["message"])
    if "Welcome" in reply["message"]:
        while 1:
            message = input("Enter message: ")
            if message == "<exit>":
                break
            j = json.dumps({"name": name, "message": message})
            try:
                s.sendall(str.encode(j))
            except:
                input('Disconnected from chatroom. Press <enter> to exit.')
                break

            reply = s.recv(4048)
            print(reply)

s.close()
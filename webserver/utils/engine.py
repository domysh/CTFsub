import socket, conf, json, secrets


def send_request(data):
    data["id"] = secrets.token_hex(30)
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.connect((conf.ENGINE_ADDR,conf.ENGINE_PORT))
    sk.sendall(json.dumps(data).encode())
    sk.close()
    return data["id"]


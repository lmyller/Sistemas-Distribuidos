from rpc import sub
import json

with open('config.json', 'r') as file:
    data = json.load(file)

server = sub.Server(data['ip'], data['port'], data['multiprocess'], "./rpc/server.crt", "./rpc/server.key")

server.start()
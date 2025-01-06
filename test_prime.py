from rpc import server
import json

with open('config.json', 'r') as file:
    data = json.load(file)

server = server.Server(data['ip'], data['port'], data['multiprocess'], data['cache'])

server.start()
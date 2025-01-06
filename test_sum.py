from rpc import sum
import json

with open('config.json', 'r') as file:
    data = json.load(file)

server = sum.Server(data['ip'], data['port'], data['multiprocess'])

server.start()
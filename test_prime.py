from rpc import prime
import json

with open('config.json', 'r') as file:
    data = json.load(file)

server = prime.Server(data['ip'], data['port'], data['multiprocess'], data['cache'], "./rpc/server.crt", "./rpc/server.key") 

server.start()
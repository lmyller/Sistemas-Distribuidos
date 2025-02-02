from rpc import client
import json

with open('config.json', 'r') as file:
    data = json.load(file)

c = client.Client('127.0.0.1', 12000, "./rpc/server.crt")

print(c.valida_cpf('11108589650'))

#for i in range(100):
#    print(c.sum(random.randint(1, 99), random.randint(1,99)))

#client.close()
from rpc import client
import json

with open('config.json', 'r') as file:
    data = json.load(file)

c = client.Client(data['ip'], data['port'])

print(c.sum(list(range(999))))
while True:
    print(c.wait_n_seconds(3))

#for i in range(100):
#    print(c.sum(random.randint(1, 99), random.randint(1,99)))

#client.close()
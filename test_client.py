from rpc import client
import json

with open('config.json', 'r') as file:
    data = json.load(file)

c = client.Client('127.0.0.1', 12000)

c.check_primes_parallel(list(range(10000)), 4)

#for i in range(100):
#    print(c.sum(random.randint(1, 99), random.randint(1,99)))

#client.close()
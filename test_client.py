from rpc import client
import random

c = client.Client('127.0.0.1', 16000)

print(c.sum(list(range(999))))
while True:
    print(c.wait_n_seconds(3))

#for i in range(100):
#    print(c.sum(random.randint(1, 99), random.randint(1,99)))

#client.close()
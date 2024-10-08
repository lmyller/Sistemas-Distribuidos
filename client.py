from rpc import client

client = client.Client('127.0.0.1', 16000)
client.sum(10, 20) # 30
#client.div(10, 2) # 5
#client.mul(5, 5) # 25
#client.sub(10, 15) # -5
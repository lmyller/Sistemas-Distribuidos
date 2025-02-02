import socket
import threading
from random import randint

def handle_client(sock, data, address):
    sum = ['127.0.0.1:3020', '127.0.0.1:3025']
    multi = ['127.0.0.1:3022', '127.0.0.1:3024']
    prime = ['127.0.0.1:3027', '127.0.0.1:3026']
    sub = ['127.0.0.1:3021', '127.0.0.1:3028']
    div = ['127.0.0.1:3025', '127.0.0.1:3029']
    cpf = ['127.0.0.1:3030']

    print(f"Recebido {data} de {address}")
    data = data.decode()
    
    if data == 'sum':
        send(sock, address, sum)

    elif data == 'mul':
        send(sock, address, multi)
    
    elif data == 'prime':
        send(sock, address, prime)

    elif data == 'sub':
        send(sock, address, sub)

    elif data == 'div':
        send(sock, address, div)

    elif data == 'cpf':
        send(sock, address, cpf)

def udp_server(host='localhost', port=1200):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    print(f"Servidor UDP está escutando em {host}:{port}")
    
    while True:
        data, address = sock.recvfrom(4096)
        client_thread = threading.Thread(target=handle_client, args=(sock, data, address))
        client_thread.start()

def send(sock, address, list_ops):
    response = list_ops[randint(0, len(list_ops) - 1)]
    sock.sendto(response.encode(), address)
    print(f'send: {response}')

if __name__ == "__main__":
    udp_server()

import socket

class Client:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((addr, port))

    def sum(self, n1, n2):
        calc = f'{n1}+{n2}'
        self.send(calc)
    
    def div(self, n1, n2):
        calc = f'{n1}/{n2}'

    def mul(self, n1, n2):
        calc = f'{n1}*{n2}'

    def sub(self, n1, n2):
        calc = f'{n1}-{n2}'

    def send(self, calc):
        self.client_socket.send(calc.encode('utf-8'))
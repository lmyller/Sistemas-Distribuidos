from multiprocessing import Process, Queue, Pool
from threading import Thread
import time
import socket
import sys
import os
import pickle

class Server:
    def __init__(self, addr, port, multiprocess):
        self.addr = addr
        self.port = port
        self.multiprocess = multiprocess.lower()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.addr, self.port))
        server_socket.listen(5)

        print("Servidor pronto para receber")

        while True:
            connection_socket, address = server_socket.accept()
            print(f"Cliente conectado: {address}")
            self.load_cache()

            if self.multiprocess == "process":
                client_process = Process(target=self.connection_client, args=(connection_socket, address))
                client_process.start()
            
            elif self.multiprocess == "thread":
                client_thread = Thread(target=self.connection_client, args=(connection_socket, address))
                client_thread.start()

    def connection_client(self, connection_socket, address):
        while True:
            try:
                message = connection_socket.recv(10000).decode()
                
                if not message: 
                    print(f"Cliente {address} desconectado.")
                    break

                try:
                    result = self.calculate_div(message.split('/'))
                except ZeroDivisionError:
                    return "Erro: Divisão por zero"

                if result is not None:
                    connection_socket.send(str(result).encode())
                else:
                    print("Operação inválida")

            except ConnectionResetError:
                break

        connection_socket.close()

    def calculate_div(self, numbers):
        return float(numbers[0].strip()) / float(numbers[1].strip())


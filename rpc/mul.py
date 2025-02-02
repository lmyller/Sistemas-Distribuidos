from multiprocessing import Process
from threading import Thread
from utils.generate_log import log_request
import time
import socket
import ssl

class Server:
    def __init__(self, addr, port, multiprocess, certfile, keyfile):
        self.addr = addr
        self.port = port
        self.cache = {}
        self.multiprocess = multiprocess.lower()
        self.certfile = certfile
        self.keyfile = keyfile

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.addr, self.port))
        server_socket.listen(5)

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)

        print("Server ready to receive connections")

        while True:
            connection_socket, address = server_socket.accept()
            secure_socket = context.wrap_socket(connection_socket, server_side=True)
            print(f"Secure connection established with: {address}")

            if self.multiprocess == "process":
                client_process = Process(target=self.connection_client, args=(secure_socket, address))
                client_process.start()
            elif self.multiprocess == "thread":
                client_thread = Thread(target=self.connection_client, args=(secure_socket, address))
                client_thread.start()

    def connection_client(self, connection_socket, address):
        while True:
            try:
                message = connection_socket.recv(10000).decode()
                
                if not message: 
                    print(f"Cliente {address} desconectado.")
                    break
                
                start_time = time.time()

                if message in self.cache:
                    result = self.cache[message]

                else:
                    result = self.calculate_mul(message.split('*'))
                    self.cache[message] = result

                end_time = time.time()
                response_time = end_time - start_time

                log_request(address[0], 'Multiplicação', response_time)

                if result is not None:
                    connection_socket.send(str(result).encode())
                else:
                    print("Operação inválida")

            except ConnectionResetError:
                break

        connection_socket.close()

    def calculate_mul(self, numbers):
        return float(numbers[0].strip()) * float(numbers[1].strip())
        

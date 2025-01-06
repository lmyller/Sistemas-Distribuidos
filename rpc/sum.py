from multiprocessing import Process
from threading import Thread
import socket

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

                result = self.calculate_sum(message.split('+'))

                if result is not None:
                    if isinstance(result, list):
                        self.send_list(connection_socket, result)
                    else:
                        connection_socket.send(str(result).encode())
                else:
                    print("Operação inválida")

            except ConnectionResetError:
                break

        connection_socket.close()

    def send_list(self, connection_socket, list_result):
        while list_result:
            chunk = list_result[:1000]
            connection_socket.send(','.join(map(str, chunk)).encode())
            list_result = list_result[1000:]

    def calculate_sum(self, numbers):
        return sum(float(number.strip()) for number in numbers)
    
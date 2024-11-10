from multiprocessing import Process
import socket
from threading import Thread
import time

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

                result = self.calculate(message)

                if result is not None: 
                    connection_socket.send(str(result).encode())
                else:
                    print("Operação inválida")

            except ConnectionResetError:
                break

        connection_socket.close()

    def calculate(self, message):
        result = None

        if 'w' in message:
            time.sleep(int(message[1]))
            result = message[1]
        elif '+' in message:
            result = self.calculate_sum(message.split('+'))
        elif '-' in message:
            result = self.calculate_sub(message.split('-'))
        elif '*' in message:
            result = self.calculate_mul(message.split('*'))
        elif '/' in message:
            try:
                result = self.calculate_div(message.split('/'))
            except ZeroDivisionError:
                result = "Erro: Divisão por zero"

        return result

    def calculate_sum(self, numbers):
        return sum(float(number.strip()) for number in numbers)
    
    def calculate_sub(self, numbers):
        return float(numbers[0].strip()) - float(numbers[1].strip())
    
    def calculate_mul(self, numbers):
        return float(numbers[0].strip()) * float(numbers[1].strip())
        
    def calculate_div(self, numbers):
        return float(numbers[0].strip()) / float(numbers[1].strip())

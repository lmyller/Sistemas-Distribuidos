from multiprocessing import Process, Pool
from threading import Thread
import socket
import sys
import os
import pickle

class Server:
    def __init__(self, addr, port, multiprocess, size_cache_prime):
        self.addr = addr
        self.port = port
        self.size_cache_prime = size_cache_prime
        self.multiprocess = multiprocess.lower()
        self.cache_prime = {}
        self.cache_file = 'cache_prime.pkl'
        self.load_cache()

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

                result = self.calculate(message)

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

    def calculate(self, message):
        if 'p' in message:
            n_process = int(message[0])
            return self.check_prime_parallel(message.split('p')[2:], n_process)
        elif 'c' in message:
            return self.check_prime(message.split('c'))
       
        return None

    def check_prime(self, numbers):
        return [self.prime_number(int(num)) for num in numbers]
    
    def check_prime_parallel(self, numbers, n_process):
        with Pool(processes = n_process) as pool:
            results = pool.map(self.prime_number, numbers)
        return results

    def prime_number(self, number):
        number = int(number)

        if number in self.cache_prime:
            return self.cache_prime[number]
        
        if number < 2:
            self.save_cache(number, False)
            return False
        
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                self.save_cache(number, False)
                return False
        
        self.save_cache(number, True)
        return True

    def save_cache(self, number, is_Prime):
        self.cache_prime[number] = is_Prime

        self.save_cache_to_disk()

        if sys.getsizeof(self.cache_prime) > self.size_cache_prime:
            self.remove_oldest_entries()

    def save_cache_to_disk(self):
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache_prime, f)

    def load_cache(self):
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                try:
                    self.cache_prime = pickle.load(f)
                except (pickle.PickleError, EOFError):
                    pass

    def remove_oldest_entries(self):
        while sys.getsizeof(self.cache_prime) > self.size_cache_prime and self.cache_prime:
            first = next(iter(self.cache_prime))
            del self.cache_prime[first]
        self.save_cache_to_disk()

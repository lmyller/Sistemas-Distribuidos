from multiprocessing import Process
from threading import Thread
from utils.generate_log import log_request
import socket
import time
import ssl

class Server:
    def __init__(self, addr, port, multiprocess, certfile, keyfile):
        self.addr = addr
        self.port = port
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
                result = self.valida_cpf(message)
                end_time = time.time()
                response_time = end_time - start_time

                log_request(address[0], 'Valida CPF', response_time)

                if result is not None:
                    connection_socket.send(str(result).encode())
                else:
                    print("Operação inválida")

            except ConnectionResetError:
                break

        connection_socket.close()

    def valida_cpf(self, cpf):
        cpf = ''.join(filter(str.isdigit, cpf))

        if len(cpf) != 11:
            return False

        if cpf == cpf[0] * 11:
            return False

        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        primeiro_digito = 11 - (soma % 11)
        if primeiro_digito >= 10:
            primeiro_digito = 0

        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        segundo_digito = 11 - (soma % 11)
        if segundo_digito >= 10:
            segundo_digito = 0

        return cpf[-2:] == f"{primeiro_digito}{segundo_digito}"



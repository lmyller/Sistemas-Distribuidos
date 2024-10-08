import socket

class Server:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.addr, self.port))
        server_socket.listen(1)

        print("Servidor pronto para receber")

        while True:
            connection_socket, address = server_socket.accept()
            message = connection_socket.recv(2048).decode('utf-8')

            if (message.find('+') != -1):
                print('aqui')

            print("{} ==> {}".format(address, message))
            #connection_socket.send(modifiedMessage.encode('utf-8'))
            connection_socket.close()
import socket

class Client:
    def __init__(self, addr, port):
        self.addr = addr
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((addr, port))

    def sum(self, *args):
        if (isinstance(args[0], list)):
            return self.sum_list(args[0])
        
        if(len(args) <= 2):
            calc = f'{args[0]}+{args[1]}'
        else:
            calc = list(args)
            
        calc = self.create_send_string(calc)

        #self.send(calc)
        #return self.client_socket.recv(2048).decode()
    
    def div(self, n1, n2):
        calc = f'{n1}/{n2}'
        self.send(calc)
        return self.client_socket.recv(1024).decode()

    def mul(self, n1, n2):
        calc = f'{n1}*{n2}'
        self.send(calc)
        return self.client_socket.recv(1024).decode()

    def sub(self, n1, n2):
        calc = f'{n1}-{n2}'
        self.send(calc)
        return self.client_socket.recv(1024).decode()

    def send(self, command):
        self.client_socket.send(command.encode())

    def close(self):
        self.client_socket.close()

    def create_send_string(self, list_numbers):
        return '+'.join(map(str,list_numbers))
    
    def sum_list(self, list_numbers):
        sum = 0

        while True:
            calc = None

            if len(list_numbers) > 1000:
                numbers = list_numbers[:1000]
                calc = self.create_send_string(numbers)
                list_numbers = list_numbers[1000:]
                self.send(calc)
                sum += float(self.client_socket.recv(10000).decode())
                
            else:
                numbers = list_numbers[:1000]
                calc = self.create_send_string(numbers)
                self.send(calc)
                sum += float(self.client_socket.recv(10000).decode())

                return sum
            
    def wait_n_seconds(self, n):
        wait = f'w{n}'
        self.send(wait)
        return self.client_socket.recv(100).decode()

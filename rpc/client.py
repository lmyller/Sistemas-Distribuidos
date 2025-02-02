from dns.dns_client import udp_client
import socket
import ssl

class Client:
    def __init__(self, addr, port, certfile):
        self.addr = addr
        self.port = port
        self.certfile = certfile
        self.context = ssl.create_default_context(cafile=self.certfile)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.client_socket = None   

    def connect(self, op):
        if op == 'sum':
            response_dns = udp_client("sum").split(':')
        elif op == 'mul':
            response_dns = udp_client("mul").split(':')
        elif op == 'prime':
            response_dns = udp_client("prime").split(':')
        elif op == 'div':
            response_dns = udp_client("div").split(':')
        elif op == 'sub':
            response_dns = udp_client("sub").split(':')
        elif op == 'cpf':
            response_dns = udp_client("cpf").split(':')
        
        raw_socket = socket.create_connection((response_dns[0], int(response_dns[1])))
        self.client_socket = self.context.wrap_socket(raw_socket, server_hostname=response_dns[0])

    def sum(self, *args):
        self.connect('sum')

        if isinstance(args[0], list):
            return self.sum_list(args[0])
        
        calc = self.create_send_string(args, '+')
        self.send(calc)
        return self.client_socket.recv(2048).decode()
    
    def div(self, n1, n2):
        self.connect('div')
        return self._calculate(f'{n1}/{n2}')

    def mul(self, n1, n2):
        self.connect('mul')
        return self._calculate(f'{n1}*{n2}')

    def sub(self, n1, n2):
        self.connect('sub')
        return self._calculate(f'{n1}-{n2}')

    def valida_cpf(self, cpf):
        self.connect('cpf')
        return self._calculate(cpf)

    def _calculate(self, calc):
        self.send(calc)
        return self.client_socket.recv(1024).decode()

    def send(self, command):
        self.client_socket.send(command.encode())

    def close(self):
        if self.client_socket:
            self.client_socket.close()

    def create_send_string(self, list_numbers, char):
        return char.join(map(str, list_numbers))
    
    def sum_list(self, list_numbers):
        total_sum = 0
        while list_numbers:
            chunk = list_numbers[:1000]
            list_numbers = list_numbers[1000:]
            calc = self.create_send_string(chunk, '+')
            self.send(calc)
            total_sum += float(self.client_socket.recv(10000).decode())
        return total_sum
    
    def wait_n_seconds(self, n):
        wait = f'w{n}'
        self.send(wait)
        return self.client_socket.recv(100).decode()
    
    def check_primes(self, numbers):
        self.connect('prime')
        return self.send_list(numbers, 'c', -1)
    
    def check_primes_parallel(self, numbers, n_process):
        self.connect('prime')
        return self.send_list(numbers, 'p', n_process)

    def send_list(self, list_numbers, char, n_process):
        list_result = []
        while list_numbers:
            if n_process != -1:
                list_numbers.insert(0, f'{n_process}p')
            chunk = list_numbers[:1000]
            list_numbers = list_numbers[1000:]
            self.send(self.create_send_string(chunk, char))
            list_result.extend(self.client_socket.recv(10000).decode().split(','))
        return list_result

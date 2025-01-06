import socket

def udp_client(message, host='localhost', port=1200):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)
    
    try:
        print(f"Enviando {message} para {host}:{port}")
        sent = sock.sendto(message.encode(), server_address)
        
        data, server = sock.recvfrom(4096)
        print(f"Recebido {data} do servidor")
        return data.decode()

    finally:
        print("Fechando o socket")
        sock.close()

if __name__ == "__main__":
    ip = udp_client('soma').split(':')
    print(f"IP: {ip[0]}, Port: {ip[1]}")

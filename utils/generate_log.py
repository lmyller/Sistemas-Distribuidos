import time    

def log_request(client_ip, operation_name, response_time):
    try:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
        log_entry = f"{timestamp}, {client_ip}, {operation_name}, {response_time}\n"
        with open('./log/server_log.log', 'a') as log_file:
            log_file.write(log_entry)
        print("Log registrado com sucesso.")
    except Exception as e:
        print(f"Erro ao registrar log: {e}")

# ts2: .edu

'''
rutgers.edu 128.1.1.4
njit.edu 10.5.6.7
'''

import socket
import sys

def load_database(filename):
    database = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2: # make sure format: domain ip
                database[parts[0].lower()] = parts[1] # parts[0]: domain, parts[1]: ip address
    return database

def handle_query(query, ts2_db):
    parts = query.split() # 0 DomainName indentification flags
    domain = parts[1].lower() # case insensitive
    identification = parts[2]
    flag = parts[3].lower()

    if domain in ts2_db:
        return f"1 {domain} {ts2_db[domain]} {identification} aa"
    else:
        return f"1 {domain} 0.0.0.0 {identification} nx"


def main():
    # python3 ts2.py 45000
    if len(sys.argv) != 2:
        print("Usage: python3 ts2.py <rudns_port>")
        return
    
    port = int(sys.argv[1]) # rudns_port
    ts2_db = load_database("ts2database.txt")

    # for domain, ip in ts2_db.items():
    #     print(f"Domain: {domain}, IP: {ip}")

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(5)
    print(f"TS2 Server listening on port {port}...")

    with open('ts2responses.txt', 'w') as resolved_log:
        while True:
            clientSocket, addr = serverSocket.accept()
            query = clientSocket.recv(1024).decode()
            response = handle_query(query, ts2_db)
            clientSocket.send(response.encode())
            resolved_log.write(f"{response}\n")
            resolved_log.flush()            
            clientSocket.close()

if __name__ == "__main__":
    main()

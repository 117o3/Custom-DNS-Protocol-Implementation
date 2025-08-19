# root server: ts1, ts2, others

''' 
com java.cs.rutgers.edu
edu cheese.cs.rutgers.edu
github.io 25.6.7.1
x.ai 45.67.89.103
bit.ly 1.2.3.4
'''

import socket
import sys

def load_database(filename):
    database = {}
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) == 2:
                database[parts[0].lower()] = parts[1]
    return database

def send_query_to_ts(ts_hostname, port, query):
    ts_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ts_socket.connect((ts_hostname, port))
    ts_socket.send(query.encode())
    response = ts_socket.recv(1024).decode()
    ts_socket.close()
    return response

# 0 domainName idendification flag
def handle_query(query, rs_db, port):
    parts = query.split()
    domain = parts[1].lower()
    identification = parts[2]
    flag = parts[3].lower()
    tld = domain[-3:] # com, edu, etc

    # check if in TS (redirect), then RS
    if tld in rs_db:  # com, edu, etc
        if flag == "it":  # iterative
            return f"1 {domain} {rs_db[tld]} {identification} ns"
        elif flag == "rd":  # recursive
            ts_response = send_query_to_ts(rs_db[tld], port, query)
            ts_response_parts = ts_response.split()
            if ts_response_parts[4] == "aa":  # if authoritative, change to ra
                return f"1 {domain} {ts_response_parts[2]} {identification} ra"
            else:
                return ts_response
    else:
        # domain is not under .com or .edu, resolve using RS database
        if domain in rs_db:
            return f"1 {domain} {rs_db[domain]} {identification} aa"
        else:
            return f"1 {domain} 0.0.0.0 {identification} nx"


def main():
    # python3 rs.py 45000
    if len(sys.argv) != 2:
        print("Usage: python3 rs.py <rudns_port>")
        return
    
    port = int(sys.argv[1]) # rudns_port
    rs_db = load_database("rsdatabase.txt")

    # for domain, ip in rs_db.items():
    #     print(f"Domain: {domain}, IP: {ip}")
            
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(5)
    print(f"Root Server listening on port {port}...")

    # 2. recieved from client.py
    with open("rsresponses.txt", "w") as rs_file:
        while True:
            clientSocket, addr = serverSocket.accept()
            query = clientSocket.recv(1024).decode()
            response = handle_query(query, rs_db, port)
            clientSocket.send(response.encode())
            rs_file.write(f"{response}\n")
            rs_file.flush()
            clientSocket.close()

if __name__ == "__main__":
    main()

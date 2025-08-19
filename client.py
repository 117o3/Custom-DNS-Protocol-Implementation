# client

'''
www.google.com rd
princeton.edu it
njit.edu it
x.ai it
watch.tv it
'''

import socket
import sys
import pprint

# 1. sends to rs.py
def send_query(hostname, port, query):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((hostname, port))
    clientSocket.send(query.encode())
    response = clientSocket.recv(1024).decode()
    clientSocket.close()
    return response

def main():
    # python3 client.py cheese.cs.rutgers.edu 45000
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <rs_hostname> <rudns_port>")
        return
    
    rs_host = sys.argv[1] # rs_hostname (cheese.cs.rutgers.edu)
    port = int(sys.argv[2]) # rudns_port

    #with open('testcases.txt', 'r') as file: # extra test cases
    with open('hostnames.txt', 'r') as file:
        queries = [line.strip().split() for line in file]
        queries = [[parts[0].lower(), parts[1].lower()] for parts in queries] # case insensitive
        # pprint.pprint(queries)

    with open('resolved.txt', 'w') as resolved_file:
        identification = 1
        for i, query in enumerate(queries):
            domain, flag = query
            query_message = f"0 {domain} {identification} {flag}" # put into format: 0 domainName id flag
            response = send_query(rs_host, port, query_message)
            resolved_file.write(f"{response}\n")
            print(f"Response for {domain}: {response}")

            # iterative
            if flag == "it":
                response_parts = response.split()
                if response_parts[4] == "ns":
                    # if ts_hostname = "ts1"
                        # ts_hosname = ts1
                    # else if ts_hostname = "ts2"
                        # ts_hostname = ts2
                    ts_hostname = response_parts[2]
                    identification += 1
                    ts_query_message = f"0 {domain} {identification} {flag}"
                    # print("ts_query_message: " + ts_query_message)
                    ts_response = send_query(ts_hostname, port, ts_query_message)
                    resolved_file.write(f"{ts_response}\n")
                    print(f"Response from TS for {domain}: {ts_response}")
            identification += 1


if __name__ == "__main__":
    main()

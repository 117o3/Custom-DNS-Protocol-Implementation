# Custom DNS Protocol Implementation

A complete distributed DNS (Domain Name System) implementation featuring recursive and iterative query resolution across multiple servers in a networked environment.

## Table of Contents
- [Overview](#overview)
- [Key Achievements](#key-achievements)
- [Technologies Used](#technologies-used)
- [System Architecture](#system-architecture)
- [Protocol Implementation](#protocol-implementation)
- [Query Types](#query-types)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Distributed Deployment](#distributed-deployment)
- [Usage](#usage)
- [Requirements](#requirements)

## Overview

This project implements a custom DNS protocol system that simulates real-world domain name resolution. The system consists of multiple distributed servers that work together to resolve domain names to IP addresses using both **recursive** and **iterative** query methods.

The implementation demonstrates a complete client-server architecture with:
- **Root Server (RS)** - Central authority that directs queries to appropriate top-level domain servers
- **Top-Level Domain Servers (TS1, TS2)** - Specialized servers handling .com and .edu domains respectively
- **Client** - Initiates domain resolution requests with configurable query types

## Key Achievements

- **Built distributed DNS system** with 4 interconnected servers across multiple machines
- **Implemented both recursive and iterative query resolution** protocols
- **Achieved 100% query resolution** for domains in system database
- **Developed complete networking protocol** using TCP socket programming
- **Deployed across distributed environment** using multiple iLab machines
- **Created flexible, non-hardcoded system** adaptable to different machine configurations
- **Implemented comprehensive logging system** tracking all server responses

## Technologies Used

- **Language**: Python
- **Networking**: TCP Socket Programming, Multi-threaded Server Architecture
- **Protocols**: Custom DNS Protocol Implementation
- **Deployment**: Distributed Systems across Multiple Linux Machines
- **Tools**: SCP for file transfer, Vim for remote editing
- **Skills**: Network programming, Distributed systems, Client-server architecture, Protocol design

## System Architecture

```
                           Client
                             |
                    (Query Resolution Request)
                             |
                      Root Server (RS)
                        /         \
              (Recursive)           (Iterative - Referral)
                   /                       \
                  |                    Client → TS1/TS2
          Direct Resolution                     |
              |                         (Direct Query)
          TS1 (.com) ←------------ Response ←--------→ TS2 (.edu)
```

## Protocol Implementation

### 1. Root Server (rs.py)
- **Primary Function**: Central DNS authority and query router
- **Responsibilities**:
  - Routes .com queries to TS1, .edu queries to TS2
  - Handles recursive resolution by forwarding queries to appropriate TS
  - Maintains database of top-level domains and direct domain mappings
  - Processes iterative queries by returning referrals to clients
- **Database**: Maps TLDs to their respective servers and direct domain resolutions

### 2. Top-Level Domain Server 1 (ts1.py)
- **Domain Authority**: .com domains
- **Function**: Authoritative server for commercial domain resolution
- **Database**: Maps .com domains to their IP addresses
- **Response Types**: Returns authoritative answers (aa) or domain not found (nx)

### 3. Top-Level Domain Server 2 (ts2.py)  
- **Domain Authority**: .edu domains
- **Function**: Authoritative server for educational domain resolution
- **Database**: Maps .edu domains to their IP addresses
- **Response Types**: Returns authoritative answers (aa) or domain not found (nx)

### 4. Client (client.py)
- **Function**: Initiates domain name resolution requests
- **Features**:
  - Reads domain queries from input file
  - Supports both recursive (rd) and iterative (it) query flags
  - Handles multi-step iterative resolution process
  - Logs all responses for analysis
- **Input**: Processes batch queries from hostnames.txt file

## Query Types

### Recursive Queries (rd flag)
```
Client → RS → TS (if needed) → RS → Client
```
1. Client sends query to Root Server
2. RS handles complete resolution process
3. RS forwards query to appropriate TS if needed
4. RS returns final resolved IP to client
5. **Single response** to client with complete resolution

### Iterative Queries (it flag)
```
Client → RS → Client → TS → Client
```
1. Client sends query to Root Server
2. RS returns referral to appropriate TS
3. **Client directly contacts TS** for final resolution
4. TS returns authoritative answer to client
5. **Multiple round-trips** managed by client

## Project Structure

```
├── client.py                 # DNS client implementation
├── rs.py                     # Root server implementation  
├── ts1.py                    # Top-level server for .com domains
├── ts2.py                    # Top-level server for .edu domains
├── rsdatabase.txt            # Root server domain mappings
├── ts1database.txt           # .com domain database
├── ts2database.txt           # .edu domain database
├── hostnames.txt             # Client query input file
├── resolved.txt              # Client resolution log
├── rsresponses.txt           # Root server response log
├── ts1responses.txt          # TS1 server response log
└── ts2responses.txt          # TS2 server response log
```

## Technical Details

### Network Protocol Design
**Query Message Format:**
```
0 domain_name identification_number query_flag
```

**Response Message Format:**
```
1 domain_name ip_address identification_number response_flag
```

### Response Flags
- **aa** - Authoritative Answer (domain found in TS database)
- **ra** - Recursive Answer (resolved through recursive process)  
- **ns** - Name Server referral (iterative query referral)
- **nx** - Name not found (domain does not exist)

### Database Structure
**Root Server Database (rsdatabase.txt):**
```
com java.cs.rutgers.edu        # .com domains → TS1 server
edu cheese.cs.rutgers.edu      # .edu domains → TS2 server
x.ai 45.67.89.103             # Direct resolution domains
```

**TS1 Database (ts1database.txt):**
```
www.google.com 9.7.5.6
princeton.com 192.1.1.7
```

**TS2 Database (ts2database.txt):**
```
rutgers.edu 128.1.1.4
njit.edu 10.5.6.7
```

### Socket Programming Implementation
- **TCP Socket Communication** for reliable data transfer
- **Multi-threaded Server Architecture** handling concurrent connections
- **Graceful Connection Management** with proper socket cleanup
- **Error Handling** for network failures and invalid queries
- **Case-insensitive Domain Processing** for robust query handling

## Distributed Deployment

### Machine Configuration
The system was successfully deployed across multiple distributed machines:

```bash
# TS1 Server (.com domains)
java.cs.rutgers.edu:45000

# TS2 Server (.edu domains) 
cheese.cs.rutgers.edu:45000

# Root Server
ilab4.cs.rutgers.edu:45000

# Client
ilab1.cs.rutgers.edu
```

### Deployment Challenges Solved
- **Server Conflict Resolution**: Identified and resolved hostname conflicts between RS and TS2
- **Cross-Machine Communication**: Ensured proper network connectivity across different iLab machines
- **Database Synchronization**: Maintained consistency between server databases and machine assignments
- **File Distribution**: Used SCP for efficient code and database file transfers across machines

## Usage

### Starting the System

1. **Start TS1 Server (.com domains):**
```bash
python3 ts1.py 45000
```

2. **Start TS2 Server (.edu domains):**
```bash
python3 ts2.py 45000
```

3. **Start Root Server:**
```bash
python3 rs.py 45000
```

4. **Run Client:**
```bash
python3 client.py <root_server_hostname> 45000
```

### Input File Format (hostnames.txt)
```
www.google.com rd    # Recursive query
princeton.edu it     # Iterative query
njit.edu it         # Iterative query
x.ai it             # Direct resolution
```

### Sample Output
```
Response for www.google.com: 1 www.google.com 9.7.5.6 1 ra
Response for princeton.edu: 1 princeton.edu cheese.cs.rutgers.edu 2 ns
Response from TS for princeton.edu: 1 princeton.edu 128.1.1.4 3 aa
```

## Requirements

### System Requirements
- **Python 3.x**
- **Linux/Unix Environment** (tested on iLab machines)
- **Network Connectivity** between machines
- **TCP Port Access** (default: 45000)

### Python Libraries
- `socket` - TCP socket communication
- `sys` - Command line argument processing  
- Built-in libraries only (no external dependencies)

### Installation
```bash
# Clone repository
git clone <repository-url>
cd Custom-DNS-Protocol-Implementation

# Ensure all database files are present
ls *database.txt hostnames.txt

# Deploy to distributed machines using SCP
scp *.py *.txt username@machine:/path/to/project/
```

## Performance & Validation

### Testing Results
- **100% Query Resolution Rate** for domains in system databases
- **Successful Cross-Machine Communication** across distributed iLab environment
- **Proper Protocol Compliance** with both recursive and iterative DNS standards
- **Comprehensive Error Handling** for invalid domains and network failures

### Validation Approach
- **Custom Test Cases**: Developed extensive test suites beyond provided examples
- **Multi-Machine Testing**: Validated functionality across different iLab machine configurations
- **Protocol Verification**: Ensured compliance with DNS resolution standards
- **Stress Testing**: Tested concurrent query handling and server reliability

---

**Note**: This project demonstrates practical implementation of distributed systems concepts, network programming, and DNS protocol understanding. The system successfully handles real-world DNS resolution scenarios across a networked environment.

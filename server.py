import socket 
import threading



DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER_IP = socket.gethostname()
SERVER_PORT = 5050
FORMAT = "utf-8"
HEADER = 64
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #First denotes this as an IPV4 socket, second does something else

server_socket.bind((SERVER_IP, SERVER_PORT))






def handle_client(conn, addr):
    print(f"[IP] {addr} connected")
    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if(msg_length): #Since the server can't know how long a client's message will be, we designate a first message of length 64 in this case that allows the client to tell how long their message will be
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[IP] {addr} SENT:\n {msg}")
            if(msg == DISCONNECT_MESSAGE):
                connected = False
    conn.close()
def server_logic():
    while True:
        client_sock, client_addr = server_socket.accept()
        client = threading.Thread(target=handle_client, args=(client_sock, client_addr))
        client.start()
def start():
    print("Server started, waiting for clients...")
    server_socket.listen(5)
    threading.Thread(target=server_logic).start()
    users = threading.active_count()-2
    while True:
        if(users != threading.active_count()-2):
            users = threading.active_count()-2
            print(f"[CLIENT COUNT] {threading.active_count()-2}")
print("Starting server...")
start()
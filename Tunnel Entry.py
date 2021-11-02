import socket
import http.client
from _thread import start_new_thread

tunnel_exit_http_host = socket.gethostbyname("localhost")
print("Tunnel Exit HTTP Host: " + tunnel_exit_http_host)
tunnel_exit_http_port = 8991
print("Tunnel Exit HTTP Port: " + str(tunnel_exit_http_port))
own_udp_port = 13337
print("Tunnel Entry (Own) UDP Port: " + str(own_udp_port))

waiting_http_messages = []

def udp_loop():
    global client_udp_address
    
    client_udp_address = None
    while True:
        data, addr = udp_sock.recvfrom(2**16)
        if client_udp_address == None:
            client_udp_address = addr
        else:
            if addr != client_udp_address:
                raise Exception("Different addresses: " + str(client_udp_address) + " and " + str(addr))
        print("Data from Client: " + str(data))
        waiting_http_messages.append(data)

def http_loop():
    global waiting_http_messages
    
    while True:
        send_data = repr(waiting_http_messages).encode()
        waiting_http_messages = []
        http_connection.request("POST", "/", send_data, {"Content-Length": str(len(send_data))})

        recv_data = http_connection.getresponse().read()
        new_http_messages = eval(recv_data.decode())
        for msg in new_http_messages:
            print("Data from Tunnel Exit: " + str(msg))
            udp_sock.sendto(msg, client_udp_address)
        
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(("", own_udp_port))

http_connection = http.client.HTTPConnection(tunnel_exit_http_host, tunnel_exit_http_port)

start_new_thread(udp_loop, ())
start_new_thread(http_loop, ())

while True:
    pass

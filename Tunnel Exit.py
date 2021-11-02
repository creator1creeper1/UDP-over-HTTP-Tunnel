import socket
import http.server
from _thread import start_new_thread
from random import randint

own_http_port = 8991
print("Tunnel Exit (Own) HTTP Port: " + str(own_http_port))
own_udp_port = randint(10000, 20000)
print("Tunnel Exit (Own) UDP Port: " + str(own_udp_port))
server_udp_host = socket.gethostbyname("localhost")
print("Server UDP Host: " + server_udp_host)
server_udp_port = 12345
print("Server UDP Port: " + str(server_udp_port))

waiting_http_messages = []

def udp_loop():
    while True:
        data, addr = udp_sock.recvfrom(2**16)
        if addr != (server_udp_host, server_udp_port):
            raise Exception("Different addresses: " + str((server_udp_host, server_udp_port)) + " and " + str(addr))
        print("Data from Server: " + str(data))
        waiting_http_messages.append(data)

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        global waiting_http_messages
        
        content_len = int(self.headers.get("Content-Length"))
        recv_data = self.rfile.read(content_len)
        new_http_messages = eval(recv_data.decode())
        for msg in new_http_messages:
            print("Data from Tunnel Entry: " + str(msg))
            udp_sock.sendto(msg, (server_udp_host, server_udp_port))

        send_data = repr(waiting_http_messages).encode()
        waiting_http_messages = []
        self.send_response(200)
        self.send_header("Content-Length", str(len(send_data)))
        self.end_headers()
        self.wfile.write(send_data)

udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(("", own_udp_port))

http_daemon = http.server.HTTPServer(("", own_http_port), RequestHandler)

start_new_thread(http_daemon.serve_forever, ())
start_new_thread(udp_loop, ())

while True:
    pass

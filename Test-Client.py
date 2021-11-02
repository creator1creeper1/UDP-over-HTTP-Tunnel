import socket
from random import randint
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
own_addr = 10000 + randint(0, 255)
sock.bind(("", own_addr))
sock.sendto(b"abc\n", ("localhost", 13337))
data, source = sock.recvfrom(2**16)
print(source, data)

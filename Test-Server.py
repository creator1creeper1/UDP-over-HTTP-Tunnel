import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 12345))
data, source = sock.recvfrom(2**16)
print(source, data)
if data == b"abc\n":
    sock.sendto(b"def\n", source)

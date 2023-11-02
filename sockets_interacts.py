import struct 
import socket

def recv_double(socket):
    msg = socket.recv(8)
    float_value = struct.unpack("d", msg)[0]
    return float_value

def recv_int(socket):
    msg = socket.recv(4)
    int_value = struct.unpack("i", msg)[0]
    return int_value

def send_double(socket, value):
    data_b = bytearray(struct.pack("d", value))
    socket.send(data_b)

def send_int(socket, value):
    data_b = bytearray(struct.pack("i", value))
    socket.send(data_b)

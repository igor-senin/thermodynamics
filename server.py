import socket 
import struct 

from engine import cycle_iteration
from engine import main_cycle_init

from sockets_interacts import send_double, send_int, recv_double

# server calculate data

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 12314))
    s.listen(1)
    print("Server started")

    clientsocket, address = s.accept()
    print("Connection from {} has been established. Descriptor".format(address))

    clientsocket.send(bytes("Send me window xmin, ymin, xmax, ymax", "utf-8"))
    # recv 4 8-byte double
    xmin, ymin, xmax, ymax = [recv_double(clientsocket) for i in range(4)]
    print(xmin, ymin, xmax, ymax)

    particles_size = 2000
    main_cycle_init(xmin, ymin, xmax, ymax, particles_size)
    
    send_int(clientsocket, particles_size)

    print("Starting sending data to client")
    while True:
        particles = cycle_iteration()

        for p in particles:
            send_double(clientsocket, p.coords[0])
            send_double(clientsocket, p.velocity[0])
            send_double(clientsocket, p.coords[1])
            send_double(clientsocket, p.velocity[1])

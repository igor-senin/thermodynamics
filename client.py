import socket
import pygame
import graphics 

from graphics import get_box_bounds
from sockets_interacts import recv_int, recv_double, send_double


def send_bounds(socket):
    bounds = get_box_bounds()
    for i in range(4):
        print(bounds[i])
        data = bounds[i]
        send_double(socket, data)

if __name__ == "__main__":
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect((socket.gethostname(), 12314))

    graphics.init()
    
    msg = sender_socket.recv(1024)
    print(msg.decode("utf-8"))

    send_bounds(sender_socket)
    # send server particles size
    particles_size = recv_int(sender_socket)

    particles = [graphics.DrawableParticle() for i in range(particles_size)]

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(60)
        graphics.draw_surface()
        for i in range(particles_size):
            coord_x = recv_double(sender_socket)
            vel_x = recv_double(sender_socket)
            coord_y = recv_double(sender_socket)
            vel_y = recv_double(sender_socket)
            particles[i].x = coord_x
            particles[i].y = coord_y
            particles[i].vx = vel_x
            particles[i].vy = vel_y
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        scale_coeff = 400.0 / graphics.Width
        metric_coeff = 10**10 # = 1 / hydgrogenium diameter

        for p in particles:
            p.Draw(scale_coeff, metric_coeff)

        graphics.display_update()

    pygame.quit()
    sender_socket.close()

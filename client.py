import socket
import pygame
import graphics 

from graphics import get_box_bounds
from sockets_interacts import recv_int, recv_double, send_double


def send_bounds(socket):
    bounds = get_box_bounds()
    for i in range(4):
        #print(bounds[i])
        data = bounds[i]
        send_double(socket, data)

if __name__ == "__main__":
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sender_socket.connect(("localhost", 12314))

    graphics.init()
    
    msg = sender_socket.recv(1024)
    print(msg.decode("utf-8"))

    send_bounds(sender_socket)
    # send server particles size
    particles_size = recv_int(sender_socket)

    scale_coeff = 400.0 / graphics.Width
    metric_coeff = 10**10 # = 1 / hydgrogenium diameter

    particles = [graphics.DrawableParticle() for i in range(particles_size)]
    xmin, xmax, ymin, ymax = get_box_bounds()
    xlen = (xmax - xmin) / metric_coeff
    ylen = (ymax - ymin) / metric_coeff

    clock = pygame.time.Clock()
    run = True

    reduse_draw_statistics = 0
    statistics = []
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

        for p in particles:
            p.Draw(scale_coeff, metric_coeff)

        reduse_draw_statistics += 1 
        if reduse_draw_statistics % 20 == 0:
            reduse_draw_statistics = 0
            statistics.clear()
            statistics.append(["Max velocity", recv_double(sender_socket)])
            statistics.append(["Min velocity", recv_double(sender_socket)])
            statistics.append(["Mean velocity", recv_double(sender_socket)])
            statistics.append(["Hits on the walls", recv_double(sender_socket)])

            pr_left = recv_double(sender_socket)
            pr_left /= (xlen * 0.1) # xlen ~ S; 0.1 ~ dt
            statistics.append(["Left wall pressure", pr_left])

            pr_right = recv_double(sender_socket)
            pr_right /= (xlen * 0.1) # xlen ~ S; 0.1 ~ dt
            statistics.append(["Right wall pressure", pr_right])

            pr_top = recv_double(sender_socket)
            pr_top /= (ylen * 0.1) # ylen ~ S; 0.1 ~ dt
            statistics.append(["Top wall pressure", pr_top])

            pr_bottom = recv_double(sender_socket)
            pr_bottom /= (ylen * 0.1) # ylen ~ S; 0.1 ~ dt
            statistics.append(["Bottom wall pressure", pr_bottom])

            pr_mean = (pr_left + pr_right + pr_bottom + pr_top) / 4.0

            statistics.append(["Pressure", pr_mean])
        else:
            for i in range(8):
                recv_double(sender_socket)


        graphics.draw_statistics(statistics)

        graphics.display_update()

    pygame.quit()
    sender_socket.close()

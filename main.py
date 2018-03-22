import math
import pygame
from pygame.locals import *

import trajectory
from trajectory import *


def main():
    pygame.init()

    # graphics objects initialization
    screen = pygame.display.set_mode((1280, 720))
    x0 = screen.get_size()[0] / 2
    y0 = screen.get_size()[1] / 2

    background = pygame.Surface(screen.get_size())
    background.fill((0, 0, 0))
    
    large_rect = pygame.Surface((50, 50))
    large_rect.fill((255, 255, 255))

    small_rect = pygame.Surface((10, 10))
    small_rect.fill((255, 0, 0))
    
    
    # trajectory
    curve = Curve()
    curve.waypoints.append(Event(0,   0,   0, 0))

    # corners
    curve.waypoints.append(Event(0,   0,   0, 0))
    curve.waypoints.append(Event(200, 0,   0, 2))
    curve.waypoints.append(Event(200, 100, 0, 4))
    curve.waypoints.append(Event(400, 100, 0, 6))
    curve.waypoints.append(Event(400, 200, 0, 8))
    curve.waypoints.append(Event(0,   200, 0, 10))
    curve.waypoints.append(Event(0,   0,   0, 12))

    # back and forth
    curve.waypoints.append(Event(0,     0,   0, 14))
    curve.waypoints.append(Event(-100, -100, 0, 16))
    curve.waypoints.append(Event( 100,  100, 0, 18))
    curve.waypoints.append(Event(-100, -100, 0, 20))
    curve.waypoints.append(Event( 0,    0,   0, 22))

    # circle
    curve.waypoints.append(Event( 0,    0,   0, 23))
    curve.waypoints.append(Event( 200,  80,  0, 24))
    curve.waypoints.append(Event( 80,   200, 0, 25))
    curve.waypoints.append(Event(-80,   200, 0, 26))
    curve.waypoints.append(Event(-200,  80,  0, 27))
    curve.waypoints.append(Event(-200, -80,  0, 28))
    curve.waypoints.append(Event(-80,  -200, 0, 29))
    curve.waypoints.append(Event( 80,  -200, 0, 30))
    curve.waypoints.append(Event( 200, -80,  0, 31))
    curve.waypoints.append(Event( 200,  80,  0, 32))
    curve.waypoints.append(Event( 80,   200, 0, 33))
    curve.waypoints.append(Event(-80,   200, 0, 34))
    curve.waypoints.append(Event(-200,  80,  0, 35))
    curve.waypoints.append(Event(-200, -80,  0, 36))
    curve.waypoints.append(Event(-80,  -200, 0, 37))
    curve.waypoints.append(Event( 80,  -200, 0, 38))
    curve.waypoints.append(Event( 200, -80,  0, 40))
    curve.waypoints.append(Event( 0,    0,   0, 42))
    curve.waypoints.append(Event( 0,    0,   0, 43))

    curve.waypoints.append(Event( 0,    0,   0, 43))

    
    running = True
    
    while running:
        # for loop through the event queue
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    
                    
        # clear screen
        screen.blit(background, (0, 0))
        
        time = pygame.time.get_ticks() / 1000
        time = time % curve.waypoints[ len(curve.waypoints) - 1 ].t

        # find and draw "drone target"
        current_event = curve.sample_smooth(time)
        screen.blit(large_rect, (x0 + current_event.x, y0 + current_event.y))

        window_backward = 2
        window_forward = 2
        for i in range(0, len(curve.waypoints)):
            if time - window_backward < curve.waypoints[i].t < time + time + window_forward:
                screen.blit(small_rect, (x0 + 20 + curve.waypoints[i].x, y0 + 20 + curve.waypoints[i].y))
        
        pygame.display.flip()

main()    

from math import sqrt
from pygame import gfxdraw
import pygame, time, sys

class Rocket(object):
    def __init__(self):
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.active = False

class Explosion(object):
    def __init__(self):
        self.position = [0, 0]
        self.radius = 50
        self.t = 0.0
        self.duration = 0.2
        self.active = False

rocket = Rocket()
explosion = Explosion()
mousepos = [0, 0]

def draw(screen):
    color = (255, 255, 255)

    mx, my = mousepos
    gfxdraw.circle(screen, mx, my, 10, color)

    if rocket.active:
        x, y = rocket.position
        gfxdraw.circle(screen, int(x), int(y), 5, color)

    if explosion.active:
        x, y = explosion.position
        r = explosion.radius * explosion.t
        gfxdraw.circle(screen, int(x), int(y), int(r), color)

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)
    if event.type == pygame.MOUSEMOTION:
        mousepos[:] = event.pos
    if event.type == pygame.MOUSEBUTTONDOWN:
        rocket.position[:] = 0, 0
        rocket.active = True

def update(dt):
    if rocket.active:
        x, y = rocket.position
        tx, ty = mousepos
        dx = tx-x
        dy = ty-y
        length = sqrt(dx*dx + dy*dy)
        xv = dx/length * 200
        yv = dy/length * 200
        rocket.velocity[:] = xv, yv

        if length < 10:
            rocket.active = False
            explosion.active = True
            explosion.position = rocket.position
            explosion.t = 0.0

        x, y = rocket.position
        xv, yv = rocket.velocity
        x += xv * dt
        y += yv * dt
        rocket.position[:] = x, y

    if explosion.active:
        explosion.t += dt / explosion.duration
        if explosion.t > 1.0:
            explosion.active = False

fps = 60
frameskip = 2

if __name__=='__main__':
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1024, 768))

    last = now = time.time()
    accum = 0
    while 1:
        accum += (now - last) * fps
        for x in range(0, min(int(accum), frameskip)):
            update(1.0/fps)
        accum -= int(accum)
        screen.fill((0, 0, 0))
        draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            dispatch(event)
        last = now
        now = time.time()

from math import sqrt
from pygame import gfxdraw
import pygame, time, sys

class Robot(object):
    def __init__(self):
        self.active = True
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.health = 1.0
        self.state = 'chase'

class Explosion(object):
    def __init__(self):
        self.position = [0, 0]
        self.radius = 50
        self.t = 0.0
        self.duration = 0.2
        self.active = False

robot = Robot()
explosion = Explosion()
mousepos = [0, 0]

def draw(screen):
    color = (255, 255, 255)

    mx, my = mousepos
    gfxdraw.circle(screen, mx, my, 10, color)

    if robot.active:
        x, y = robot.position
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
        explosion.active = True
        explosion.position = mousepos
        explosion.t = 0.0

def update(dt):
    if robot.active:
        x, y = robot.position
        tx, ty = mousepos
        dx = tx-x
        dy = ty-y
        length = sqrt(dx*dx + dy*dy)

        if robot.health < 0:
            robot.active = False
        if robot.state == 'chase' and length > 0:
            xv = dx/length * 200
            yv = dy/length * 200
            robot.velocity[:] = xv, yv
        if robot.state == 'flee' and length > 0:
            xv = -dx/length * 200
            yv = -dy/length * 200
            robot.velocity[:] = xv, yv
        if robot.health < 0.5 and robot.state == 'chase':
            robot.state = 'flee'
        if robot.state == 'flee' and length > 150:
            robot.state = 'heal'
        if robot.state == 'heal':
            robot.health += dt * 0.2
            robot.velocity[:] = 0, 0
        if robot.state == 'heal' and robot.health > 1.0:
            robot.state = 'chase'
        if robot.state == 'heal' and length < 150:
            robot.state = 'flee'

        x, y = robot.position
        xv, yv = robot.velocity
        x += xv * dt
        y += yv * dt
        robot.position[:] = x, y

    if explosion.active:
        explosion.t += dt / explosion.duration
        if explosion.t > 1.0:
            explosion.active = False
        if distance(explosion.position, robot.position) < explosion.radius * explosion.t:
            robot.health -= dt

def distance((x1, y1), (x2, y2)):
    dx = x1 - x2
    dy = y1 - y2
    return sqrt(dx*dx + dy*dy)

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

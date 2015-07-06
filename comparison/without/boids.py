from math import sqrt, exp
from pygame import gfxdraw
from random import random
import pygame, time, sys

class vec2(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        return iter((self.x, self.y))

    def __add__(self, other):
        return vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return vec2(self.x * other, self.y * other)

    def __div__(self, other):
        return vec2(self.x / other, self.y / other)

    def __neg__(self):
        return vec2(-self.x, -self.y)

    @property
    def magnitude(self):
        return sqrt(self.x*self.x + self.y*self.y)

    @property
    def normal(self):
        x, y = self.x, self.y
        length = sqrt(x*x + y*y)
        if length > 0:
            return vec2(x / length, y / length)
        return vec2(x, y)

    def limit(self, magnitude):
        mag = self.magnitude
        if mag > magnitude:
            return self * (magnitude / mag)
        return self

class Robot(object):
    def __init__(self):
        self.active = True
        self.position = vec2(0, 0)
        self.velocity = vec2(0, 0)
        self.acceleration = vec2(0, 0)

robots = []
for x in range(50):
    robot = Robot()
    robot.position = vec2(x*10, 20 + x*5)
    robots.append(robot)

maxspeed = 150
maxforce = 200

def draw(screen):
    color = (255, 255, 255)
    for robot in robots:
        x, y = robot.position
        gfxdraw.circle(screen, int(x), int(y), 5, color)

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)

def update(dt):
    for robot in robots:
        others = []
        for other in robots:
            if other is not robot:
                d = (other.position - robot.position).magnitude
                if d < 40:
                    others.append((other, d))
        # separation
        steer = vec2(0, 0)
        desired = 25.0
        count = 0
        for other, d in others:
            if d < desired:
                delta = robot.position - other.position
                steer += delta / d
                count += 1
        if count > 0:
            steer /= count
            steer = (steer.normal * maxspeed) - robot.velocity
            robot.acceleration += steer.limit(maxforce) * 2.5
        # stay on screen
        if robot.position.x < 0:
            robot.acceleration.x += maxforce * 10
        if robot.position.x > width:
            robot.acceleration.x -= maxforce * 10
        if robot.position.y < 0:
            robot.acceleration.y += maxforce * 10
        if robot.position.y > height:
            robot.acceleration.y -= maxforce * 10

        # align
        velo = robot.velocity
        for other, d in others:
            velo += other.velocity
        velo /= len(others) + 1
        steer = velo.normal * maxspeed - robot.velocity
        robot.acceleration += steer.limit(maxforce)

        # cohesion
        center = robot.position
        for other, d in others:
            center += other.position
        center /= len(others) + 1
        robot.acceleration += seek(robot, center)

    for robot in robots:
        robot.velocity += robot.acceleration * dt
        robot.position += robot.velocity * dt
        robot.acceleration = vec2(0, 0)

def seek(robot, target, radius=10.0):
    delta = target - robot.position
    magnitude = delta.magnitude
    desired = delta / magnitude if magnitude > 0 else delta
    steer = desired - robot.velocity
    strength = min(1.0, magnitude / radius)
    return steer.limit(maxforce) * strength

fps = 60
frameskip = 2
width = 1024
height = 768

if __name__=='__main__':
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((width, height))

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

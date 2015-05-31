from elmbonsai import *
from gamebonsai import *
import pygame, time, sys, math
import operator

left = key_input(pygame.K_LEFT)
right = key_input(pygame.K_RIGHT)
up = key_input(pygame.K_UP)
down = key_input(pygame.K_DOWN)

def init(signals, layer):
    font = pygame.font.Font(None, 32)

    # Control signals
    xc = lift(operator.mul, keyboard_axis(left, right), 50)
    yc = lift(operator.mul, keyboard_axis(up, down), 50)
    # Velocity signals
    xv = accum(0, now, xc)
    yv = accum(0, now, yc)
    # Position signals
    x = accum(50.0, now, xv)
    y = accum(50.0, now, yv)
    # Moving text, with its velocity printed out.
    v = layer.show(Text, font, lift("{:0.2f},{:0.2f}".format, xv, yv), x, y)
    signals.spawn(v)

def dispatch(signals, event):
    if event.type == pygame.QUIT:
        signals.discard()
    if (event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE):
        signals.discard()

if __name__=='__main__':
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1024, 768))
    signals = ReactionGroup(time.time())
    layer = Layer()
    init(signals, layer)
    while 1:
        for event in pygame.event.get():
            dispatch(signals, event)
            signals.update(event)
        signals.update(Tick(Tick, time.time()))
        if not signals.active:
            sys.exit(0)
        screen.fill((0, 0, 0))
        layer.update(screen)
        pygame.display.flip()

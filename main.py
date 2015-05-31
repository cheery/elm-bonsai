from elmbonsai import *
from gamebonsai import *
import pygame, time, sys, math

left = key_input(pygame.K_LEFT)
right = key_input(pygame.K_RIGHT)

rect_t = [0]
rect = [100, 100, 10, 10]
color = [0, 128, 0]

def recolor(r, g, b):
    color[0] = 255*abs(r)
    color[1] = 255*abs(g)
    color[2] = 255*abs(b)
    return (r, g, b)

def keyboard_axis(neg, pos):
    def _keyboard_axis_(neg, pos):
        return float(pos - neg)
    return lift(_keyboard_axis_, neg, pos)

def accum(control, t, v):
    rect[0] += control * (t - rect_t[0]) * v
    rect_t[0] = t
    if not 0 < rect[0] < 1024:
        raise StopIteration()

def init(signals):
    signals.spawn(lift(accum, keyboard_axis(left, right), now, constant(500)))

    s = lift(math.sin, now)
    c = lift(math.cos, now)
    #signals.spawn(lift(recolor, s, c, s))

def animation_frame(screen):
    screen.fill(color)
    screen.fill((255, 255, 255), rect)

def dispatch(signals, event):
    if event.type == pygame.QUIT:
        signals.discard()
    if (event.type == pygame.KEYDOWN
        and event.key == pygame.K_ESCAPE):
        signals.discard()

if __name__=='__main__':
    pygame.display.init()
    screen = pygame.display.set_mode((1024, 768))
    signals = ReactionGroup(time.time())
    init(signals)
    while 1:
        for event in pygame.event.get():
            dispatch(signals, event)
            signals.update(event)
        signals.update(Tick(Tick, time.time()))
        if not signals.active:
            sys.exit(0)
        animation_frame(screen)
        pygame.display.flip()

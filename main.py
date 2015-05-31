from elmbonsai import *
from gamebonsai import *
import pygame, time, sys, math
import operator

def pick(control, sequence):
    def _pick_(control, sequence):
        return sequence[control]
    return lift(_pick_, control, sequence)

def bundle(result, *rest):
    def _bundle_(result, *rest):
        return result
    return lift(_bundle_, result, *rest)

def simple_button(x, y, width, height, click=False):
    def _hover_(x, y, width, height, (px, py)):
        return 0 <= px - x < width and 0 <= py - y < height
    hover = lift(_hover_, x, y, width, height, mouse_position)
    click = lift(operator.or_, click, lift(operator.and_, hover, mouse_button(1)))
    color = pick(click, [(155, 155, 155), (200, 200, 200)])
    visual = layer.show(Rectangle, x, y, width, height, color)
    return bundle(click, visual)

def init(signals, layer):
    font = pygame.font.Font(None, 32)

    # Lets make a button
    left = simple_button(1*32, 2*32, 32, 32, key_input(pygame.K_LEFT))
    right = simple_button(3*32, 2*32, 32, 32, key_input(pygame.K_RIGHT))
    up = simple_button(2*32, 1*32, 32, 32, key_input(pygame.K_UP))
    down = simple_button(2*32, 3*32, 32, 32, key_input(pygame.K_DOWN))

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

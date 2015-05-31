from elmbonsai import *
from gamebonsai import *
import pygame, time, sys, math, random
import operator

def simple_button(x, y, width, height, click=False):
    def _hover_(x, y, width, height, (px, py)):
        return 0 <= px - x < width and 0 <= py - y < height
    hover = lift(_hover_, x, y, width, height, mouse_position)
    click = lift(operator.or_, click, lift(operator.and_, hover, mouse_button(1)))
    color = pick(click, ((155, 155, 155), (200, 200, 200)))
    visual = layer.show(Rectangle, x, y, width, height, color)
    return bundle(click, visual)

def key_spawner(signals, layer, font):
    def _init_spawn_(reaction):
        return None
    def _spawn_input_(cell, event):
        if event.type == pygame.KEYDOWN:
            def _keep_only_(cond):
                if not cond:
                    raise Discard()
            signals.spawn(bundle(
                lift(_keep_only_, key_input(event.key)),
                layer.show(Text,
                    font,
                    lift("{:0.2f} {}".format, after, pygame.key.name(event.key)),
                    random.randint(0, 1024),
                    random.randint(0, 768))))
            if event.key == pygame.K_F4:
                signals.discard()
    return bundle(
        Input(_init_spawn_, _spawn_input_),
        layer.show(Text, font, "You may spawn nibs. Press F4 to stop", 10, 10))


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


    spawner = signals.group()
    spawner.spawn(key_spawner(spawner, layer, font))

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

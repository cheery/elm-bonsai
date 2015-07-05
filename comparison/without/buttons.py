import pygame, time, sys

class VirtualButton(object):
    def __init__(self, key, x, y):
        self.key = key
        self.down = False
        self.x = x
        self.y = y

left = VirtualButton(pygame.K_LEFT, 0, 1)
up = VirtualButton(pygame.K_UP, 1, 0)
right = VirtualButton(pygame.K_RIGHT, 2, 1)
down = VirtualButton(pygame.K_DOWN, 1, 2)
buttons = [left, up, right, down]

player = [50, 50]

scale = 16
speed = 500

def draw(screen):
    for button in buttons:
        color = (255, 255, 255)
        if button.down:
            color = (0, 255, 0)
        screen.fill(color, (button.x*scale, button.y*scale, scale, scale))
        screen.fill((255, 255, 0), player + [32, 32])

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)
    if event.type == pygame.KEYDOWN:
        for button in buttons:
            if button.key == event.key:
                button.down = True
    if event.type == pygame.KEYUP:
        for button in buttons:
            if button.key == event.key:
                button.down = False

def update(dt):
    if left.down:
        player[0] -= dt * speed
    if right.down:
        player[0] += dt * speed
    if up.down:
        player[1] -= dt * speed
    if down.down:
        player[1] += dt * speed

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

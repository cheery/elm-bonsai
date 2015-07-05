from pygame import gfxdraw
import pygame, sys

class DragDraw(object):
    def __init__(self):
        self.active = False
        self.seq = []

dragdraw = DragDraw()

def draw(screen):
    last = None
    for this in dragdraw.seq:
        if last is not None:
            x1, y1 = last
            x2, y2 = this
            color = (255, 255, 255)
            if dragdraw.active:
                color = (0, 255, 0)
            gfxdraw.line(screen, x1, y1, x2, y2, color)
        last = this

def dispatch(event):
    if event.type == pygame.QUIT:
        sys.exit(0)
    if (event.type == pygame.MOUSEBUTTONDOWN
        and event.button == 1):
        dragdraw.active = True
        dragdraw.seq[:] = []
        dragdraw.seq.append(event.pos)
    if (event.type == pygame.MOUSEBUTTONUP
        and event.button == 1):
        dragdraw.active = False
    if (dragdraw.active
        and event.type == pygame.MOUSEMOTION):
        dragdraw.seq.append(event.pos)


if __name__=='__main__':
    pygame.display.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1024, 768))
    while 1:
        for event in pygame.event.get():
            dispatch(event)
        screen.fill((0, 0, 0))
        draw(screen)
        pygame.display.flip()

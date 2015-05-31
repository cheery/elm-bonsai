from elmbonsai import *
import pygame

def key_input(keycode):
    def _key_intro_(reaction):
        return False
    def _key_input_(cell, event):
        if (event.type == pygame.KEYDOWN
            and event.key == keycode):
            cell.value = True
            return True
        if (event.type == pygame.KEYUP
            and event.key == keycode):
            cell.value = False
            return True
        return False
    return Input(_key_intro_, _key_input_)

class Layer(object):
    def __init__(self):
        self.elements = []

    def update(self, screen):
        self.elements[:] = (x for x in self.elements if x.update(screen))

    def add(self, cls, link, *args, **kw):
        element = cls(link, *args, **kw)
        self.elements.append(element)
        return element

    def show(self, cls, *args):
        def _intro_(reaction, *args):
            print args
            return self.add(cls, reaction, *args)
        def _foldp_(element, *args):
            element.adjust(*args)
            return element
        return liftfoldp(_intro_, _foldp_, *args)

class Rectangle(object):
    def __init__(self, link, *args):
        self.link = link
        self.adjust(*args)

    def adjust(self, x, y, width, height, color=(255, 255, 255, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def update(self, screen):
        if not self.link.active:
            return False
        screen.fill(
            self.color,
            (self.x, self.y, self.width, self.height))
        return True

class Text(object):
    def __init__(self, link, *args):
        self.link = link
        self.adjust(*args)

    def adjust(self, font, text, x, y, color=(255, 255, 255, 255)):
        self.font = font
        self.text = text
        self.x = x
        self.y = y
        self.color = color

    def update(self, screen):
        if not self.link.active:
            return False
        screen.blit(
            self.font.render(self.text, True, self.color),
            (self.x, self.y))
        return True

class AccumCell(Cell):
    def __init__(self, origin, time, velocity):
        Cell.__init__(self, origin)
        self.last = time.value
        self.time = time
        self.velocity = velocity

    def update(self, event):
        if self.time.changed:
            dt = self.time.value - self.last
            value = self.value + dt * self.velocity.value
            self.changed = value != self.value
            self.value = value
            self.last = self.time.value

class accum(Signal):
    def __init__(self, origin, time, velocity):
        self.origin = origin
        self.time = time
        self.velocity = velocity

    def deploy(self, deploy):
        return AccumCell(
            self.origin, 
            deploy.one(self.time),
            deploy.one(self.velocity))

def keyboard_axis(neg, pos):
    def _keyboard_axis_(neg, pos):
        return float(pos - neg)
    return lift(_keyboard_axis_, neg, pos)

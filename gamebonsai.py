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

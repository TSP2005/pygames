import math
from .utils import Animations as anims
import pygame
import random


class Entity:
    def __init__(self, loc, e_type, state):
        self.loc = loc
        self.e_type = e_type
        self.state = state
        self.collisions = {'left': False,
                           'right': False,
                           'top': False,
                           'bottom': False}

        self.animations = {
            'idle': anims(self.e_type, 'idle', [12, 12, 12, 12, 12], True),
            'walk': anims(self.e_type, 'walk', [10, 10, 10, 10, 10, 10], True),
            'walk_up_down': anims(self.e_type, 'walk_up_down', [7, 7, 7], True)
        }

        self.current_anim = self.animations[self.state]
        self.rect = pygame.Rect(self.loc[0], self.loc[1], self.current_anim.get_frame_width(),
                                self.current_anim.get_frame_height())

    def move(self, movement=None):
        if movement is None:
            movement = [0, 0]
        self.movement_x = movement[0]
        self.movement_y = movement[1]
        if self.movement_x != 0 and self.movement_y != 0:
            self.movement_y *= math.sqrt(1 / 2)
            self.movement_x *= math.sqrt(1 / 2)
        self.loc[0] += self.movement_x
        self.loc[1] += self.movement_y

    def render(self, surf, scroll, flip):
        self.current_anim.render(surf, self.loc, scroll, flip)
        self.current_anim.update()

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.current_anim = self.animations[self.state]


class Zombie:
    def __init__(self, loc):
        self.loc = loc
        self.goal = None
        self.state = 'walk'
        self.flip = False
        self.animations = {
            'walk': anims('zombie', 'walk', [15, 15, 15, 15], True),
            'attack': anims('zombie', 'attack', [3, 7, 7], False)
        }
        self.current_anim = self.animations[self.state]
        self.rect = pygame.Rect(self.loc[0], self.loc[1], 18, 32)

    def update(self):
        slope = (self.loc[1] - self.goal[1])/(self.loc[0] - self.goal[0])
        direction = math.atan(slope)
        if not self.flip:
            self.loc[0] += math.cos(direction)
            self.loc[1] += math.sin(direction)
        if self.flip:
            self.loc[0] -= math.cos(direction)
            self.loc[1] -= math.sin(direction)

    def render(self, surf, scroll, flip):
        self.current_anim.render(surf, self.loc, scroll, flip)
        self.current_anim.update()

    def set_state(self, state):
        if state != self.state:
            self.state = state
            self.current_anim = self.animations[self.state]

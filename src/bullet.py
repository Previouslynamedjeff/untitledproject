import pygame
import math
import random


class Bullet():

    def __init__(self, health, direction, start, colour):
        self.dims: tuple((int, int)) = (20, 20)
        self.sprite = pygame.Surface((20, 20))
        self.sprite.fill(colour)
        self.sprite.set_colorkey(colour)
        self.x, self.y = start[0], start[1]

        self.body = pygame.Rect(self.pos, self.dims)

        #health
        self.hp = health
        
        #mobility
        self.speed = 2
        self.direction = direction

    @property
    def w(self):
        return self.dims[0]

    @property 
    def h(self):
        return self.dims[1]

    @property 
    def pos(self):
        return (self.x, self.y)

    def update(self):

        moveVecx = self.direction["chx"] * self.speed
        moveVecy = self.direction["chy"] * self.speed
        self.x += moveVecx
        self.y += moveVecy
        self.body.x = self.x
        self.body.y = self.y
        

    def render(self, screen, dims):
        screen.blit(self.sprite, (self.x, self.y))
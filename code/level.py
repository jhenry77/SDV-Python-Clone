from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from player import Player
from overlay import Overlay
from sprites import Ordinary

class Level:
    def __init__(self):


        # Gets the display
        self.displaySurface = pygame.display.get_surface()

        # Sprite Groups
        self.allSprites = Camera()


        self.setup()
        self.overlay = Overlay(self.player)



    def run(self,dt):
        self.displaySurface.fill('black')
        # self.allSprites.draw(self.displaySurface)
        self.allSprites.newDraw(self.player)
        self.allSprites.update(dt)







        self.overlay.updateDisplay()


    def setup(self):
        Ordinary(
            pos = (0,0),
            surface = pygame.image.load('../images/ground/ground.png').convert_alpha(),
            groups= self.allSprites,
            z = LAYERS['ground']
        )
        self.player = Player((640,360),self.allSprites)


class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()
        # Used for making the 3d camera effect, moving around the screen 
        self.offset = pygame.math.Vector2()

    def newDraw(self,player):
        # This is for setting the offset for the camera
        # What this does is ensure all the sprites in the game such as the ground are drawn relative to the player
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2
        # Creates a for loop to itterate through all of the layer values
        for layers in LAYERS.values():
            # For loop to itterate through all of the sprites
            for sprite in self.sprites():
                    # if the spirtes z value is equivalent to the current layer then get that sprites location and subtract the offset from it to move it relative to the player and then draw it
                    if sprite.z == layers:
                        offsetRect = sprite.rect.copy()
                        offsetRect.center -= self.offset
                        self.displaySurface.blit(sprite.image, offsetRect)
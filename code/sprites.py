from typing import Any
import pygame
from settings import *
from settings import LAYERS
from timer import Timer

class Ordinary(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        # Making the hitbox slightly narrowers and a lot shorter to allow us to walk behind the object
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * .75)



class Interactions(Ordinary):
    def __init__(self,pos,size,groups,name):
        surface = pygame.Surface(size)
        super().__init__(pos,surface,groups)
        self.name = name



class Particle(Ordinary):
    def __init__(self, pos, surface, groups, z, time = 200):

        super().__init__(pos, surface, groups, z)


        self.startTime = pygame.time.get_ticks()
        self.duration = time

        #white surface for particles
        # Masks https://www.youtube.com/watch?v=tJiKYMQJnYg
        maskSurface = pygame.mask.from_surface(self.image)
        particleSurface = maskSurface.to_surface()
        particleSurface.set_colorkey((0,0,0))
        self.image = particleSurface


    def update(self,dt):
        currTime = pygame.time.get_ticks()
        if currTime - self.startTime > self.duration:
            self.kill()

class waterSprite(Ordinary):
    def __init__(self, pos, animationFrame, groups):

        #animation
        self.animation = animationFrame
        self.frameNum = 0

        #sprite creation
        super().__init__(
                            pos = pos, 
                            surface = self.animation[self.frameNum], 
                            groups = groups,
                            z = LAYERS['water']
        )


    def animateWater(self,dt):
        self.frameNum += 8 * dt

        # ensure we dont go over the amount of frames we have for an animation
        if self.frameNum >= len(self.animation):
            self.frameNum = 0

        self.image = self.animation[int(self.frameNum)]

    def update(self,dt):
        self.animateWater(dt)
        
class natFlower(Ordinary):
    def __init__(self, pos, surface, groups):
        super().__init__(pos,surface,groups,LAYERS['main'])
        self.hitbox = self.rect.copy().inflate(-20,-self.rect.height * 0.9)

class Tree(Ordinary):
    def  __init__(self, pos, surface, groups, name, inventoryAdd):
        super().__init__(pos,surface,groups,LAYERS['main'])
        # Health of the tree
        self.health = 5
        # Tells us if the tree is alive
        self.alive = True
        self.stumpSurface = pygame.image.load(f'../graphics/stumps/{"small" if name == "Small" else "large"}.png').convert_alpha()
        self.invalTimer = Timer(200)


        self.addToInventory = inventoryAdd

    def damage(self):

        self.health -= 1

    def checkHealth(self):
        if self.health <= 0:
            # if tree is dead then set the trees image to the corresponding stump
            self.image = self.stumpSurface
            # Create a new rect that has an equivalent mid bottom
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            # Copy that rect into our hitbox but make it slightly narrower and much shorter
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.addToInventory('wood')


    def update(self,dt):
        if self.alive:
            self.checkHealth()


class Interaction(Ordinary):
    def __init__(self, pos, size, groups, name):
        surface = pygame.Surface(size)
        super().__init__(pos, surface, groups)
        self.name = name
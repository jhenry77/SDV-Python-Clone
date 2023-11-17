import pygame
from settings import *

class Ordinary(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z = LAYERS['main']):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        # Making the hitbox slightly narrowers and a lot shorter to allow us to walk behind the object
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * .75)



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
    def  __init__(self, pos, surface, groups, name):
        super().__init__(pos,surface,groups,LAYERS['main'])
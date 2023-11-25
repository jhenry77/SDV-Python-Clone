from typing import Iterable, Union
import pygame
from pygame.sprite import AbstractGroup
from settings import *
from player import Player
from overlay import Overlay
from sprites import Ordinary,waterSprite,natFlower,Tree,Interactions
from pytmx.util_pygame import load_pygame
from helpful import *
from transition import Transition

class Level:
    def __init__(self):


        # Gets the display
        self.displaySurface = pygame.display.get_surface()

        # Sprite Groups
        self.allSprites = Camera()
         # Tree Sprites
        self.treeSprites = pygame.sprite.Group()
        # Collision Sprites
        self.collisionSprites = pygame.sprite.Group()
       
        # Iteraction sprites
        self.interactionSprites = pygame.sprite.Group()


        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.resetDay,self.player)



    def run(self,dt):
        self.displaySurface.fill('black')
        # self.allSprites.draw(self.displaySurface)
        self.allSprites.newDraw(self.player)
        self.allSprites.update(dt)






        # print(self.player.itemInventory)
      
        self.overlay.updateDisplay()
        if self.player.sleep:
            self.transition.play()
            

    def setup(self):

        
        # Loads the map data created using tiled
        mapData = load_pygame('../map/map.tmx')
        


        #taking the data from the map from the house furniture bottom
        for mapLayer in ['HouseFloor','HouseFurnitureBottom']:
            for x, y, surface in mapData.get_layer_by_name(mapLayer).tiles():
                # Creating a genric sprite
                # multiply by tile size so that you convert correctly from tiled
                Ordinary((x * TILE_SIZE,y * TILE_SIZE), surface, self.allSprites,LAYERS['house bottom'])
        # data for the house
        for mapLayer in ['HouseWalls','HouseFurnitureTop']:
            for x, y, surface in mapData.get_layer_by_name(mapLayer).tiles():
                # Creating a genric sprite
                # multiply by tile size so that you convert correctly from tiled
                Ordinary((x * TILE_SIZE,y * TILE_SIZE), surface, self.allSprites,LAYERS['main'])
        # Fence Sprite : Main Layer
        for x,y, surface in mapData.get_layer_by_name("Fence").tiles():
            Ordinary((x * TILE_SIZE,y * TILE_SIZE), surface, [self.allSprites, self.collisionSprites],LAYERS['main'])

        # Water Sprite : Water Layer
        waterFrames = importFolder('../graphics/water')
        for x,y, surface in mapData.get_layer_by_name("Water").tiles():
            waterSprite((x * TILE_SIZE, y * TILE_SIZE), waterFrames,self.allSprites)


        # Natrual Flowers : Main Layer
        for flower in mapData.get_layer_by_name("Decoration"):
            # Dont need to multiply as these are not tiles and therefore have pixel measurements
            natFlower((flower.x, flower.y),flower.image,[self.allSprites,self.collisionSprites])


        # Trees : Main Layer 
        for tree in mapData.get_layer_by_name("Trees"):
            # Dont need to multiply as these are not tiles and therefore have pixel measurements
            Tree((tree.x, tree.y),tree.image,[self.allSprites,self.collisionSprites,self.treeSprites], tree.name,self.addToInventory)

        # Collision Tiles from Tiled / Base Level Collision
        for x,y, surface in mapData.get_layer_by_name("Collision").tiles():
            Ordinary((x * TILE_SIZE,y * TILE_SIZE), pygame.Surface((TILE_SIZE,TILE_SIZE)), self.collisionSprites)

        # Player Items such as Player Sprite, Spawn, Trader, Bed
        for playerItems in mapData.get_layer_by_name("Player"):
            # Sets spawn point
            if playerItems.name == "Start":
                self.player = Player((playerItems.x,playerItems.y), self.allSprites, self.collisionSprites, self.treeSprites, self.interactionSprites)
            # Creates the interaction location for the bed
            if playerItems.name == 'Bed':
                Interactions((playerItems.x,playerItems.y), (playerItems.width, playerItems.height), self.interactionSprites, 'Bed')
                


        # Creating the ground sprite
        Ordinary(
            pos = (0,0),
            surface = pygame.image.load('../graphics/ground/ground.png').convert_alpha(),
            groups= self.allSprites,
            z = LAYERS['ground']
        )

    def addToInventory(self,item):
        self.player.itemInventory[item] += 1

    def resetDay(self):


        # Reset apples
        for tree in self.treeSprites:
            for apple in tree.appleSprites.sprites():
                apple.kill()
            tree.createApples()

    
# A new class that will handle some of the things that pygame.sprite controls
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
            # For loop to itterate through all of the sprites, sorts the sprite using the center of a sprite as the sorting key, this is so that the player will appear behind flowers/trees aka faking more 3-d
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                    # if the spirtes z value is equivalent to the current layer then get that sprites location and subtract the offset from it to move it relative to the player and then draw it
                    if sprite.z == layers:
                        offsetRect = sprite.rect.copy()
                        offsetRect.center -= self.offset
                        # Actually draw the sprite
                        self.displaySurface.blit(sprite.image, offsetRect)
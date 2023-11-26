import pygame
from settings import *
from pytmx.util_pygame import load_pygame
from helpful import *

class SoilTile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']



class SoilLayer:
    def __init__(self,allSprites):


        # sprite groups
        self.allSprites = allSprites
        self.soilSprites = pygame.sprite.Group()


        # Soil Images
        self.soilSurf = pygame.image.load('../graphics/soil/o.png')

        self.soilSurfaces = importDictFolder('../graphics/soil/')
        # Create grid
        self.createSoilGrid()

        # Create hitboxes
        self.createHitbox()

        # Soil Requirements
        # Is Farmable?

        # Is Watered?

        # Contains Plant?

    def createSoilGrid(self):
        groundImage = pygame.image.load('../graphics/world/ground.png')
        hLength = groundImage.get_width() // TILE_SIZE
        vLength = groundImage.get_height() // TILE_SIZE
        
        self.grid = [  [[] for col in range(hLength)  ] for row in range(vLength) ]
        for x, y, surface in load_pygame('../map/map.tmx').get_layer_by_name('Farmable').tiles():
            self.grid[y][x].append('F')
        


    def createHitbox(self):
        self.hitBoxes = []
        for rowNum,row in enumerate(self.grid):
            for tileNum,tile in enumerate(row):
                if 'F' in tile:
                    x = tileNum * TILE_SIZE
                    y = rowNum * TILE_SIZE
                    hitbox = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                    self.hitBoxes.append(hitbox)

    def getHit(self,hitLocation):
        for rect in self.hitBoxes:
            if rect.collidepoint(hitLocation):
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if 'F' in self.grid[y][x]:
                    self.grid[y][x].append('X')
                    self.createSoilTiles()

    def createSoilTiles(self):
        self.soilSprites.empty()
        for rowNum,row in enumerate(self.grid):
            for tileNum,tile in enumerate(row):
                if 'X' in tile:
                    x = tileNum * TILE_SIZE
                    y = rowNum * TILE_SIZE
                    SoilTile((x,y), self.soilSurf,[self.allSprites,self.soilSprites])





import pygame
from settings import *
from helpful import *
from timer import Timer

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        
        # Creation of groups for the sprites
        super().__init__(group)


        self.importAssets()
        self.status = 'down'
        self.frameIndex = 0



        # basic setting up
        self.image = self.animations[self.status][self.frameIndex]
        self.rect = self.image.get_rect(center = pos)
        # Location for drawing on screen or Z-Location
        self.z = LAYERS['main']

        # player location
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # timers
        self.timers = {
            'toolUse': Timer(350,self.useTool),
            'seedUse': Timer(350,self.useSeed)
        }

        # player tools
        self.tools = ['hoe','axe','water']
        self.toolNum = 0
        self.selectedTool = self.tools[self.toolNum]

        # seeds
        self.seeds = ['corn','tomato']
        self.seedNum = 0
        self.selectedSeed = self.seeds[self.seedNum]

    def importAssets(self):
        self.animations =  {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}


        for animation in self.animations.keys():
            path = '../images/character/' + animation
            self.animations[animation] = importFolder(path)
        


    def animate(self,dt):

        # determine what frame were on for the current index
        self.frameIndex += 4 * dt

        # ensure we dont go over the amount of frames we have for an animation
        if self.frameIndex >= len(self.animations[self.status]):
            self.frameIndex = 0


        self.image = self.animations[self.status][int(self.frameIndex)]
    
    def useTool(self):
        print(self.selectedTool)
    
    def useSeed(self):
        pass


    def input(self):

        if not self.timers['toolUse'].active:
            playerInput = pygame.key.get_pressed()
            # check player input for up or down ('w' 's')
            if playerInput[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif playerInput[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            # check player input for left or right ('a' or 'd')
            if playerInput[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif playerInput[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0


            # If player presses space it will use the active tool
            if playerInput[pygame.K_SPACE]:
                # Create a timer for tool use
                self.timers['toolUse'].activate()
                # Stops the player from moving while using a tool
                self.direction = pygame.math.Vector2()
                self.frameIndex = 0

            # If the player presses e then plant a seed
            if playerInput[pygame.K_e]:
                self.timers['seedUse'].activate()
                self.direction = pygame.math.Vector2()
                self.frameIndex = 0
            # Click buttons 1-3 to change the active tool
            if playerInput[pygame.K_1]:
                self.toolNum = 0
                self.selectedTool = self.tools[self.toolNum]
            elif playerInput[pygame.K_2]:
                self.toolNum = 1
                self.selectedTool = self.tools[self.toolNum]
            elif playerInput[pygame.K_3]:
                self.selectedTool = self.tools[self.toolNum]
                self.toolNum = 2
            # Click 4 or 5 to change the active seed
            if playerInput[pygame.K_4]:
                self.seedNum = 0
                self.selectedSeed = self.seeds[self.seedNum]
            elif playerInput[pygame.K_5]:
                self.seedNum = 1
                self.selectedSeed = self.seeds[self.seedNum]

    
    
    def runTimers(self):
        for timer in self.timers.values():
            timer.update()
    def getStatus(self):
        # Making it so if the player isnt moving then they will play their idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        if self.timers['toolUse'].active:
            self.status = self.status.split('_')[0] + '_' + self.selectedTool



    def move(self,dt):
        
        # Prevent diagonal movement from being faster than just up/down or left/right
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()


        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y


    def update(self,dt):
        self.input()
        self.getStatus()
        self.move(dt)
        self.animate(dt)
        self.runTimers()
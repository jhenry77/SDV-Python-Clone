import pygame
from settings import *

class Overlay:
    def __init__(self,player):


        # Setting things up
        self.displaySurface = pygame.display.get_surface()
        self.player = player


        # importing surfaces
        overlayPath = '../graphics/overlay/'
        # What this does is say that for every tool inside of player tools create a dictionary with the tool being the key and the image with the corresponding path being the value
        self.toolsSurface = {tool: pygame.image.load(f'{overlayPath}{tool}.png').convert_alpha() for tool in player.tools}
        self.seedsSurface = {seed: pygame.image.load(f'{overlayPath}{seed}.png').convert_alpha() for seed in player.seeds}


    def updateDisplay(self):


        # Overlay for current Tool
        toolOverlay = self.toolsSurface[self.player.selectedTool]
        # Gets location of overlay from settings
        toolLocation = toolOverlay.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
        # Draws on to screen
        self.displaySurface.blit(toolOverlay,toolLocation)
        # Overlay for current Seed
        seedOverlay = self.seedsSurface[self.player.selectedSeed]
         # Gets location of overlay from settings
        seedLocation = seedOverlay.get_rect(midbottom = OVERLAY_POSITIONS['seed'])
        # Draws on to screen
        self.displaySurface.blit(seedOverlay,seedLocation)

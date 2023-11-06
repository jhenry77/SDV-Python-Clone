import pygame, sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        # Needed for pygame
        pygame.init()
        # Gets the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        # Sets the clock
        self.clock = pygame.time.Clock()
        # Sets the caption for the game
        pygame.display.set_caption("CropMaster")
        # Creates a level class insid eour game
        self.level = Level()

    def run(self):
        # Game Loop
        while True:
            # Event checker for if we exit the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # Gets delta time
            dt = self.clock.tick() / 1000
            # Runs the level/game
            self.level.run(dt)
            # Updates the display
            pygame.display.update()



if __name__ == '__main__':
    game = Game()
    game.run()
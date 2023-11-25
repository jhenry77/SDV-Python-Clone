import pygame

class Timer:
    def __init__(self, duration, func = None):
        self.duration = duration
        self.func = func
        self.startTime = 0
        self.active = False

    def activate(self):
        self.active = True
        self.startTime = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.startTime = 0

    def update(self):
        currentTime = pygame.time.get_ticks()
        if currentTime - self.startTime >= self.duration:
            if self.func and self.startTime != 0:
                self.func()
            self.deactivate()

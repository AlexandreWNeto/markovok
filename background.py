"""
Tela do jogo

"""


import os, sys
import getopt


import pygame
from pygame.locals import *

images_dir = os.path.join("imagens")

class Background():
    pos = [1,1]
    def __init__(self):
        pass

    def set_screen(self):
        # create display
        pygame.display.set_caption("Markovok")
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        size = [self.SCREEN_WIDTH, self.SCREEN_HEIGHT]
        self.screen = pygame.display.set_mode(size)

        pygame.mouse.set_visible(True)


        # create surface
        self.screen = pygame.display.get_surface()


    def load_image(self,image):
        if isinstance(image,str):
            self.image = os.path.join(images_dir,image)
            self.image = pygame.image.load(self.image).convert()

    def draw( self ):
        self.screen.fill((200,200,200))
        surface = pygame.Surface((500,500))
        surface.fill((0,0,0))
        rect = surface.get_rect()
        surf_center = (
            (self.SCREEN_WIDTH - surface.get_width()) / 2,
            (self.SCREEN_HEIGHT - surface.get_height()) / 2
        )
        self.screen.blit(surface,surf_center)
        pygame.display.flip()


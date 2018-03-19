import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self,ai_settings,screen):
        super(Alien,self).__init__()
        self.ai_settings = ai_settings
        self.screen = screen

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)



    def blitme(self):
        self.screen.blit(self.image,self.rect)

    def check_edges(self):
        screen_right = self.screen.get_rect()
        if screen_right.right <= self.rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False

    def update(self):
        self.x += self.ai_settings.fleet_direction * self.ai_settings.alien_speed_factor
        self.rect.x = self.x

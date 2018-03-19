import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():

    def __init__(self,ai_settings,screen,stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (0,0,0)
        self.font = pygame.font.SysFont(None,36)

        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        round_score = int(round(self.stats.score,-1))

        score_str = "Score:" + "{:,}".format(round_score)
        self.score_image = self.font.render(score_str,True,self.text_color,self.ai_settings.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_level(self):
        level_str = "Level:" + str(self.stats.level)
        self.level_image = self.font.render(level_str,True,self.text_color,self.ai_settings.bg_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 10
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings,self.screen)
            ship.rect.x = ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        self.screen.blit(self.score_image,self.score_rect)
        self.screen.blit(self.level_image,self.level_rect)
        self.ships.draw(self.screen)
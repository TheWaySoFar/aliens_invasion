import pygame

from settings import Settings
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf

def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("Alias Invasion")

    play_button = Button(ai_settings,screen,"Play")
    game_over = Button(ai_settings,screen,"Game Over!",-60)
    game_over.set_button_color((230,230,230))
    game_over.set_text_color((255,0,0))

    ship = Ship(ai_settings,screen)
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)

    while True:

        gf.check_event(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens)
            gf.update_aliens(ai_settings,stats,screen,sb,play_button,ship,aliens,bullets)
        gf.update_screen(ai_settings, screen, stats,ship,aliens,bullets,play_button,game_over,sb)

if __name__ == "__main__":
    run_game()

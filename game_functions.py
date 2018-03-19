import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button

def check_keydown_events(ai_settings,event,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(ai_settings,event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def reset_all(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    ai_settings.init_dynamic_settings()
    stats.reset_stats()
    stats.game_active = True
    stats.game_over = False
    sb.prep_score()
    sb.prep_level()
    sb.prep_ships()
    aliens.empty()
    bullets.empty()
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y):
    if play_button.rect.collidepoint(mouse_x,mouse_y) and not stats.game_active:
        pygame.mouse.set_visible(False)
        reset_all(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)

def check_event(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(ai_settings,event,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(ai_settings,event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets,mouse_x,mouse_y)


def update_screen(ai_setting,screen,stats,ship,aliens,bullets,play_button,game_over,sb):
    screen.fill(ai_setting.bg_color)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if stats.game_over:
        game_over.draw_button()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,bullets,aliens):
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)
    bullets.update()
    check_bullet_alien_collision(ai_settings, screen, stats,sb,ship, aliens, bullets)

def check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()



def shiphit(ai_settings,stats,screen,sb,play_button,ship,aliens,bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        reset_all(ai_settings,screen,stats,sb,play_button,ship,aliens,bullets)
        stats.game_over = True
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_alien_bottom(ai_settings,stats,screen,sb,play_button,ship,aliens,bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if screen_rect.bottom <= alien.rect.bottom:
            shiphit(ai_settings,stats,screen,sb,play_button,ship,aliens,bullets)
            break

def update_aliens(ai_settings,stats,screen,sb,play_button,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)

    if pygame.sprite.spritecollideany(ship,aliens):
        shiphit(ai_settings,stats,screen,sb,play_button,ship,aliens,bullets)
    check_alien_bottom(ai_settings, stats, screen, sb,play_button,ship, aliens, bullets)
    aliens.update()

def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def create_alien(ai_settings,screen,alien_width,aliens,alien_number,row_number):
    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 2 * alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings,ship_rect_height,alien_rect_height):
    available_space_y = ai_settings.screen_height - 4 * alien_rect_height - ship_rect_height
    number_rows = int(available_space_y / (2 * alien_rect_height))
    return number_rows


def create_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings,screen)
    number_alien_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings,screen,alien.rect.width,aliens,alien_number,row_number)

def check_fleet_edges(ai_settings,aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

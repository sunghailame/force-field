#!/usr/bin/env python

import pygame
import random
import os.path

from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(center=(random.randint(820, 900), random.randint(0, 475)))
        self.speed = random.randint(1, 4)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs


pygame.init()

spritex = 50
spritey = 450
screen = pygame.display.set_mode((800, 600))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 700)

player = Player()

# background = pygame.Surface(screen.get_size())

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    bgdtile = load_image('cloudbg-01.png')
    background = pygame.Surface(screen.get_size())
    for x in range(0, 800, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))
    pygame.display.flip()

    screen.blit(player.surf, (spritex, spritey))
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update()
    enemies.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()

    if pressed_keys[pygame.K_UP]:
        spritey -= 5
        if spritey <= 0:
            spritey = 0
    elif pressed_keys[pygame.K_DOWN]:
        spritey += 5
        if spritey >= 475:
            spritey = 475

    pygame.display.flip()
    pygame.display.update()



#!/usr/bin/env python

import pygame
import random
import os.path
import pyganim
# import serial

from pygame.locals import *

main_dir = os.path.split(os.path.abspath(__file__))[0]

spritex = 50
spritey = 450
score = 0
pygame.init()

screen = pygame.display.set_mode((800, 600))

#ser = serial.Serial('COM6')


def maprange(a, b, s):
    (a1, a2), (b1, b2) = a, b
    return b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def load_animation(folder):
    animation = pyganim.PygAnimation(
        [(folder + "/{0:0=3d}.png".format(x), 17) for x in range(1, 300)])
    animation.set_colorkey((0, 0, 0))
    animation.smoothscale((75, 75))
    animation.play()
    return animation


goldfish_animation = load_animation('data/GoldfishAnimation')
raincloud_animation = load_animation('data/RainCloud')


class Player(pygame.sprite.Sprite):
    images = []

    def __init__(self):
        super(Player, self).__init__()
        # self.surf = pygame.Surface((75, 75))
        # self.surf.fill((255, 255, 255))
        self.anim = goldfish_animation
        self.rect = pygame.Rect(0, 0, 75, 75)

    def update(self):
        self.rect.left = spritex
        self.rect.top = spritey


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.transform.scale(
            load_image('ocean-enemy.png').convert_alpha(), (75, 75))
        self.rect = self.surf.get_rect(
            center=(random.randint(820, 900), random.randint(0, 475)))
        self.speed = random.randint(1, 4)
        self.anim = raincloud_animation

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


class Score(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, 30)
        self.font.set_italic(1)
        self.color = Color('black')
        self.lastscore = -1
        self.update()
        self.rect = self.surf.get_rect().move(10, 575)

    def update(self):
        if score != self.lastscore:
            self.lastscore = score
            msg = "Score: %d" % score
            self.surf = self.font.render(msg, 0, self.color)


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit(
            'Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface.convert_alpha()


def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file).convert_alpha())
    return imgs


ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

if pygame.font:
    all_sprites.add(Score())

running = True

#ser.write(b'r')
while running:

    bgdtile = load_image('cloudbg-01.png')
    background = pygame.Surface(screen.get_size())
    for x in range(0, 800, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0, 0))

    #screen.blit(player.surf, player.rect)

    score += 1
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            if random.random() < .45:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    all_sprites.update()

    for entity in all_sprites:
        if (hasattr(entity, 'anim')):
            entity.anim.blit(screen, entity.rect)
        else:
            screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        pygame.quit()
        exit()
    pygame.display.flip()

    min_ir_val = 515
    max_ir_val = 590

#    irvalue = int(ser.readline().decode('ascii'))
#    if irvalue > max_ir_val:
#        irvalue = max_ir_val
#    if irvalue < min_ir_val:
#        irvalue = min_ir_val
#
#    target = maprange((min_ir_val, max_ir_val), (0, 475), irvalue)

#    spritey = (target - spritey) * .15 + spritey
#    ser.write(b'g')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygame, os, sys

TELE1 = (30,4)
ROLL1 = (50,4)
ROLL2 = (256,4)
TELE2 = (276,4)

def load_image(nombre, dir_imagen, alpha=False):
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print "Error, no se puede cargar la imagen: ", ruta
        sys.exit(1)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

class Hud(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        player1 = load_image("player1.png", "sprites/", alpha=True)
        player2 = load_image("player2.png", "sprites/", alpha=True)
        self.empty = load_image("empty.png", "sprites/", alpha=False)
        self.power = load_image("powertransport-inside.png", "sprites/", alpha=False)
        self.image = pygame.Surface([320,24], pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image.blit(player1, (10,4))
        self.image.blit(player2, (296,4))
        self.image.blit(self.empty, TELE1)
        self.image.blit(self.empty, TELE2)

    def putPower(self, player):
        if player == 1:
            self.image.blit(self.power, TELE1)
        elif player == 2:
            self.image.blit(self.power, TELE2)

    def removePower(self, player):
        if player == 1:
            self.image.blit(self.empty, TELE1)
        elif player == 2:
            self.image.blit(self.empty, TELE2)

    def getTime(self, totalSeconds):
        minutes = totalSeconds / 60
        seconds = totalSeconds - minutes*60
        time = "0"+str(minutes)+":"+str(seconds) if seconds > 9 else "0"+str(minutes)+":0"+str(seconds)
        return time

    def draw(self, screen, seconds):
        screen.blit(self.image, (0,0))
        font=pygame.font.Font(None,28)
        time=font.render(self.getTime(seconds), 1,(255,255,255))
        screen.blit(time, (140, 4))


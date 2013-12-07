#!/usr/bin/env python
# -*- coding: utf-8 -*-
  

import pygame, os, sys

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

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

class Tile(pygame.sprite.Sprite):

    def __init__(self, image, hasAlpha, x, y, breakable, crossable):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(image, "sprites/", alpha=hasAlpha)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.isBreakable = breakable
        self.isCrossable = crossable
        self.x, self.y = self.getMapCoordinates(x,y)

    def getMapCoordinates(self, x, y):
        return (x-16)/16,(y-32)/16

    def getSpriteCoordinates(self, x, y):
        return 16+16*x,32+16*y

    def destroy(self):
        self.kill()
        return None

    def position(self, d, pos = 1):
        if d == UP:
            return self.up(pos)
        elif d == RIGHT:
            return self.right(pos)
        elif d == DOWN:
            return self.down(pos)
        elif d == LEFT:
            return self.left(pos)


    def up(self, pos = 1):
        return self.x,self.y-pos

    def right(self, pos = 1):
        return self.x+pos,self.y

    def down(self, pos = 1):
        return self.x,self.y+pos

    def left(self, pos = 1):
        return self.x-pos,self.y

class Block(Tile):
 
    def __init__(self, x, y):
        Tile.__init__(self, "block.png", False, x, y, False, False)

class Brick(Tile):
 
    def __init__(self, x, y, powerup = None):
        Tile.__init__(self, "brick.png", False, x, y, True, False)
        self.powerup = powerup

    def destroy(self):
        self.kill()
        return self.powerup

class Bomberman(Tile):

    def __init__(self, x, y, number):
        Tile.__init__(self, "body%d.png" % (number), True, x, y, True, True)
        self.maxBombs = 1
        self.bombExpansion = 2
        self.bombs = []
        self.insideBomb = None
        self.playerNumber = number

        # Head part
        self.head = load_image("head%d.png" % (number), "sprites/", alpha=True)
        self.rhead = self.head.get_rect()
        self.updateHead()

    def updateHead(self):
        self.rhead.centerx = self.rect.centerx
        self.rhead.y = self.rect.top-13

    def updatePosition(self):
        if self.rect.centerx % 16 < 16/2:
            x = self.rect.centerx - self.rect.centerx % 16
        else:
            x = self.rect.centerx + (16 - self.rect.centerx % 16)
        if self.rect.centery % 16 < 16/2:
            y = self.rect.centery - self.rect.centery % 16
        else:
            y = self.rect.centery + (16 - self.rect.centery % 16)
        self.x, self.y = self.getMapCoordinates(x,y)
        self.updateHead()

    def createBomb(self, time):
        if len(self.bombs) < self.maxBombs:
            x, y = self.getSpriteCoordinates(self.x, self.y)
            b = Bomb(x,y, time, self.bombExpansion, self)
            self.bombs.append(b)
            self.insideBomb = b
            return b

    def removeBomb(self, bomb):
        self.bombs.remove(bomb)


class Bomb(Tile):
    def __init__(self, x, y, time, expansion, player):
        Tile.__init__(self, "bomb.png", True, x, y, True, False)
        self.timer = time
        self.owner = player
        self.expansion = expansion

class Fire(Tile):
    def __init__(self, x, y, time, expansion):
        Tile.__init__(self, "fire.png", True, x, y, False, True)
        self.timer = time
        # Starts from top, right, bottom, left
        self.expansion = [expansion, expansion, expansion, expansion]

class BombPower(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, "powerbomb.png", False, x, y, True, True)

    def activate(self, player):
        player.maxBombs = player.maxBombs + 1

class FirePower(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, "powerfire.png", False, x, y, True, True)

    def activate(self, player):
        player.bombExpansion = player.bombExpansion + 1













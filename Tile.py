﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
  

import pygame, os, sys, random, pyganim

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]

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
        
        self.front_standing = pygame.image.load("sprites/bomber%d/bomber_front.png" % (number))
        self.back_standing = pygame.image.load("sprites/bomber%d/bomber_back.png" % (number))
        self.left_standing = pygame.image.load("sprites/bomber%d/bomber_left.png" % (number))
        self.right_standing = pygame.transform.flip(self.left_standing, True, False)
        self.animTypes = 'back_walk front_walk left_walk'.split()
        self.animObjs = {}
        for animType in self.animTypes:
            imagesAndDurations = [('sprites/bomber%d/bomber_%s.%s.png' % (number,animType, str(num).rjust(3, '0')), 0.1) for num in range(3)]
            self.animObjs[animType] = pyganim.PygAnimation(imagesAndDurations)
        self.animObjs['right_walk'] = self.animObjs['left_walk'].getCopy()
        self.animObjs['right_walk'].flip(True, False)
        self.animObjs['right_walk'].makeTransformsPermanent()
        self.moveConductor = pyganim.PygConductor(self.animObjs)

        self.moving = False
        self.direction = DOWN

        self.number = number
        self.maxBombs = 1
        self.bombExpansion = 2
        self.bombs = []
        self.insideBomb = None
        self.playerNumber = number
        self.speed = 1
        self.transport = False

        # Head part
        self.head = load_image("head%d.png" % (number), "sprites/", alpha=True)
        self.rhead = self.head.get_rect()
        self.updateHead()

    def draw(self, screen):
        if self.moving:
            self.moveConductor.play()
            if self.direction == UP:
                self.animObjs['back_walk'].blit(screen, (self.rect.x, self.rect.y-13))
            elif self.direction == DOWN:
                self.animObjs['front_walk'].blit(screen, (self.rect.x, self.rect.y-13))
            elif self.direction == LEFT:
                self.animObjs['left_walk'].blit(screen, (self.rect.x, self.rect.y-13))
            elif self.direction == RIGHT:
                self.animObjs['right_walk'].blit(screen, (self.rect.x, self.rect.y-13))
        else:
            self.moveConductor.stop()
            if self.direction == UP:
                screen.blit(self.back_standing, (self.rect.x, self.rect.y-13))
            elif self.direction == DOWN:
                screen.blit(self.front_standing, (self.rect.x, self.rect.y-13))
            elif self.direction == LEFT:
                screen.blit(self.left_standing, (self.rect.x, self.rect.y-13))
            elif self.direction == RIGHT:
                screen.blit(self.right_standing, (self.rect.x, self.rect.y-13))


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

        self.bombAnim = pyganim.PygAnimation([('sprites/bomb.png', 0.2),
                                         ('sprites/bomb1.png', 0.2),
                                         ('sprites/bomb2.png', 0.2)])
        self.bombAnim.play()

    def draw(self, screen):
        self.bombAnim.blit(screen, (self.rect.x, self.rect.y))

class Fire(Tile):
    def __init__(self, x, y, time, expansion):
        Tile.__init__(self, "fire/fire.png", True, x, y, False, True)
        self.timer = time
        # Starts from top, right, bottom, left
        self.max_expansion = expansion
        self.expansion = [expansion, expansion, expansion, expansion]

        width = height = 16*(2*expansion+1)
        self.image = pygame.Surface([width,height], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def getFirePosition(self, direction, pos):
        if direction == UP:
            return (self.max_expansion*16,(self.max_expansion-pos)*16)
        if direction == RIGHT:
            return ((self.max_expansion+pos)*16,self.max_expansion*16)
        if direction == DOWN:
            return (self.max_expansion*16,(self.max_expansion+pos)*16)
        if direction == LEFT:
            return ((self.max_expansion-pos)*16,self.max_expansion*16)

    def updateSprite(self):
        center = load_image("fire-center.png", "sprites/fire", alpha=True)
        self.image.blit(center, (self.max_expansion*16,self.max_expansion*16))

        fireTypes = 'up right down left'.split()
        for direction in DIRECTIONS:
            fire_image = load_image('fire-%s.png' % fireTypes[direction], "sprites/fire", alpha=True)
            fire_end = load_image('fire-%s-end.png' % fireTypes[direction], "sprites/fire", alpha=True)
            for pos in range(1, self.expansion[direction]+1):
                if pos < self.max_expansion:
                    self.image.blit(fire_image, self.getFirePosition(direction, pos))
                else:
                    self.image.blit(fire_end, self.getFirePosition(direction, pos))

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

class SpeedPower(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, "powerspeed.png", False, x, y, True, True)

    def activate(self, player):
        if player.speed == 1:
            player.speed = 2

class TransportPower(Tile):
    def __init__(self, x, y):
        Tile.__init__(self, "powertransport.png", False, x, y, True, True)

    def activate(self, player):
        player.transport = True










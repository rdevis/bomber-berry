#!/usr/bin/env python
# -*- coding: utf-8 -*-
  
# ---------------------------
# Importacion de los módulos
# ---------------------------
 
import pygame
from pygame.locals import *
import os, sys, random, math
 
# -----------
# Constantes
# -----------

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
BLOCK_SIZE = 16
FPS = 30
BOMB_TIME = 2
 
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
 
def texts(text, x, y):
   font=pygame.font.Font(None,30)
   scoretext=font.render(text, 1,(255,255,255))
   screen.blit(scoretext, (x, y))
 
def load_image(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print "Error, no se puede cargar la imagen: ", ruta
        sys.exit(1)
    # Comprobar si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image
 
 
# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:
 
class Game():
    def __init__(self):
        self.score = 0
        self.player = Bomberman(32,48)
        self.blocks = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.createMap()

    def createMap(self):
        for x in range(0,19):
            for y in range(0,13):
                # Bloques bordeantes
                if x == 0 or y == 0 or x == 18 or y == 12:
                    self.blocks.add(Block(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y))
                # Bloques internos
                elif y % 2 == 0 and x % 2 == 0:
                    self.blocks.add(Block(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y))
                # Ladrillos al azar
                elif random.randint(1,10) == 5 and (x > 3 or y > 3):
                    self.bricks.add(Brick(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y))

    def drawGame(self, screen):
        for bomb in self.bombs:
            bomb.timer -= 1
            if bomb.timer <= 0:
                self.fires.add(Fire(bomb.rect.centerx, bomb.rect.centery))
                bomb.kill()
        for fire in self.fires:
            fire.timer -= 1
            if fire.timer <= 0:
                fire.kill()

        collisions=pygame.sprite.groupcollide(self.fires,self.bricks,False,True)

        screen.fill((16,120,48))
        self.blocks.draw(screen); self.bricks.draw(screen); self.bombs.draw(screen)
        self.fires.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        screen.blit(self.player.head, self.player.rhead)
        pygame.display.flip()

    def putBomb(self):
        if len(self.bombs) < self.player.max_bombs:
            x = 0; y = 0
            if self.player.rect.centerx % BLOCK_SIZE < BLOCK_SIZE/2:
                x = self.player.rect.centerx - self.player.rect.centerx % BLOCK_SIZE
            else:
                x = self.player.rect.centerx + (BLOCK_SIZE - self.player.rect.centerx % BLOCK_SIZE)
            if self.player.rect.centery % BLOCK_SIZE < BLOCK_SIZE/2:
                y = self.player.rect.centery - self.player.rect.centery % BLOCK_SIZE
            else:
                y = self.player.rect.centery + (BLOCK_SIZE - self.player.rect.centery % BLOCK_SIZE)
            self.bombs.add(Bomb(x,y))

    def movePlayer(self, dx, dy):
        self.player.rect.centerx += dx
        self.player.rect.centery += dy

        for block in self.blocks:
            if self.player.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    self.player.rect.right = block.rect.left
                if dx < 0: # Moving left; Hit the right side of the block
                    self.player.rect.left = block.rect.right
                if dy > 0: # Moving down; Hit the top side of the block
                    self.player.rect.bottom = block.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the block
                    self.player.rect.top = block.rect.bottom

        for brick in self.bricks:
            if self.player.rect.colliderect(brick.rect):
                if dx > 0: # Moving right; Hit the left side of the brick
                    self.player.rect.right = brick.rect.left
                if dx < 0: # Moving left; Hit the right side of the brick
                    self.player.rect.left = brick.rect.right
                if dy > 0: # Moving down; Hit the top side of the brick
                    self.player.rect.bottom = brick.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the brick
                    self.player.rect.top = brick.rect.bottom

        self.player.rhead.centerx = self.player.rect.centerx
        self.player.rhead.y = self.player.rect.top-13
 
class Block(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("block.png", "sprites/", alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Brick(pygame.sprite.Sprite):
 
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("brick.png", "sprites/", alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Bomberman(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.max_bombs = 1
        self.image = load_image("body.png", "sprites/", alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

        # Head part
        self.head = load_image("head.png", "sprites/", alpha=True)
        self.rhead = self.head.get_rect()
        self.rhead.centerx = self.rect.centerx
        self.rhead.y = self.rect.top-13

class Bomb(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bomb.png", "sprites/", alpha=True)
        self.timer = FPS*BOMB_TIME
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("fire.png", "sprites/", alpha=True)
        self.timer = FPS*1
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

# ------------------------------
# Funcion principal del juego
# ------------------------------
 
 
def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BomberPi")
 
    # cargamos los objetos
    game = Game()
 
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 15)
 
    # el bucle principal del juego
    while True:
        clock.tick(FPS)
        
        # Posibles entradas del teclado
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            sys.exit(0)

        if keys[K_DOWN]:
            game.movePlayer(0,4)
        if keys[K_UP]:
            game.movePlayer(0,-4)
        if keys[K_RIGHT]:
            game.movePlayer(4,0)
        if keys[K_LEFT]:
            game.movePlayer(-4,0)
        if keys[K_LCTRL] or keys[K_RCTRL]:
            game.putBomb()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # actualizamos la pantalla
        game.drawGame(screen)
 
if __name__ == "__main__":
    main()

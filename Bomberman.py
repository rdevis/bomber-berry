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

blocks = pygame.sprite.Group() 
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
BLOCK_SIZE = 16
 
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
 
class Juego():
    def __init__(self):
        self.puntos = 0
 
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

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("body.png", "sprites/", alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = 32
        self.rect.centery = 48

        # Head part
        self.head = load_image("head.png", "sprites/", alpha=True)
        self.rhead = self.head.get_rect()
        self.rhead.centerx = self.rect.centerx
        self.rhead.y = self.rect.top-13

    def moveMe(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

        for block in blocks:
            if self.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    self.rect.right = block.rect.left
                if dx < 0: # Moving left; Hit the right side of the block
                    self.rect.left = block.rect.right
                if dy > 0: # Moving down; Hit the top side of the block
                    self.rect.bottom = block.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the block
                    self.rect.top = block.rect.bottom

        self.rhead.centerx = self.rect.centerx
        self.rhead.y = self.rect.top-13

# ------------------------------
# Funcion principal del juego
# ------------------------------
 
 
def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("BomberPi")
 
    # cargamos los objetos
    juego = Juego()
    #blocks = pygame.sprite.Group()
    bricks = pygame.sprite.Group()
    bomberman = Bomberman()
    for x in range(0,19):
        for y in range(0,13):
            # Bloques bordeantes
            if x == 0 or y == 0 or x == 18 or y == 12:
                blocks.add(Block(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y))
            # Bloques internos
            elif y % 2 == 0 and x % 2 == 0:
                blocks.add(Block(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y))
            # Ladrillos al azar
            elif random.randint(1,10) == 5 and (x > 3 or y > 3):
                bricks.add(Brick(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y))
 
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 15)
 
    # el bucle principal del juego
    while True:
        clock.tick(30)
        
        # Posibles entradas del teclado
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            sys.exit(0)

        if keys[K_DOWN]:
            bomberman.moveMe(0,4)
        if keys[K_UP]:
            bomberman.moveMe(0,-4)
        if keys[K_RIGHT]:
            bomberman.moveMe(4,0)
        if keys[K_LEFT]:
            bomberman.moveMe(-4,0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # actualizamos la pantalla
        #screen.blit(fondo, (0, 0))
        screen.fill((16,120,48))
        blocks.draw(screen); bricks.draw(screen)
        screen.blit(bomberman.image, bomberman.rect)
        screen.blit(bomberman.head, bomberman.rhead)
        pygame.display.flip()
 
if __name__ == "__main__":
    main()

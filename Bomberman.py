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
BOMB_TIME = 3
 
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
        self.player = Bomberman(32,48, False)
        self.player2 = Bomberman(288,208, True)

        self.blocks = pygame.sprite.Group()
        self.bricks = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.bombs2 = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        #self.matrix = [[0 for x in xrange(19)] for x in xrange(13)]
        self.matrix = [[0]*50 for i in range(50)]
        self.createMap()

    def createMap(self):
        for x in range(0,19):
            for y in range(0,13):
                # Bloques bordeantes
                if x == 0 or y == 0 or x == 18 or y == 12:
                    b = Block(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y)
                    self.blocks.add(b)
                    self.matrix[x][y] = b
                # Bloques internos
                elif y % 2 == 0 and x % 2 == 0:
                    b = Block(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y)
                    self.blocks.add(b)
                    self.matrix[x][y] = b
                # Ladrillos al azar
                elif random.randint(1,10) == 5 and (x > 3 or y > 3):
                    b = Brick(BLOCK_SIZE+x*BLOCK_SIZE,32+BLOCK_SIZE*y)
                    self.bricks.add(b)
                    self.matrix[x][y] = b

    def drawGame(self, screen):

        for bomb in self.bombs:
            bomb.timer -= 1
            if bomb.timer <= 0:
                self.fires.add(Fire(bomb.rect.centerx, bomb.rect.centery))
                bomb.kill()
        for bomb in self.bombs2:
            bomb.timer -= 1
            if bomb.timer <= 0:
                self.fires.add(Fire(bomb.rect.centerx, bomb.rect.centery))
                bomb.kill()
        for fire in self.fires:
            fire.timer -= 1
            if fire.timer <= 0:
                fire.kill()

        #Calcula colisiones fuego
        for fire in self.fires:
            if self.matrix[fire.x+1][fire.y].__class__.__name__ == "Brick":
                self.matrix[fire.x+1][fire.y].kill()
            elif self.matrix[fire.x+1][fire.y].__class__.__name__ != "Block":
                if self.matrix[fire.x+2][fire.y].__class__.__name__ == "Brick":
                    self.matrix[fire.x+2][fire.y].kill()

            if self.matrix[fire.x-1][fire.y].__class__.__name__ == "Brick":
                self.matrix[fire.x-1][fire.y].kill()
            elif self.matrix[fire.x-1][fire.y].__class__.__name__ != "Block":
                if self.matrix[fire.x-2][fire.y].__class__.__name__ == "Brick":
                    self.matrix[fire.x-2][fire.y].kill()

            if self.matrix[fire.x][fire.y+1].__class__.__name__ == "Brick":
                self.matrix[fire.x][fire.y+1].kill()
            elif self.matrix[fire.x][fire.y+1].__class__.__name__ != "Block":
                if self.matrix[fire.x][fire.y+2].__class__.__name__ == "Brick":
                    self.matrix[fire.x][fire.y+2].kill()

            if self.matrix[fire.x][fire.y-1].__class__.__name__ == "Brick":
                self.matrix[fire.x][fire.y-1].kill()
            elif self.matrix[fire.x][fire.y-1].__class__.__name__ != "Block":
                if self.matrix[fire.x][fire.y-2].__class__.__name__ == "Brick":
                    self.matrix[fire.x][fire.y-2].kill()

            #Colisiones con jugadores
            if fire.x+1 == self.player.x or fire.x-1 == self.player.x or fire.y+1 == self.player.y or fire.y-1 == self.player.y:
                sys.exit(0)
                            

        screen.fill((16,120,48))
        self.blocks.draw(screen); self.bricks.draw(screen); 
        self.bombs.draw(screen); self.bombs2.draw(screen)
        self.fires.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        screen.blit(self.player.head, self.player.rhead)
        screen.blit(self.player2.image, self.player2.rect)
        screen.blit(self.player2.head, self.player2.rhead)
        pygame.display.flip()

    def putBomb(self, player):
        n_bombs = len(self.bombs) if player.isPlayer2 == False else len(self.bombs2)

        if n_bombs < player.max_bombs:
            x = 0; y = 0
            if player.rect.centerx % BLOCK_SIZE < BLOCK_SIZE/2:
                x = player.rect.centerx - player.rect.centerx % BLOCK_SIZE
            else:
                x = player.rect.centerx + (BLOCK_SIZE - player.rect.centerx % BLOCK_SIZE)
            if player.rect.centery % BLOCK_SIZE < BLOCK_SIZE/2:
                y = player.rect.centery - player.rect.centery % BLOCK_SIZE
            else:
                y = player.rect.centery + (BLOCK_SIZE - player.rect.centery % BLOCK_SIZE)

            if player.isPlayer2 == False:
                self.bombs.add(Bomb(x,y))
            else:
                self.bombs2.add(Bomb(x,y))

    def movePlayer(self, player, dx, dy):
        player.rect.centerx += dx
        player.rect.centery += dy

        for block in self.blocks:
            if player.rect.colliderect(block.rect):
                if dx > 0: # Moving right; Hit the left side of the block
                    player.rect.right = block.rect.left
                if dx < 0: # Moving left; Hit the right side of the block
                    player.rect.left = block.rect.right
                if dy > 0: # Moving down; Hit the top side of the block
                    player.rect.bottom = block.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the block
                    player.rect.top = block.rect.bottom

        for brick in self.bricks:
            if player.rect.colliderect(brick.rect):
                if dx > 0: # Moving right; Hit the left side of the brick
                    player.rect.right = brick.rect.left
                if dx < 0: # Moving left; Hit the right side of the brick
                    player.rect.left = brick.rect.right
                if dy > 0: # Moving down; Hit the top side of the brick
                    player.rect.bottom = brick.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the brick
                    player.rect.top = brick.rect.bottom

        player.rhead.centerx = player.rect.centerx
        player.rhead.y = player.rect.top-13
        player.updatePosition()

class Tile(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.breakable = False
        self.passable = False

class Block(Tile):
 
    def __init__(self, x, y):
        Tile.__init__(self)
        self.image = load_image("block.png", "sprites/", alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Brick(Tile):
 
    def __init__(self, x, y):
        Tile.__init__(self)
        self.image = load_image("brick.png", "sprites/", alpha=False)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.breakable = True

class Bomberman(Tile):

    def __init__(self, x, y, isPlayer2):
        Tile.__init__(self)
        self.max_bombs = 1
        if isPlayer2 == False:
            self.image = load_image("body.png", "sprites/", alpha=True)
        else:
            self.image = load_image("body2.png", "sprites/", alpha=True)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.breakable = True
        self.passable = True
        if isPlayer2 == False:
            self.x = 1
            self.y = 1
        else:
            self.x = 17
            self.y = 11
        self.isPlayer2 = isPlayer2

        # Head part
        if isPlayer2 == False:
            self.head = load_image("head.png", "sprites/", alpha=True)
        else:
            self.head = load_image("head2.png", "sprites/", alpha=True)
        self.rhead = self.head.get_rect()
        self.rhead.centerx = self.rect.centerx
        self.rhead.y = self.rect.top-13

    def updatePosition(self):
        if self.rect.centerx % BLOCK_SIZE < BLOCK_SIZE/2:
            pos = self.rect.centerx - self.rect.centerx % BLOCK_SIZE
            self.x = (pos - 16) / 16
        else:
            pos = self.rect.centerx + (BLOCK_SIZE - self.rect.centerx % BLOCK_SIZE)
            self.x = (pos - 16) / 16
        if self.rect.centery % BLOCK_SIZE < BLOCK_SIZE/2:
            pos = self.rect.centery - self.rect.centery % BLOCK_SIZE
            self.y = (pos - 32) / 16
        else:
            pos = self.rect.centery + (BLOCK_SIZE - self.rect.centery % BLOCK_SIZE)
            self.y = (pos - 32) / 16

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Tile.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("bomb.png", "sprites/", alpha=True)
        self.timer = FPS*BOMB_TIME
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = (x-16)/16
        self.y = (y-32)/16

class Fire(pygame.sprite.Sprite):
    def __init__(self, x, y):
        #Tile.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("fire.png", "sprites/", alpha=True)
        self.timer = FPS*1
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.x = (x-16)/16
        self.y = (y-32)/16

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

        # Control del jugador 1
        if keys[K_DOWN]:
            game.movePlayer(game.player,0,4)
        if keys[K_UP]:
            game.movePlayer(game.player,0,-4)
        if keys[K_RIGHT]:
            game.movePlayer(game.player,4,0)
        if keys[K_LEFT]:
            game.movePlayer(game.player,-4,0)
        if keys[K_RCTRL]:
            game.putBomb(game.player)

        # Control del jugador 2
        if keys[K_s]:
            game.movePlayer(game.player2,0,4)
        if keys[K_w]:
            game.movePlayer(game.player2,0,-4)
        if keys[K_d]:
            game.movePlayer(game.player2,4,0)
        if keys[K_a]:
            game.movePlayer(game.player2,-4,0)
        if keys[K_LCTRL]:
            game.putBomb(game.player2)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        # actualizamos la pantalla
        game.drawGame(screen)
 
if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
  
# ---------------------------
# Importacion de los módulos
# ---------------------------
 
import pygame
from pygame.locals import *
import os, sys, random, math, time
import serial
 
# -----------
# Constantes
# -----------

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
BLOCK_SIZE = 16
FPS = 30
BOMB_TIME = 3

PlayController = {"PS1_CUADRADO":False, "PS1_TRIANGULO":False, "PS1_CIRCULO":False, "PS1_EQUIS":False, "PS1_ARRIBA":False, "PS1_ABAJO":False, "PS1_IZQUIERDA":False, "PS1_DERECHA":False, "PS1_L1":False, "PS1_R1":False, "PS1_L2":False, "PS1_R2":False, "PS1_L3":False, "PS1_R3":False, "PS1_START":False, "PS1_SELECT":False, "PS1_JLARRIBA":False, "PS1_JLABAJO":False, "PS1_JLIZQUIERDA":False, "PS1_JLDERECHA":False, "PS1_JRARRIBA":False, "PS1_JRABAJO":False, "PS1_JRIZQUIERDA":False, "PS1_JRDERECHA":False, "PS2_CUADRADO":False, "PS2_TRIANGULO":False, "PS2_CIRCULO":False, "PS2_EQUIS":False, "PS2_ARRIBA":False, "PS2_ABAJO":False, "PS2_IZQUIERDA":False, "PS2_DERECHA":False, "PS2_L1":False, "PS2_R1":False, "PS2_L2":False, "PS2_R2":False, "PS2_L3":False, "PS2_R3":False, "PS2_START":False, "PS2_SELECT":False, "PS2_JLARRIBA":False, "PS2_JLABAJO":False, "PS2_JLIZQUIERDA":False, "PS2_JLDERECHA":False, "PS2_JRARRIBA":False, "PS2_JRABAJO":False, "PS2_JRIZQUIERDA":False, "PS2_JRDERECHA":False}

port = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=3.0)
 
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
 
def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv
    
def keysPS():
    salida = {"PS1_CUADRADO":False, "PS1_TRIANGULO":False, "PS1_CIRCULO":False, "PS1_EQUIS":False, "PS1_ARRIBA":False, "PS1_ABAJO":False, "PS1_IZQUIERDA":False, "PS1_DERECHA":False, "PS1_L1":False, "PS1_R1":False, "PS1_L2":False, "PS1_R2":False, "PS1_L3":False, "PS1_R3":False, "PS1_START":False, "PS1_SELECT":False, "PS1_JLARRIBA":False, "PS1_JLABAJO":False, "PS1_JLIZQUIERDA":False, "PS1_JLDERECHA":False, "PS1_JRARRIBA":False, "PS1_JRABAJO":False, "PS1_JRIZQUIERDA":False, "PS1_JRDERECHA":False, "PS2_CUADRADO":False, "PS2_TRIANGULO":False, "PS2_CIRCULO":False, "PS2_EQUIS":False, "PS2_ARRIBA":False, "PS2_ABAJO":False, "PS2_IZQUIERDA":False, "PS2_DERECHA":False, "PS2_L1":False, "PS2_R1":False, "PS2_L2":False, "PS2_R2":False, "PS2_L3":False, "PS2_R3":False, "PS2_START":False, "PS2_SELECT":False, "PS2_JLARRIBA":False, "PS2_JLABAJO":False, "PS2_JLIZQUIERDA":False, "PS2_JLDERECHA":False, "PS2_JRARRIBA":False, "PS2_JRABAJO":False, "PS2_JRIZQUIERDA":False, "PS2_JRDERECHA":False}
        while port.inWaiting() > 0:
            rcv = readlineCR(port)
            if rcv == ";1CU:\r":
                salida["PS1_CUADRADO"]=True
            elif rcv == ";1TR:\r":
                salida["PS1_TRIANGULO"]=True
            elif rcv == ";1CI:\r":
                salida["PS1_CIRCULO"]=True
            elif rcv == ";1EQ:\r":
                salida["PS1_EQUIS"]=True
            elif rcv == ";1AR:\r":
                salida["PS1_ARRIBA"]=True
            elif rcv == ";1AB:\r":
                salida["PS1_ABAJO"]=True
            elif rcv == ";1IZ:\r":
                salida["PS1_IZQUIERDA"]=True
            elif rcv == ";1DE:\r":
                salida["PS1_DERECHA"]=True
            elif rcv == ";1L1:\r":
                salida["PS1_L1"]=True
            elif rcv == ";1R1:\r":
                salida["PS1_R1"]=True
            elif rcv == ";1L2:\r":
                salida["PS1_L2"]=True
            elif rcv == ";1R2:\r":
                salida["PS1_R2"]=True
            elif rcv == ";1L3:\r":
                salida["PS1_L3"]=True
            elif rcv == ";1R3:\r":
                salida["PS1_R3"]=True
            elif rcv == ";1ST:\r":
                salida["PS1_START"]=True
            elif rcv == ";1SE:\r":
                salida["PS1_SELECT"]=True
            elif rcv == ";1LU:\r":
                salida["PS1_JLARRIBA"]=True
            elif rcv == ";1LD:\r":
                salida["PS1_JLABAJO"]=True
            elif rcv == ";1LL:\r":
                salida["PS1_JLIZQUIERDA"]=True
            elif rcv == ";1LR:\r":
                salida["PS1_JLDERECHA"]=True
            elif rcv == ";1RU:\r":
                salida["PS1_JRARRIBA"]=True
            elif rcv == ";1RD:\r":
                salida["PS1_JRABAJO"]=True
            elif rcv == ";1RL:\r":
                salida["PS1_JRIZQUIERDA"]=True
            elif rcv == ";1RR:\r":
                salida["PS1_JRDERECHA"]=True
            elif rcv == ";2CU:\r":
                salida["PS2_CUADRADO"]=True
            elif rcv == ";2TR:\r":
                salida["PS2_TRIANGULO"]=True
            elif rcv == ";2CI:\r":
                salida["PS2_CIRCULO"]=True
            elif rcv == ";2EQ:\r":
                salida["PS2_EQUIS"]=True
            elif rcv == ";2AR:\r":
                salida["PS2_ARRIBA"]=True
            elif rcv == ";2AB:\r":
                salida["PS2_ABAJO"]=True
            elif rcv == ";2IZ:\r":
                salida["PS2_IZQUIERDA"]=True
            elif rcv == ";2DE:\r":
                salida["PS2_DERECHA"]=True
            elif rcv == ";2L1:\r":
                salida["PS2_L1"]=True
            elif rcv == ";2R1:\r":
                salida["PS2_R1"]=True
            elif rcv == ";2L2:\r":
                salida["PS2_L2"]=True
            elif rcv == ";2R2:\r":
                salida["PS2_R2"]=True
            elif rcv == ";2L3:\r":
                salida["PS2_L3"]=True
            elif rcv == ";2R3:\r":
                salida["PS2_R3"]=True
            elif rcv == ";2ST:\r":
                salida["PS2_START"]=True
            elif rcv == ";2SE:\r":
                salida["PS2_SELECT"]=True
            elif rcv == ";2LU:\r":
                salida["PS2_JLARRIBA"]=True
            elif rcv == ";2LD:\r":
                salida["PS2_JLABAJO"]=True
            elif rcv == ";2LL:\r":
                salida["PS2_JLIZQUIERDA"]=True
            elif rcv == ";2LR:\r":
                salida["PS2_JLDERECHA"]=True
            elif rcv == ";2RU:\r":
                salida["PS2_JRARRIBA"]=True
            elif rcv == ";2RD:\r":
                salida["PS2_JRABAJO"]=True
            elif rcv == ";2RL:\r":
                salida["PS2_JRIZQUIERDA"]=True
            elif rcv == ";2RR:\r":
                salida["PS2_JRDERECHA"]=True
        port.write(";1RE:")
        port.write(";2RE:")
        return salida
 
# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:
 
class Game():
    def __init__(self):
        self.score = 0
        self.player = Bomberman(32,48, False)
        self.player2 = Bomberman(288,208, True)
        self.players = [self.player, self.player2]

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
                elif random.randint(1,10) == 5 and (x > 2 or y > 2) and (x < 16 or y < 10):
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

        #Calcula colisiones fuego
        for fire in self.fires:
            if self.matrix[fire.x+1][fire.y].__class__.__name__ == "Brick":
                self.matrix[fire.x+1][fire.y].kill()
                if fire.timer == 0:
                    self.matrix[fire.x+1][fire.y] = 0
            elif self.matrix[fire.x+1][fire.y].__class__.__name__ != "Block":
                if self.matrix[fire.x+2][fire.y].__class__.__name__ == "Brick":
                    self.matrix[fire.x+2][fire.y].kill()
                    if fire.timer == 0:
                        self.matrix[fire.x+2][fire.y] = 0

            if self.matrix[fire.x-1][fire.y].__class__.__name__ == "Brick":
                self.matrix[fire.x-1][fire.y].kill()
                if fire.timer == 0:
                    self.matrix[fire.x-1][fire.y] = 0
            elif self.matrix[fire.x-1][fire.y].__class__.__name__ != "Block":
                if self.matrix[fire.x-2][fire.y].__class__.__name__ == "Brick":
                    self.matrix[fire.x-2][fire.y].kill()
                    if fire.timer == 0:
                        self.matrix[fire.x-2][fire.y] = 0

            if self.matrix[fire.x][fire.y+1].__class__.__name__ == "Brick":
                self.matrix[fire.x][fire.y+1].kill()
                if fire.timer == 0:
                    self.matrix[fire.x][fire.y+1] = 0
            elif self.matrix[fire.x][fire.y+1].__class__.__name__ != "Block":
                if self.matrix[fire.x][fire.y+2].__class__.__name__ == "Brick":
                    self.matrix[fire.x][fire.y+2].kill()
                    if fire.timer == 0:
                        self.matrix[fire.x][fire.y+2] = 0

            if self.matrix[fire.x][fire.y-1].__class__.__name__ == "Brick":
                self.matrix[fire.x][fire.y-1].kill()
                if fire.timer == 0:
                    self.matrix[fire.x][fire.y-1] = 0
            elif self.matrix[fire.x][fire.y-1].__class__.__name__ != "Block":
                if self.matrix[fire.x][fire.y-2].__class__.__name__ == "Brick":
                    self.matrix[fire.x][fire.y-2].kill()
                    if fire.timer == 0:
                        self.matrix[fire.x][fire.y-2] = 0

            #Colisiones con jugadores
            if fire.timer > 0:
                for player in self.players:
                    if fire.x+1 == player.x and fire.y == player.y:
                        sys.exit(0)
                    if self.matrix[fire.x+1][fire.y].__class__.__bases__[0].__name__ != "Tile":
                        if fire.x+2 == player.x and fire.y == player.y:
                            sys.exit(0)

                    if fire.x-1 == player.x and fire.y == player.y:
                        sys.exit(0)
                    if self.matrix[fire.x-1][fire.y].__class__.__bases__[0].__name__ != "Tile":
                        if fire.x-2 == player.x and fire.y == player.y:
                            sys.exit(0)

                    if fire.y+1 == player.y and fire.x == player.x:
                        sys.exit(0)
                    if self.matrix[fire.x][fire.y+1].__class__.__bases__[0].__name__ != "Tile":
                        if fire.x == player.x and fire.y+2 == player.y:
                            sys.exit(0)

                    if fire.y-1 == player.y and fire.x == player.x:
                        sys.exit(0)
                    if self.matrix[fire.x][fire.y-1].__class__.__bases__[0].__name__ != "Tile":
                        if fire.x == player.x and fire.y-2 == player.y:
                            sys.exit(0)

            if fire.timer <= 0:
                fire.kill()
                            

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
            player.insideBomb = True

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

        if player.insideBomb == False:
            for bomb in self.bombs:
                if player.rect.colliderect(bomb.rect):
                    if dx > 0: # Moving right; Hit the left side of the bomb
                        player.rect.right = bomb.rect.left
                    if dx < 0: # Moving left; Hit the right side of the bomb
                        player.rect.left = bomb.rect.right
                    if dy > 0: # Moving down; Hit the top side of the bomb
                        player.rect.bottom = bomb.rect.top
                    if dy < 0: # Moving up; Hit the bottom side of the bomb
                        player.rect.top = bomb.rect.bottom
            for bomb in self.bombs2:
                if player.rect.colliderect(bomb.rect):
                    if dx > 0: # Moving right; Hit the left side of the bomb
                        player.rect.right = bomb.rect.left
                    if dx < 0: # Moving left; Hit the right side of the bomb
                        player.rect.left = bomb.rect.right
                    if dy > 0: # Moving down; Hit the top side of the bomb
                        player.rect.bottom = bomb.rect.top
                    if dy < 0: # Moving up; Hit the bottom side of the bomb
                        player.rect.top = bomb.rect.bottom

        player.rhead.centerx = player.rect.centerx
        player.rhead.y = player.rect.top-13

        bombaActual = 0
        for bomb in self.bombs:
            if player.rect.colliderect(bomb.rect):
                bombaActual = bomb
        for bomb in self.bombs2:
            if player.rect.colliderect(bomb.rect):
                bombaActual = bomb
        player.updatePosition(bombaActual)

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
        self.insideBomb = False

        # Head part
        if isPlayer2 == False:
            self.head = load_image("head.png", "sprites/", alpha=True)
        else:
            self.head = load_image("head2.png", "sprites/", alpha=True)
        self.rhead = self.head.get_rect()
        self.rhead.centerx = self.rect.centerx
        self.rhead.y = self.rect.top-13

    def updatePosition(self, bomb):
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
        if self.insideBomb == True and bomb == 0:
            self.insideBomb = False


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
        PlayController = keysPS()
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

        if PlayController["PS1_ABAJO"] or PlayController["PS1_JLABAJO"]:
            game.movePlayer(game.player,0,4)
        if PlayController["PS1_ARRIBA"] or PlayController["PS1_JLARRIBA"]:
            game.movePlayer(game.player,0,-4)
        if PlayController["PS1_DERECHA"] or PlayController["PS1_JLDERECHA"]:
            game.movePlayer(game.player,4,0)
        if PlayController["PS1_IZQUIERDA"] or PlayController["PS1_JLIZQUIERDA"]:
            game.movePlayer(game.player,-4,0)
        if PlayController["PS1_EQUIS"]:
            game.putBomb(game.player)

        if PlayController["PS2_ABAJO"] or PlayController["PS2_JLABAJO"]:
            game.movePlayer(game.player2,0,4)
        if PlayController["PS2_ARRIBA"] or PlayController["PS2_JLARRIBA"]:
            game.movePlayer(game.player2,0,-4)
        if PlayController["PS2_DERECHA"] or PlayController["PS2_JLDERECHA"]:
            game.movePlayer(game.player2,4,0)
        if PlayController["PS2_IZQUIERDA"] or PlayController["PS2_JLIZQUIERDA"]:
            game.movePlayer(game.player2,-4,0)
        if PlayController["PS2_EQUIS"]:
            game.putBomb(game.player2)

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

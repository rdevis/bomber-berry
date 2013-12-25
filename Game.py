#!/usr/bin/env python
# -*- coding: utf-8 -*-
  
# ---------------------------
# Importacion de los módulos
# ---------------------------

SERIAL = True
 
import pygame, datetime, Tweet
from pygame.locals import *
import Tile, Hud, os, sys, random, math, time
if SERIAL:
    import Serial
 
# -----------
# Constantes
# -----------

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
FPS = 30
BOMB_TIME = 3
TIME_LIMIT = 90

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
DIRECTIONS = [UP, RIGHT, DOWN, LEFT]
 
# ------------------------------
# Clases y Funciones utilizadas
# ------------------------------
 
def texts(text, x, y):
   font=pygame.font.Font(None,30)
   scoretext=font.render(text, 1,(255,255,255))
   screen.blit(scoretext, (x, y))
 
# -----------------------------------------------
# Creamos los sprites (clases) de los objetos del juego:
 
class Game():
    def __init__(self):
        self.score = 0
        self.player = Tile.Bomberman(32,48,1)
        self.player2 = Tile.Bomberman(288,208,2)
        self.players = [self.player, self.player2]

        self.hud = Hud.Hud()
        self.tiles = pygame.sprite.Group()
        self.bombs = pygame.sprite.Group()
        self.fires = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.win = None

        self.map = [[None]*13 for i in range(19)]
        self.createMap()

        self.tock = 0

    def timeLeft(self):
        return TIME_LIMIT-self.tock/FPS

    def timer(self):
        minutes = self.timeLeft() / 60
        seconds = self.timeLeft() - minutes*60
        time = "0"+str(minutes)+":"+str(seconds) if seconds > 9 else "0"+str(minutes)+":0"+str(seconds)
        return time

    def startGame(self, screen):
        clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 15)
        while self.win is None and self.timeLeft() >= 0:
            clock.tick(FPS)
            self.checkEvents()
            self.drawGame(screen)
            self.tock += 1
        return self.win, self.timeLeft()

    def createMap(self):
        for x in range(0,19):
            for y in range(0,13):
                xGrid = 16+16*x
                yGrid = 32+16*y
                # Bloques bordeantes
                if x == 0 or y == 0 or x == 18 or y == 12:
                    b = Tile.Block(xGrid,yGrid)
                    self.tiles.add(b)
                    self.map[x][y] = b
                # Bloques internos
                elif y % 2 == 0 and x % 2 == 0:
                    b = Tile.Block(xGrid,yGrid)
                    self.tiles.add(b)
                    self.map[x][y] = b
                # Ladrillos al azar
                elif random.randint(1,8) == 4 and (x > 2 or y > 2) and (x < 16 or y < 10):
                    b = Tile.Brick(xGrid,yGrid,self.getRandomPowerUp(xGrid,yGrid))
                    self.tiles.add(b)
                    self.map[x][y] = b

    def getRandomPowerUp(self,x,y):
        n = random.randint(1,27)
        if n < 9: 
            return Tile.BombPower(x,y)
        elif n < 15:
            return Tile.FirePower(x,y)
        elif n == 15:
            return Tile.SpeedPower(x,y)
        elif n < 19:
            return Tile.TransportPower(x,y)
        else:
            return None

    def destroy(self, tile):
        powerup = tile.destroy()
        if powerup:
            self.powerups.add(powerup)
            self.map[powerup.x][powerup.y] = powerup
        elif issubclass(tile.__class__, Tile.Bomb):
            self.explodeBomb(tile)
        else:
            self.map[tile.x][tile.y] = None


    def explodeBomb(self, bomb):
        bomb.owner.removeBomb(bomb)
        fire = Tile.Fire(bomb.rect.centerx, bomb.rect.centery,FPS*1, bomb.expansion)
        self.fires.add(fire)
        bomb.kill()
        self.map[bomb.x][bomb.y] = None

        for direction in DIRECTIONS:
            for pos in range(1,fire.expansion[direction]+1):
                x,y = fire.position(direction, pos)
                tile = self.map[x][y]
                if tile:
                    if tile.isBreakable:
                        self.destroy(tile)
                    fire.expansion[direction] = pos-1
                    break

        fire.updateSprite()

    def checkFire(self, player, fire):
        if player.x == fire.x and player.y == fire.y:
            return True
        for direction in DIRECTIONS:
            for cell in range(1,fire.expansion[direction]+1):
                x,y = fire.position(direction, cell)
                if player.x == x and player.y == y:
                    return True
        return False


    def drawGame(self, screen):
        for bomb in self.bombs:
            bomb.timer -= 1
            if bomb.timer <= 0:
                self.explodeBomb(bomb)

        for fire in self.fires:
            fire.timer -= 1
            if fire.timer <= 0:
                fire.kill()
            else:
                for player in self.players:
                    if self.checkFire(player, fire):
                        self.win = 1 if player.playerNumber is 2 else 2

        screen.fill((16,120,48))
        self.tiles.draw(screen)
        self.bombs.draw(screen)
        self.fires.draw(screen)
        self.powerups.draw(screen)
        screen.blit(self.player.image, self.player.rect)
        screen.blit(self.player.head, self.player.rhead)
        screen.blit(self.player2.image, self.player2.rect)
        screen.blit(self.player2.head, self.player2.rhead)
        self.hud.draw(screen, self.timer())
        pygame.display.flip()

    def putBomb(self, player):
        otherPlayer = self.players[player.number%2]
        if otherPlayer.x != player.x or otherPlayer.y != player.y:
            if not self.map[player.x][player.y] and not pygame.sprite.spritecollideany(player, self.bombs):
                bomb = player.createBomb(FPS*BOMB_TIME)
                if bomb:
                    self.bombs.add(bomb)
                    self.map[bomb.x][bomb.y] = bomb

    def transportPlayer(self, player):
        while True:
            x = random.randint(1,18)
            y = random.randint(1,12)
            if self.map[x][y] is None:
                break
        xr, yr = player.getSpriteCoordinates(x,y)
        player.rect.centerx = xr
        player.rect.centery = yr
        player.updatePosition()
        player.transport = False
        self.hud.removePower(player.number)

    def movePlayer(self, player, dx, dy):
        player.rect.centerx += dx
        player.rect.centery += dy

        for tile in self.tiles:
            if not tile.isCrossable and player.rect.colliderect(tile.rect):
                if dx > 0: # Moving right; Hit the left side of the tile
                    player.rect.right = tile.rect.left
                if dx < 0: # Moving left; Hit the right side of the tile
                    player.rect.left = tile.rect.right
                if dy > 0: # Moving down; Hit the top side of the tile
                    player.rect.bottom = tile.rect.top
                if dy < 0: # Moving up; Hit the bottom side of the tile
                    player.rect.top = tile.rect.bottom
        for bomb in self.bombs:
            if player.rect.colliderect(bomb.rect):
                if not bomb == player.insideBomb:
                    if dx > 0: # Moving right; Hit the left side of the bomb
                        player.rect.right = bomb.rect.left
                    if dx < 0: # Moving left; Hit the right side of the bomb
                        player.rect.left = bomb.rect.right
                    if dy > 0: # Moving down; Hit the top side of the bomb
                        player.rect.bottom = bomb.rect.top
                    if dy < 0: # Moving up; Hit the bottom side of the bomb
                        player.rect.top = bomb.rect.bottom
            elif bomb == player.insideBomb:
                player.insideBomb = None
        for powerup in self.powerups:
            if player.rect.colliderect(powerup.rect):
                if issubclass(powerup.__class__, Tile.TransportPower):
                    self.hud.putPower(player.number)
                powerup.activate(player)
                powerup.kill()
                self.map[powerup.x][powerup.y] = None

        player.updatePosition()

    def checkEvents(self):
        if SERIAL:
            PlayController = Serial.keysPS()
        else:
            PlayController = {"PS1_CUADRADO":False, "PS1_TRIANGULO":False, "PS1_CIRCULO":False, "PS1_EQUIS":False, "PS1_ARRIBA":False, "PS1_ABAJO":False, "PS1_IZQUIERDA":False, "PS1_DERECHA":False, "PS1_L1":False, "PS1_R1":False, "PS1_L2":False, "PS1_R2":False, "PS1_L3":False, "PS1_R3":False, "PS1_START":False, "PS1_SELECT":False, "PS1_JLARRIBA":False, "PS1_JLABAJO":False, "PS1_JLIZQUIERDA":False, "PS1_JLDERECHA":False, "PS1_JRARRIBA":False, "PS1_JRABAJO":False, "PS1_JRIZQUIERDA":False, "PS1_JRDERECHA":False, "PS2_CUADRADO":False, "PS2_TRIANGULO":False, "PS2_CIRCULO":False, "PS2_EQUIS":False, "PS2_ARRIBA":False, "PS2_ABAJO":False, "PS2_IZQUIERDA":False, "PS2_DERECHA":False, "PS2_L1":False, "PS2_R1":False, "PS2_L2":False, "PS2_R2":False, "PS2_L3":False, "PS2_R3":False, "PS2_START":False, "PS2_SELECT":False, "PS2_JLARRIBA":False, "PS2_JLABAJO":False, "PS2_JLIZQUIERDA":False, "PS2_JLDERECHA":False, "PS2_JRARRIBA":False, "PS2_JRABAJO":False, "PS2_JRIZQUIERDA":False, "PS2_JRDERECHA":False}
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            sys.exit(0)

        # Player 1 controls
        if keys[K_DOWN]:
            self.movePlayer(self.player,0,4*self.player.speed)
        if keys[K_UP]:
            self.movePlayer(self.player,0,-4*self.player.speed)
        if keys[K_RIGHT]:
            self.movePlayer(self.player,4*self.player.speed,0)
        if keys[K_LEFT]:
            self.movePlayer(self.player,-4*self.player.speed,0)
        if keys[K_RCTRL]:
            self.putBomb(self.player)
        if keys[K_RSHIFT] and self.player.transport:
            self.transportPlayer(self.player)


        if PlayController["PS1_ABAJO"] or PlayController["PS1_JLABAJO"]:
            self.movePlayer(self.player,0,4*self.player.speed)
        if PlayController["PS1_ARRIBA"] or PlayController["PS1_JLARRIBA"]:
            self.movePlayer(self.player,0,-4*self.player.speed)
        if PlayController["PS1_DERECHA"] or PlayController["PS1_JLDERECHA"]:
            self.movePlayer(self.player,4*self.player.speed,0)
        if PlayController["PS1_IZQUIERDA"] or PlayController["PS1_JLIZQUIERDA"]:
            self.movePlayer(self.player,-4*self.player.speed,0)
        if PlayController["PS1_EQUIS"]:
            self.putBomb(self.player)
        if PlayController["PS1_CIRCULO"] and self.player.transport:
            self.transportPlayer(self.player)

        # Player 2 controls
        if keys[K_s]:
            self.movePlayer(self.player2,0,4*self.player2.speed)
        if keys[K_w]:
            self.movePlayer(self.player2,0,-4*self.player2.speed)
        if keys[K_d]:
            self.movePlayer(self.player2,4*self.player2.speed,0)
        if keys[K_a]:
            self.movePlayer(self.player2,-4*self.player2.speed,0)
        if keys[K_LCTRL]:
            self.putBomb(self.player2)
        if keys[K_LSHIFT] and self.player2.transport:
            self.transportPlayer(self.player2)

        if PlayController["PS2_ABAJO"] or PlayController["PS2_JLABAJO"]:
            self.movePlayer(self.player2,0,4*self.player2.speed)
        if PlayController["PS2_ARRIBA"] or PlayController["PS2_JLARRIBA"]:
            self.movePlayer(self.player2,0,-4*self.player2.speed)
        if PlayController["PS2_DERECHA"] or PlayController["PS2_JLDERECHA"]:
            self.movePlayer(self.player2,4*self.player2.speed,0)
        if PlayController["PS2_IZQUIERDA"] or PlayController["PS2_JLIZQUIERDA"]:
            self.movePlayer(self.player2,-4*self.player2.speed,0)
        if PlayController["PS2_EQUIS"]:
            self.putBomb(self.player2)
        if PlayController["PS2_CIRCULO"] and self.player2.transport:
            self.transportPlayer(self.player2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

# ------------------------------
# Funcion principal del juego
# ------------------------------
 
 
def main():
    pygame.init()
    # creamos la ventana y le indicamos un titulo:
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((320, 240))
    pygame.display.set_caption("BomberPi")
 
    while True:
        game = Game()
        whoWin, timeleft = game.startGame(screen)
	date_end = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	if not whoWin is None:
		message = "Gano el jugador %s en la fecha %s a falta de %s segundos" % (whoWin, date_end, timeleft)
	else:
		message = "En la fecha %s hubo un empate de los dos jugadores" % (date_end)
	Tweet.sendTweet(message)

        #End of game
        scoreBadge=pygame.image.load("scoreframe.png")
        scoreBadge.convert_alpha()
        screen.blit(scoreBadge,(10,10))
        scoreFont=pygame.font.Font(None,52)
        scoreFont2=pygame.font.Font(None,22)
        if whoWin is None:
            statusText=scoreFont.render('Draw game',True,(255,255,255))
            screen.blit(statusText,(66,90))
        else:
            statusText=scoreFont.render('Player '+str(whoWin)+' wins',True,(255,255,255))
            screen.blit(statusText,(44,90))
        statusText2=scoreFont2.render('Press r to restart',True,(255,255,255))
        screen.blit(statusText2,(104,130))
        pygame.display.flip()
        ## Wait for the player to restart
        restart = False
        while not restart:
	    if SERIAL:
        	PlayController = Serial.keysPS()
	    else:
                PlayController = {"PS1_CUADRADO":False, "PS1_TRIANGULO":False, "PS1_CIRCULO":False, "PS1_EQUIS":False, "PS1_ARRIBA":False, "PS1_ABAJO":False, "PS1_IZQUIERDA":False, "PS1_DERECHA":False, "PS1_L1":False, "PS1_R1":False, "PS1_L2":False, "PS1_R2":False, "PS1_L3":False, "PS1_R3":False, "PS1_START":False, "PS1_SELECT":False, "PS1_JLARRIBA":False, "PS1_JLABAJO":False, "PS1_JLIZQUIERDA":False, "PS1_JLDERECHA":False, "PS1_JRARRIBA":False, "PS1_JRABAJO":False, "PS1_JRIZQUIERDA":False, "PS1_JRDERECHA":False, "PS2_CUADRADO":False, "PS2_TRIANGULO":False, "PS2_CIRCULO":False, "PS2_EQUIS":False, "PS2_ARRIBA":False, "PS2_ABAJO":False, "PS2_IZQUIERDA":False, "PS2_DERECHA":False, "PS2_L1":False, "PS2_R1":False, "PS2_L2":False, "PS2_R2":False, "PS2_L3":False, "PS2_R3":False, "PS2_START":False, "PS2_SELECT":False, "PS2_JLARRIBA":False, "PS2_JLABAJO":False, "PS2_JLIZQUIERDA":False, "PS2_JLDERECHA":False, "PS2_JRARRIBA":False, "PS2_JRABAJO":False, "PS2_JRIZQUIERDA":False, "PS2_JRDERECHA":False}

            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                sys.exit(0)
            if keys[K_r] or PlayController["PS1_START"] or PlayController["PS2_START"]:
                restart = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
 
if __name__ == "__main__":
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial

port = serial.Serial("/dev/ttyAMA0", baudrate=57600, timeout=3.0)

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
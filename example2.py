#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os

from pygameMenu import *
import pygame
import pygame.gfxdraw
from pygame.locals import *

from configLoader import configLoader
from menu import Menu, PYGAME_MENU_BACK, PYGAME_MENU_EXIT
from textmenu import TextMenu, TEXT_NEWLINE
from fonts import FONT_BEBAS

TextMenu

# constantes
WIN_SIZE = (1000, 600)
FPS = 60
COLOR_BACKGROUND = (236, 237, 238)
os.environ['SDL_VIDEO_CENTERED'] = '1'


# Clase ventana
class Window:
    def __init__(self, winsize):
        self.window = winsize

    def getWindowWidth(self):
        return self.window[0]

    def getWindowHeight(self):
        return self.window[1]


# MAIN ELEMENTS TEST
font = "pygameMenu/fonts/nevis.ttf"
window = Window(WIN_SIZE)
pygame.init()
display = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Test menu")
surface = pygame.display.get_surface()
clock = pygame.time.Clock()
image = pygame.image.load("bg1.jpg").convert_alpha()
global options
options = configLoader("window.ini", verbose=True)
track = [0]


def playTrack(index):
    track[0] = index


def dummyconfig(element, *args):
    options.setParameter(args[0], element)
    options.export()


# MENU TESTING
menu_jugar = Menu(surface, window.getWindowWidth(), window.getWindowHeight(),
                  font, "Jugar", menu_centered=False, draw_region_x=10)
menu_jugar.add_selector("Pista", [("Adelaide rw", 0), ("El origen", 1)],
                        playTrack, None)
menu_jugar.add_option("Volver", PYGAME_MENU_BACK)

# Config
menu_config = Menu(surface, window.getWindowWidth(), window.getWindowHeight(),
                   font, "Configuraciones", menu_centered=False,
                   draw_region_x=10)
menu_config.add_selector("Modo ventana",
                         [("Activado", "TRUE"), ("Desactivado", "FALSE")],
                         dummyconfig, None, "WINDOWED")
menu_config.add_option("Volver", PYGAME_MENU_BACK)

# Ayuda
menu_ayuda = TextMenu(surface, window.getWindowWidth(),
                      window.getWindowHeight(), font, "Ayuda", draw_region_y=50)
menu_ayuda.add_option("Volver", PYGAME_MENU_BACK)
menu_ayuda.add_line("Para acelerar pulsa la tecla W")
menu_ayuda.add_line("Para frenar pulsa la tecla W")
menu_ayuda.add_line(TEXT_NEWLINE)

# Acerca de menu
menu_about = TextMenu(surface, window.getWindowWidth(),
                      window.getWindowHeight(), font, "Acerca de")
menu_about.add_option("Volver", PYGAME_MENU_BACK)
menu_about.add_line("Menu para Python")
menu_about.add_line("Autor: Pablo Pizarro")
menu_about.add_line(TEXT_NEWLINE)

# Se arma menu
menu = Menu(surface, window.getWindowWidth(), window.getWindowHeight(), font,
            "Menu principal")
menu.add_option("Jugar", menu_jugar)
menu.add_option("Configuraciones", menu_config)
menu.add_option("Ayuda", menu_ayuda)
menu.add_option("Acerca de", menu_about)
menu.add_option("Cerrar", PYGAME_MENU_EXIT)

inmenu = True

while True:
    surface.fill(COLOR_BACKGROUND)
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if inmenu:
                if event.key == K_UP:
                    menu.down()
                elif event.key == K_DOWN:
                    menu.up()
                elif event.key == K_RETURN:
                    menu.select()
                elif event.key == K_LEFT:
                    menu.left()
                elif event.key == K_RIGHT:
                    menu.right()
                elif event.key == K_BACKSPACE:
                    menu.reset(1)
            else:
                print("NO_MENU")
    surface.blit(image, (0, 0))
    menu.draw()
    pygame.display.flip()

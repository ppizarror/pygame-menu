#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MENU TEXTUAL
# Menu el cual posee un campo textual (correspsondiente a varias lineas) las cuales se imprimen
# en dicho menu. Adicionalmente posee botones
#
# Autor: PABLO PIZARRO @ ppizarro ~
# Fecha: ABRIL 2015

# Importación de librerías
import types

import pygame
import pygame.gfxdraw

from menu import *


# Configuraciones de menú
MENU_FONT_TEXT_SIZE = 25
TEXT_CENTERED = False
TEXT_DRAW_X = 5
TEXT_FONT_COLOR = (255, 255, 255)
TEXT_MARGIN = 10
TEXT_NEWLINE = ""

class textMenu (Menu):

    # Constructor
    def __init__(self, surface, window, font, title, **kwargs):
        # Se llama al constructor padre
        Menu.__init__(self, surface, window.getWindowWidth(), window.getWindowHeight(), font, title, **kwargs)
        # Se obtienen parámetros pasados por kwargs
        # Define si el texto se dibuja centrado
        if kwargs.get("text_centered") is not None: self.centered_text = kwargs.get("text_centered")
        else: self.centered_text = TEXT_CENTERED
        # Color de la fuente del texto
        if kwargs.get("font_text_color") is not None: self.font_textcolor = kwargs.get("font_text_color")
        else: self.font_textcolor = TEXT_FONT_COLOR
        # Tamaño de la fuente del texto
        if kwargs.get("font_text_size") is not None: self.font_textsize = kwargs.get("font_text_size")
        else: self.font_textsize = MENU_FONT_TEXT_SIZE
        # Fuente del texto
        self.fonttext = pygame.font.Font(font, self.font_textsize)
        # Distancia vertical entre linas
        if kwargs.get("text_margin") is not None: self.textdy = kwargs.get("text_margin")
        else: self.textdy = TEXT_MARGIN
        # Variables independientes de la clase
        self.text = []
        # Punto a dibujar el texto
        if kwargs.get("draw_text_region") is not None: self.drawTextRegionX = kwargs.get("draw_text_region")
        else: self.drawTextRegionX = TEXT_DRAW_X
        self.posTextX = int(self.width * (self.drawTextRegionX / 100.0)) + self.posx

    # Agrega una linea de texto
    def addText(self, text):
        self.actual.text.append(text)
        self.actual.posOptionY += -self.actual.font_textsize - self.actual.textdy / 2

    # Dibujar el menu
    def draw(self, surface):
        # Se dibuja el fondo del menú
        pygame.gfxdraw.filled_polygon(surface, self.actual.bgRect, self.actual.bgColor)
        # Se dibuja el titulo
        pygame.gfxdraw.filled_polygon(surface, self.actual.titleRect, self._bg_color_title)
        surface.blit(self.actual.title, self.titlePos)
        dy = 0
        # Se dibuja el texto
        for linea in self.actual.text:
            text = self.actual.fonttext.render(linea, 1, self.actual.font_textcolor)
            text_width = text.get_size()[0]
            if self.actual.centered_text:
                text_dx = -int(text_width / 2.0)
            else:
                text_dx = 0
            surface.blit(text, (self.actual.posTextX + text_dx, self.actual.posOptionY + dy * (self.actual.font_textsize + self.actual.textdy)))
            dy += 1
        dy_index = 0
        for option in self.actual.opciones:
            # Si el tipo es un selector
            if option[0] == SELECTOR:
                # Si el indice seleccionado es el item se cambia el color
                if (dy == self.actual.index):
                    text = self.actual.font.render(option[1].get(), 1, self.actual.selectedcolor)
                    textBg = self.actual.font.render(option[1].get(), 1, SHADOW)
                else:
                    text = self.actual.font.render(option[1].get(), 1, self.actual.fontColor)
                    textBg = self.actual.font.render(option[1].get(), 1, SHADOW)
            else:
                # Si el indice seleccionado es el item se cambia el color
                if (dy == self.actual.index):
                    text = self.actual.font.render(option[0], 1, self.actual.selectedcolor)
                    textBg = self.actual.font.render(option[0], 1, SHADOW)
                else:
                    text = self.actual.font.render(option[0], 1, self.actual.fontColor)
                    textBg = self.actual.font.render(option[0], 1, SHADOW)
            # Se obtiene el texto y su ancho
            text_width, text_height = text.get_size()
            # Si el texto está centrado se obtiene el tamaño de la fuente
            if self.actual.centered_option:
                text_dx = -int(text_width / 2.0)
                text_dy = -int(text_height / 2.0)
            else:
                text_dx = 0
                text_dy = 0
            # Se dibuja la fuente
            if self.actual.option_shadow:
                surface.blit(textBg, (self.actual.posOptionX + text_dx - 3, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) + text_dy - 3))
            surface.blit(text, (self.actual.posOptionX + text_dx, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) + text_dy))
            # Si se tiene la seleccionada se dibuja el rectangulo
            if self.actual.drawselrect and (dy_index == self.actual.index):
                if not self.actual.centered_option: text_dx_tl = -text_width
                else: text_dx_tl = text_dx
                pygame.draw.line(surface, self.actual.selectedcolor, (self.actual.posOptionX + text_dx - 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) + text_dy - 2), \
                                 ((self.actual.posOptionX - text_dx_tl + 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) + text_dy - 2)), self.actual.rectwidth)
                pygame.draw.line(surface, self.actual.selectedcolor, (self.actual.posOptionX + text_dx - 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) - text_dy + 2), \
                                 ((self.actual.posOptionX - text_dx_tl + 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) - text_dy + 2)), self.actual.rectwidth)
                pygame.draw.line(surface, self.actual.selectedcolor, (self.actual.posOptionX + text_dx - 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) + text_dy - 2), \
                                 ((self.actual.posOptionX + text_dx - 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.opt_dy) - text_dy + 2)), self.actual.rectwidth)
                pygame.draw.line(surface, self.actual.selectedcolor, (self.actual.posOptionX - text_dx_tl + 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) + text_dy - 2), \
                                ((self.actual.posOptionX - text_dx_tl + 10, self.actual.posOptionY + dy * (self.actual.fontsize + self.actual.optiondy) - text_dy + 2)), self.actual.rectwidth)
            dy += 1
            dy_index += 1

# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os

WHITE = (255,255,255) # kolor do sprite 
BLACK =(0,0,0)
SCREEN_SIZE = (1000,720)
SCREEN_WIDTH = 2425 #rozmiar mapy
SCREEN_HEIGHT = 1300
gold=0
FPS = 30

clock = pygame.time.Clock()
screen = pygame.display.set_mode(SCREEN_SIZE)

pygame.init()
mala = pygame.font.SysFont(None,30)
srednia = pygame.font.SysFont(None,60)
duza = pygame.font.SysFont(None,100)


def text(text,color,size):
	if size == "m":
		textSurface = mala.render(text,True,color)
	elif size == "s":
		textSurface = srednia.render(text,True,color)
	elif size == "d":
		textSurface = duza.render(text,True,color)
	return textSurface,textSurface.get_rect()
    
def text_button(tekst,color,bx,by,bw,bh,size="m"):
	textSurf, textRect = text(tekst,color,size)
	textRect.center = ((bx+(bw/2)),by+(bh/2))
	screen.blit(textSurf,textRect)
    
def on_screen(tekst,color,y,x,size="mala",):
	textSurf, textRect = text(tekst,color,size)
	textRect.center = (SCREEN_SIZE[0]/2) + x,(SCREEN_SIZE[1]/2)+y
	screen.blit(textSurf,textRect)
    


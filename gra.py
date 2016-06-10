# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import sys

SCREEN_SIZE = (1000,720)
SCREEN_WIDTH = 2350 
SCREEN_HEIGHT = 1225
HORIZ_MOV_INCR = 10 #speed of movement
WHITE = (255,255,255)
FPS = 30
clock = pygame.time.Clock()


def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x - camera.rect.x, actor.rect.y - camera.rect.y, actor.rect.w, actor.rect.h)
    
class Camera(object):
    #klasa do wyśdrodkownia obrazu na boahterze
    def __init__(self, screen, player, level_width, level_height):
        self.player = player
        self.rect = screen.get_rect()
        self.rect.center = self.player.center
        self.world_rect = Rect(0, 0, level_width, level_height)

    def update(self):
      if self.player.centerx > self.rect.centerx + 25:
          self.rect.centerx = self.player.centerx - 25
      if self.player.centerx < self.rect.centerx - 25:
          self.rect.centerx = self.player.centerx + 25
      if self.player.centery > self.rect.centery + 25:
          self.rect.centery = self.player.centery - 25
      if self.player.centery < self.rect.centery - 25:
          self.rect.centery = self.player.centery + 25
      self.rect.clamp_ip(self.world_rect)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))
       
    
class Lawa(pygame.sprite.Sprite):
    '''Class for create obstacles'''#przeszkoda - teraz lawa
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("lawa.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        
class Droga(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("droga.jpg").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        
class Hero(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('hero.jpg').convert_alpha()
        self.rect=self.image.get_rect()
        self.rect.center = x,y
        self.x = 0
        self.y = 0
        self.hp = 100
        self.hajs = 0
        
    def update(self):
        self.rect.move_ip((self.x,self.y))
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top < 0: 
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT     

class Hp(pygame.sprite.Sprite):# wyświetlanie hp nad obrazkiem
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tekst = "Hp: %4d" %hero.hp
        self.font = pygame.font.SysFont(None,20)
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = 0,0
        
    def update(self):
        self.tekst = "Hp: %4d" %hero.hp
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = 0,0

class Level(object):
    '''Read a map and create a level'''
    def __init__(self, open_level):
        self.level1 = []
        self.droga = []
        self.lawa = []
        self.hero1 = []
        self.all_sprite = pygame.sprite.Group()
        self.level = open(open_level, "r")

    def create_level(self, x, y):
        for l in self.level:
            self.level1.append(l)

        for row in self.level1:
            for col in row:
                if col == "X":
                    lawa1 = Lawa(x, y)
                    self.lawa.append(lawa1)
                    self.all_sprite.add(self.lawa)
                if col == "P":
                    self.hero = Hero(x,y)
                    self.hero1.append(self.hero)
                    self.all_sprite.add(self.hero)
                if col == "Y":
                    droga1=Droga(x,y)
                    self.droga.append(droga1)
                    self.all_sprite.add(self.droga)
                    print x, y
                x += 25
            y += 25
            x = 0
            
            #zamknąć plik!

    def get_size(self):
        lines = self.level1
        line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return (self.width, self.height)
        
def tps(orologio,fps):
    temp = orologio.tick(fps)
    tps = temp / 1000.
    return tps
        

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32)
screen_rect = screen.get_rect()

background = pygame.image.load("trawa.jpg").convert_alpha()
background_rect = background.get_rect()

background2 = pygame.image.load("droga.jpg").convert_alpha()
background2_rect = background2.get_rect()

level = Level("mapa.txt")
level.create_level(0,0)
lawa = level.lawa
hero = level.hero
pygame.mouse.set_visible

#HpSprite = pygame.sprite.RenderClear()
#HpSprite.add(Hp())
#HpSprite.draw(screen)

camera = Camera(screen, hero.rect , level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite

x, y = 0, 0
action = False
while True:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                sys.exit()
            elif event.key == K_LEFT:
                hero.x = -10
                hero.y = 0
            elif event.key == K_RIGHT:
                hero.x = 10
                hero.y = 0
            elif event.key == K_UP:
                hero.y = -10
                hero.x = 0
            elif event.key == K_DOWN:
                hero.y = 10
                hero.x = 0
            elif event.key == K_SPACE:
                action = True
            if action == True and event.key == K_RIGHT:              
                hero.hp -= 1
                hero.x = 10
            if action == True and event.key == K_LEFT:
                hero.x = -10
                hero.hp -= 1
            if action == True and event.key == K_UP:
                hero.y = -10
                hero.hp -= 1
            if action == True and event.key == K_DOWN:
                hero.y = 10
                hero.hp -= 1    
        elif event.type == KEYUP:
            if event.key == K_LEFT:
                hero.x = 0
            elif event.key == K_RIGHT:
                hero.x = 0
            elif event.key == K_UP:
                hero.y = 0
            elif event.key == K_DOWN:
                hero.y = 0
            elif event.key == K_SPACE:
                action = False
    asize = ((screen_rect.w // background_rect.w + 1) * background_rect.w, (screen_rect.h // background_rect.h + 1) * background_rect.h)
    bg = pygame.Surface(asize)
    for x in range(0, asize[0], background_rect.w):
        for y in range(0, asize[1], background_rect.h):
            screen.blit(background, (x,y))
     
#     flist=[line.strip() for line in open ("mapa.txt")]
#     i = j = 0
#     for x in range(0, asize[0], background_rect.w):
#         for y in range(0, asize[1], background_rect.h):
#             screen.blit(background, (x,y))
#             if i<len(flist) and j<len(flist[i]):
#
#                 if flist[i][j] == "Y":
#                     screen.blit(background2,(x,y))
#                 else:
#                     screen.blit(background, (x,y))
#             else:
#                 screen.blit(background, (x,y))
#             j += 1
#         i += 1
        
        
    #x = y = 0
    #level3=[]
    #level2 = open("mapa.txt", "r")
    #for l in level2:
        #level3.append(l)
    #for row in level3:
     #   for col in row:
      #      if col == "Y":
       #         screen.blit(background2, (x,y))
        #    if col == " ":
         #       screen.blit(background, (x,y))
          #  y += background_rect.h
        #x += background_rect.w
            
            
    for hit in pygame.sprite.groupcollide(level.hero1,lawa,0,0):
      hero.x = -hero.x 
      hero.y = -hero.y

    time_spent = tps(clock, FPS)
    camera.draw_sprites(screen, all_sprite)

    hero.update()
    #HpSprite.update()
    camera.update()
    pygame.display.flip()  
        
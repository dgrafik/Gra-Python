# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
import os.path
import sys
import random
import math
from menu import *

def Menu():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameMenu = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
        
        screen.fill(BLACK)
        on_screen(u"NIE WIEM",WHITE,-300,0,"d")
        Button("PLAY",450,360,100,100,BLACK,BLACK,"PLAY")
        Button("QUIT",450,460,100,100,BLACK,BLACK,"QUIT")
        pygame.display.update()

def Button(text,x,y,w,h,passive_color,active_color,action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,active_color,(x,y,w,h))
        if click[0] == 1:
            if action == "PLAY":
                Game()
            if action == "QUIT":
                sys.exit()
        else:
            text_button(text,WHITE,x,y,w,h,"s")
    else:
        pygame.draw.rect(screen,passive_color,(x,y,w,h))
        text_button(text,WHITE,x,y,w,h,"s")
        

def RelRect(actor, camera): #określanie pozycji 
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
      #przesuwanie 
    def draw_sprites(self, surf, sprites):
        for s in sprites:
            if s.rect.colliderect(self.rect):
                surf.blit(s.image, RelRect(s, self))
       
    
class Lawa(pygame.sprite.Sprite):# lawa
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/lawa.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        
class Droga(pygame.sprite.Sprite): # wczytywanie drogi 
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/DROGA_1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        
class Woda(pygame.sprite.Sprite): # wczytywanie wody
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/Woda1.png").convert()
        self.rect = self.image.get_rect()
        self.rect.topleft = [self.x, self.y]
        
class Hero(pygame.sprite.Sprite): # bohater 
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data/Hero_1.png').convert_alpha()
        self.rect=self.image.get_rect()
        self.left = ["Data/Hero_2.png"]
        self.right = ["Data/Hero_3.png"]
        self.up = ["Data/Hero_4.png"]
        self.down = ["Data/Hero_1.png"]
        self.rect.center = (x,y)
        self.x = 0
        self.y = 0
        self.hp = 100
        self.gold = 0
               
    def update(self):
        self.rect.move_ip((self.x,self.y)) # żeby nie wychodzi poza ekran 
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        elif self.rect.top < 30: 
            self.rect.top = 30
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT 

class Przeciwnik(pygame.sprite.Sprite): # wolniejszy, czyli łatwiejszy przeciwnik LAMA
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/przeciwnik2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = 0
        self.y = 0
        self.gold = random.randint(1,10)
        self.hp = 100
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
            
        self.x1 = self.rect.center[0] - hero.rect.center[0]
        self.y1 = self.rect.center[1] - hero.rect.center[1]
        self.distance = math.sqrt(self.x1**2+self.y1**2)
        if self.distance <= 347:
             self.rect.left -= ((self.rect.left - hero.rect.left)/10.)*0.1
             self.rect.top -= ((self.rect.top - hero.rect.top)/10.)*0.1
             self.rect.right -= ((self.rect.right - hero.rect.right)/10.)*0.1
             self.rect.bottom -= ((self.rect.bottom - hero.rect.bottom)/10.)*0.1
             
             
class Przeciwnik1(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/Przeciwnik.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.x = 0
        self.y = 0
        self.gold = random.randint(5,15)
        self.hp = 140   
        
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
            
        self.x1 = self.rect.center[0] - hero.rect.center[0]
        self.y1 = self.rect.center[1] - hero.rect.center[1]
        self.distance = math.sqrt(self.x1**2+self.y1**2)
        if self.distance <= 278:
             self.rect.left -= ((self.rect.left - hero.rect.left)/16.)*0.3
             self.rect.top -= ((self.rect.top - hero.rect.top)/16.)*0.3
             self.rect.right -= ((self.rect.right - hero.rect.right)/16.)*0.3
             self.rect.bottom -= ((self.rect.bottom - hero.rect.bottom)/16.)*0.3

class Domek(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/ppp1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
            
            
class Domek1(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/ppp.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
           

class Domek2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/ppp31.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def update(self):
        self.x1 = self.rect.center[0] - hero.rect.center[0]
        self.y1 = self.rect.center[1] - hero.rect.center[1]
        self.distance = math.sqrt(self.x1**2+self.y1**2)
        if self.distance <= 150:
            hero.hp = 100 
 
class Drzewo(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Data/drzewo_2.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)           
            
class Hp(pygame.sprite.Sprite):# wyświetlanie hp 
    def __init__(self,x,y,hp):
        pygame.sprite.Sprite.__init__(self)
        self.tekst = "Hp: %d" %hp
        self.font = pygame.font.SysFont(None,20)
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
    def update(self,hp):
        self.tekst = "Hp: %d " %hp 
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = hero.rect.top - 30
        self.rect.left = hero.rect.left
        if self.rect.top < 0: 
            self.rect.top = 0

class GameOver(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.tekst = "GAME OVER"
        self.font = pygame.font.SysFont(None,60)
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = hero.rect.center
    def update(self):
        self.tekst = "GAME OVER" 
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = hero.rect.center
        

class HpP1(pygame.sprite.Sprite):# wyświetlanie hp 
    def __init__(self,x,y,hp):
        pygame.sprite.Sprite.__init__(self)
        self.tekst = "Hp: %d" %hp
        self.font = pygame.font.SysFont(None,20)
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
    def update(self,hp):
        self.tekst = "Hp: %d " %hp 
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = przeciwnik1.rect.top - 30
        self.rect.left = przeciwnik1.rect.left

class HpP(pygame.sprite.Sprite):# wyświetlanie hp 
    def __init__(self,x,y,hp):
        pygame.sprite.Sprite.__init__(self)
        self.tekst = "Hp: %d" %hp
        self.font = pygame.font.SysFont(None,20)
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
    def update(self,hp):
        self.tekst = "Hp: %d " %hp 
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = przeciwnik.rect.top - 30
        self.rect.left = przeciwnik.rect.left

class Gold(pygame.sprite.Sprite):# wyświetlanie hp - jeszcze nie działa 
    def __init__(self,x,y,g):
        pygame.sprite.Sprite.__init__(self)
        self.tekst = "Gold: %d"%g
        self.font = pygame.font.SysFont(None,20)
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        
    def update(self,g):
        self.tekst = "Gold: %d " %g
        self.image = self.font.render(self.tekst,1,WHITE)
        self.rect = self.image.get_rect()
        self.rect.top = hero.rect.top - 15
        self.rect.left = hero.rect.left
        if self.rect.top < -20: 
            self.rect.top = -20
        
class Level(object):
    # czyta plik txt z mapą i tworzy level, wpisuje do list
    def __init__(self, open_level):
        self.level1 = []
        self.droga = []
        self.lawa = []
        self.woda = []
        self.hero1 = []
        self.przeciwnik = []
        self.przeciwnik_1 = []
        self.hp =[]
        self.hp_1 = []
        self.hp_2 = []
        self.gold = []
        self.domek = []
        self.domek_1 = []
        self.domek_2 = []        
        self.drzewo = []
        self.all_sprite = pygame.sprite.Group()
        self.all_sprite1 = pygame.sprite.Group()
        self.all_sprite2 = pygame.sprite.Group()
        self.level = open(open_level, "r")

    def create_level(self, x, y):
        for l in self.level:
            self.level1.append(l)

        for row in self.level1: # poruszamy się po pliku i patrzymy co gdzie jest
            for col in row:
                if col == "X":
                    lawa1 = Lawa(x, y)
                    self.lawa.append(lawa1)
                    self.all_sprite.add(self.lawa)
                if col == "P":
                    self.hero = Hero(x,y)
                    self.hero1.append(self.hero)
                    self.all_sprite.add(self.hero1)
                if col == "Y":
                    droga1=Droga(x,y)
                    self.droga.append(droga1)
                    self.all_sprite1.add(self.droga)
                if col == "T":
                    self.woda1=Woda(x,y)
                    self.woda.append(self.woda1)
                    self.all_sprite.add(self.woda)
                if col == "B":
                    self.przeciwnik1 = Przeciwnik(x,y)
                    self.przeciwnik.append(self.przeciwnik1)
                    self.all_sprite.add(self.przeciwnik)
                if col == "C":
                    self.przeciwnik2 = Przeciwnik1(x,y)
                    self.przeciwnik_1.append(self.przeciwnik2)
                    self.all_sprite.add(self.przeciwnik_1)
                if col =="H":
                    self.hp1 = Hp(x,y,100)
                    self.hp.append(self.hp1)
                    self.all_sprite2.add(self.hp)
                if col == "F":
                    self.gold1 = Gold(x,y,gold)
                    self.gold.append(self.gold1)
                    self.all_sprite2.add(self.gold)
                if col =="D":
                    self.hp2 = HpP1(x,y,140)
                    self.hp_1.append(self.hp2)
                    self.all_sprite2.add(self.hp_1)
                if col == "S":
                    self.hp3 = HpP(x,y,100)
                    self.hp_2.append(self.hp3)
                    self.all_sprite2.add(self.hp_2)
                if col =="E":
                    self.domek1 = Domek(x,y)
                    self.domek.append(self.domek1)
                    self.all_sprite.add(self.domek)
                if col =="O":
                    self.domek2 = Domek1(x,y)
                    self.domek_1.append(self.domek2)
                    self.all_sprite.add(self.domek_1)
                if col == "A":
                    self.drzewo1 = Drzewo(x,y)
                    self.drzewo.append(self.drzewo1)
                    self.all_sprite.add(self.drzewo)
                if col =="W":
                    self.domek3 = Domek2(x,y)
                    self.domek_2.append(self.domek3)
                    self.all_sprite.add(self.domek_2)
                x += 25
            y += 25
            x = 0
            #zamknąć plik!

    def get_size(self): # do kamery
        lines = self.level1
        line = lines[0]
        line = max(lines, key=len)
        self.width = (len(line))*25
        self.height = (len(lines))*25
        return (self.width, self.height)
        
def tps(o,fps): #do FPS, płynniejszy ruch (czasem gubi klatki)
    temp = o.tick(fps)
    tps = temp / 1000.
    return tps
        

pygame.init()#inicjalizacja  
screen = pygame.display.set_mode(SCREEN_SIZE, FULLSCREEN, 32) # ekran
screen_rect = screen.get_rect()

background = pygame.image.load("Data/trawa1.png").convert_alpha() #tło - trawa 
background_rect = background.get_rect()

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
pygame.mixer.music.load("Music/mm.ogg")
pygame.mixer.music.play(-1)

level = Level("Mapa/mapa-5.txt")#wczytanie pliku przy inicjalizacji klasy Level 
level.create_level(0,0)
lawa = level.lawa
hero = level.hero
woda = level.woda
przeciwnik  = level.przeciwnik1
przeciwnik1 = level.przeciwnik2
domek = level.domek1
domek1 = level.domek2
domek2 = level.domek3
drzewo = level.drzewo1
hp = level.hp1
hp1 = level.hp2
hp2 = level.hp3
gold = level.gold1
pygame.mouse.set_visible = False

camera = Camera(screen, hero.rect , level.get_size()[0], level.get_size()[1])
all_sprite = level.all_sprite


def Game():
    x, y = 0, 0
    action = False
    fol = False
    a=0
    b=0
    c=0
    d=0
    while 1:
        for event in pygame.event.get(): # sterowanie 
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_LEFT:
                    hero.x = -10
                    hero.y = 0
                    hero.image = pygame.image.load(hero.left[0]).convert_alpha()
                elif event.key == K_RIGHT:
                    hero.x = 10
                    hero.y = 0
                    hero.image = pygame.image.load(hero.right[0]).convert_alpha()
                elif event.key == K_UP:
                    hero.y = -10
                    hero.x = 0
                    hero.image = pygame.image.load(hero.up[0]).convert_alpha()
                elif event.key == K_DOWN:
                    hero.y = 10
                    hero.x = 0
                    hero.image = pygame.image.load(hero.down[0]).convert_alpha()
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
        for x in range(0, asize[0],background_rect.w):
            for y in range(0, asize[1],background_rect.h):
                screen.blit(background,(x,y))

    ######################
        atakhero=random.randint(5,20)
        atakprzeciwnik1=random.randint(5,20)
        atakprzeciwnik=random.randint(2,12)
    
    #############KOLIZJE############
        for hit in pygame.sprite.groupcollide(level.hero1,lawa,0,0):
            hero.hp -= 15
            hero.x = -hero.x 
            hero.y = -hero.y
            if hero.hp<=0:
                sys.exit()
    
        for hit in pygame.sprite.groupcollide(level.hero1,woda,0,0):
            hero.x = -hero.x
            hero.y = -hero.y

        if c != 1:
            for hit in pygame.sprite.groupcollide(level.przeciwnik,level.hero1,0,0):
                hero.x = -hero.x
                hero.y = -hero.y
                hero.hp -= atakprzeciwnik
                przeciwnik.hp -= atakhero
                pygame.mixer.music.load("Music/sword.ogg")
                pygame.mixer.music.play()
                if przeciwnik.hp <= 0:
                    hero.gold += przeciwnik.gold
                    all_sprite.remove(level.przeciwnik)
                    level.all_sprite2.remove(level.hp_2)
                    d = 1
                    c = 1
                if hero.hp <= 0:
                    sys.exit()
            
        if b != 1:
            for hit in pygame.sprite.groupcollide(level.przeciwnik_1,level.hero1,0,0):
                hero.x = -hero.x
                hero.y = -hero.y
                hero.hp -= atakprzeciwnik1
                hphero = hero.hp 
                przeciwnik1.hp -= atakhero
                pygame.mixer.music.load("Music/sword.ogg")
                pygame.mixer.music.play()
            
                if przeciwnik1.hp <= 0:
                    hero.gold += przeciwnik1.gold
                    all_sprite.remove(level.przeciwnik_1)
                    level.all_sprite2.remove(level.hp_1)
                    a = 1
                    b = 1
                if hero.hp <= 0:
                    sys.exit()
            
        for hit in pygame.sprite.groupcollide(level.przeciwnik,woda,0,0):
            przeciwnik.rect.bottom -= 10
            przeciwnik.rect.top -= 10
            przeciwnik.rect.left -= 10
            przeciwnik.rect.right -= 10
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik,lawa,0,0):
            przeciwnik.rect.top += 10
            przeciwnik.rect.left += 10
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik_1,woda,0,0):
            przeciwnik1.rect.bottom += 10
            przeciwnik1.rect.top += 10 
            przeciwnik1.rect.left -= 10
            przeciwnik1.rect.right -= 10
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik_1,lawa,0,0):
            przeciwnik1.rect.top += 10
            przeciwnik1.rect.left += 10
        
        for hit in pygame.sprite.groupcollide(level.hero1,level.drzewo,0,0):
            hero.x = -hero.x
            hero.y = -hero.y
    
        for hit in pygame.sprite.groupcollide(level.przeciwnik,level.drzewo,0,0):
            przeciwnik.rect.bottom -= 10
            #przeciwnik.rect.top -= 10
            przeciwnik.rect.left += 10
            #przeciwnik.rect.right -= 10
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik_1,level.drzewo,0,0):
            przeciwnik1.rect.bottom += 10
            przeciwnik1.rect.top += 10 
            przeciwnik1.rect.left -= 10
            przeciwnik1.rect.right -= 10
        
        for hit in pygame.sprite.groupcollide(level.hero1,level.domek,0,0):
            hero.x = -hero.x
            hero.y = -hero.y
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik,level.domek,0,0):
            przeciwnik.rect.bottom -= 10
            przeciwnik.rect.top -= 10
            przeciwnik.rect.left -= 10
            przeciwnik.rect.right -= 10
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik_1,level.domek,0,0):
            przeciwnik1.rect.bottom += 10
            przeciwnik1.rect.top += 10 
            przeciwnik1.rect.left -= 10
            przeciwnik1.rect.right -= 10
    
        for hit in pygame.sprite.groupcollide(level.hero1,level.domek_1,0,0):
            hero.x = -hero.x
            hero.y = -hero.y
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik_1,level.domek_1,0,0):
            przeciwnik1.rect.bottom += 10
            przeciwnik1.rect.top += 10 
            przeciwnik1.rect.left -= 10
            przeciwnik1.rect.right -= 10
            
        for hit in pygame.sprite.groupcollide(level.przeciwnik,level.domek_1,0,0):
            przeciwnik.rect.bottom += 10
            przeciwnik.rect.top += 10 
            przeciwnik.rect.left -= 10
            przeciwnik.rect.right -= 10
    
        for hit in pygame.sprite.groupcollide(level.hero1, level.domek_2,0,0):
            hero.x = -hero.x
            hero.y = -hero.y
    
        for hit in pygame.sprite.groupcollide(level.przeciwnik,level.domek_2,0,0):
            przeciwnik.rect.bottom += 10
            przeciwnik.rect.top += 10 
            przeciwnik.rect.left -= 10
            przeciwnik.rect.right -= 10
        
        for hit in pygame.sprite.groupcollide(level.przeciwnik_1,level.domek_2,0,0):
            przeciwnik1.rect.bottom += 10
            przeciwnik1.rect.top += 10 
            przeciwnik1.rect.left -= 10
            przeciwnik1.rect.right -= 10
        
#################################### 
    
        time_spent = tps(clock, FPS)
    
        camera.draw_sprites(screen, level.all_sprite1) 
        camera.draw_sprites(screen, all_sprite)
        camera.draw_sprites(screen, level.all_sprite2)
    

        hero.update()
        camera.update()
        hp.update(hero.hp)
        domek2.update()
        gold.update(hero.gold)
        if d!=1:
            przeciwnik.update()
            hp2.update(przeciwnik.hp)
            if a!=1:
                przeciwnik1.update()
                hp1.update(przeciwnik1.hp)
            pygame.display.flip()  
       
       
Menu()
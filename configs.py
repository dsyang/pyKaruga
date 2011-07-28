#!/usr/bin/env python
# encoding: utf-8
"""
configs.py

Created by Daniel Yang on 2011-03-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import os
import pygame

##initialization
pygame.init()
#pygame.key.set_repeat(1,1)



##Default constants
DEBUG = True
AI = 0
IMAGEDIR = "images"
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800
NUM_PLAYERS = 1
MAX_SHIELD = 5

EVENT_ENEMY1 = pygame.USEREVENT+1
EVENT_ENEMY2 = pygame.USEREVENT+2
EVENT_ENEMY3 = pygame.USEREVENT+3
EVENT_BOSS =   pygame.USEREVENT+4
EVENT_ENEMY1_M = pygame.USEREVENT+5

##### Key Bindings #####




p1_bindings = {
  "left"  : (pygame.K_LEFT, "Left arrow"),
  "right" : (pygame.K_RIGHT, "Right arrow"),
  "up"    : (pygame.K_UP, "Up arrow"),
  "down"  : (pygame.K_DOWN, "Down arrow"),
  "switch": (pygame.K_b, " b key"),
  "fire"  : (pygame.K_SPACE, "Space")
}

p2_bindings = {
  "left"  : (pygame.K_a, "a key"),
  "right" : (pygame.K_d, "d key"),
  "up"    : (pygame.K_w, "w key"),
  "down"  : (pygame.K_s, "s key"),
  "switch": (pygame.K_x, "x key"),
  "fire"  : (pygame.K_z, "z key"),
}






##### Initialize Pygame #######
app_screen = pygame.display.set_mode((WINDOW_WIDTH+200, WINDOW_HEIGHT))
app_screen.fill((255,255,255))
screen = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("pyKaruga")
background_color = pygame.Surface(screen.get_size()).convert()
background_color.fill((0,0,0))

clock = pygame.time.Clock()
running = True
app_running = True
paused = False

#### Initialize sprite collections ###
humans = []
bullets = []
enemies = []
lethal =  []
powerups = []
dead_guys =[]


### Availiable Enemies ###
echoices = [
  'white_enemy1',
  'black_enemy1',
  'black_enemy2',
  'white_enemy2'
]
##Nice helpers 
def load_sliced_sprites(w, h, filename):
    images = []
    master_image = pygame.image.load(os.path.join(IMAGEDIR, filename)).convert_alpha()
    master_width, master_height = master_image.get_size()
    for k in xrange(int(master_height/h)):
      for i in xrange(int(master_width/w)):
    	  images.append(master_image.subsurface((i*w,(k)*h,w,h)))
    return images

#create image
IMG_dead = load_sliced_sprites(64,64,'explosions.png')[0]
IMG_dead_anim = load_sliced_sprites(64,64,'explosions.png')
IMG_black = [pygame.image.load(os.path.join(IMAGEDIR, "ikaruga_black.png")).convert_alpha()]
IMG_white = [pygame.image.load(os.path.join(IMAGEDIR, "ikaruga_white.png")).convert_alpha()]
IMG_bulletb = [pygame.image.load(os.path.join(IMAGEDIR, "bulletb.png")).convert_alpha()]
IMG_bulletw = [pygame.image.load(os.path.join(IMAGEDIR, "bulletw.png")).convert_alpha()]
IMG_lethalb = [pygame.image.load(os.path.join(IMAGEDIR, "enemybsm.png")).convert_alpha()]
IMG_lethalw = [pygame.image.load(os.path.join(IMAGEDIR, "enemyw.png")).convert_alpha()]   
IMG_enemy1b = [pygame.image.load(os.path.join(IMAGEDIR, "enemyb1.png")).convert_alpha()]
IMG_enemy1w = [pygame.image.load(os.path.join(IMAGEDIR, "enemyw1.png")).convert_alpha()]   
IMG_enemy2b = [pygame.image.load(os.path.join(IMAGEDIR, "enemyb2.png")).convert_alpha()]
IMG_enemy2w = [pygame.image.load(os.path.join(IMAGEDIR, "enemy02w.png")).convert_alpha()]
IMG_enemy3  = [pygame.image.load(os.path.join(IMAGEDIR, "enemy3.png")).convert_alpha()]
IMG_enemy1b_hit = [pygame.image.load(os.path.join(IMAGEDIR, "enemyb1_hit.png")).convert_alpha()]
IMG_enemy1w_hit = [pygame.image.load(os.path.join(IMAGEDIR, "enemyw1_hit.png")).convert_alpha()]  
IMG_enemy2b_hit = [pygame.image.load(os.path.join(IMAGEDIR, "enemyb2_hit.png")).convert_alpha()] 
IMG_enemy2w_hit = [pygame.image.load(os.path.join(IMAGEDIR, "enemy02w_hit.png")).convert_alpha()] 
IMG_enemy3_hit  = [pygame.image.load(os.path.join(IMAGEDIR, "enemy3_hit.png")).convert_alpha()] 


##images to load
images = {
  'dead' : IMG_dead,
  'dead_anim' : IMG_dead_anim,
  'black' : IMG_black,
  'white' : IMG_white,
  'black_bullet' : IMG_bulletb,
  'white_bullet' : IMG_bulletw,
  'black_lethal' : IMG_lethalb,
  'white_lethal' : IMG_lethalw,
  'white_enemy1' : IMG_enemy1w,
  'black_enemy1' : IMG_enemy1b,
  'black_enemy2' : IMG_enemy2b,
  'white_enemy2' : IMG_enemy2w,
  'enemy3'       : IMG_enemy3,
  'black_enemy1_hit' : IMG_enemy1b_hit,
  'white_enemy1_hit' : IMG_enemy1w_hit,
  'black_enemy2_hit' : IMG_enemy2b_hit,
  'white_enemy2_hit' : IMG_enemy2w_hit,
  'enemy3_hit'       : IMG_enemy3_hit 
  
}

color = {
  'black' : (150, 0, 0),
  'white' : (200, 200, 255),
  'black_banner' : (200, 100, 100),
  'white_banner' : (150,150,200)
}

  
bullet_configs = {
  "limit_p1" : 120, #Rate of fire
  "limit_p2" : 120,
  "lastout_p1": 0,
  "lastout_p2" :0 }
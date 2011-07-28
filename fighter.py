#!/usr/bin/env python
# encoding: utf-8
"""
fighter.py

Created by Daniel Yang on 2011-03-09.
"""

import sys
import os
import unittest
import pygame
import configs
from AnimatedSprite import AnimatedSprite

class Fighter(AnimatedSprite):
  def __init__(self, type, speed = 9, pos =(400,300), fps=10):
    images = configs.images[type]
    AnimatedSprite.__init__(self, images, fps)
    self.fps = fps
    self.type = type
    self.speed = speed
    self.rect.topleft = pos
    self.dead = False
  
  def doDie(self):
    oldpos = self.rect.topleft
    AnimatedSprite.__init__(self, configs.images["dead_anim"], self.fps)
    self.rect.topleft = oldpos
    self.dead = True



class Player(Fighter):
  def __init__(self, type, pos, speed = 9):
    Fighter.__init__(self, type, speed, pos)
    self.color = type
    self.shield = {"black": 1, "white": 1}
    self.done = False
    self.fired = 0
    self.hits = 0

  def switch_pole(self):
    if self.type == "black":
      self.type = "white"
      self.color = "white"
      oldpos = self.rect.topleft
      AnimatedSprite.__init__(self, configs.images[self.type])
      self.rect.topleft = oldpos
    else:
      self.type = "black"
      self.color = "black"
      oldpos = self.rect.topleft
      AnimatedSprite.__init__(self, configs.images[self.type])
      self.rect.topleft = oldpos
  def bulletout1(self):
    return (self.rect.left+5, self.rect.top-5)
  def bulletout2(self):
    return (self.rect.left+(self.rect.width*0.5), self.rect.top-5)
    
  def move_left(self):
    if self.rect.left < 0: pass
    else: self.rect.left += -self.speed
  
  def move_right(self):
    if self.rect.left+self.rect.width > configs.WINDOW_WIDTH: pass
    else: self.rect.left += self.speed
  
  def move_up(self):
    if self.rect.top < 0: pass
    else: self.rect.top += -self.speed
  
  def move_down(self):
    if self.rect.top+self.rect.height > configs.WINDOW_HEIGHT: pass
    else: self.rect.top += self.speed
  
  def onHit(self,color):
    if color == self.color:
      if self.shield[self.color] <= configs.MAX_SHIELD:
          self.shield[self.color] += 0.5
    else:
      self.shield[self.color] -= 1
    if filter(lambda x: x < 0, self.shield.values()):
      self.dead = True

  def onEndAnimate(self):
    if self.dead == True: 
      self.done = True
      configs.running = False
      



class Enemy(Fighter):
  def __init__(self, type, speed, pos, move, fire_limit, lethal_speed, health=1):
    Fighter.__init__(self, type, speed, pos, 400)
    self.color = type[0:5]
    self.type_num = int(type[-1])
    self.done = False
    
    
    self.move = move
    self.state = "move"

    self.health = health    
    self.isHit = False
    self.hurt_anim_Counter = 3
    self.killed_by = ""
    
    self.last_lethal = pygame.time.get_ticks()
    self.fire_limit= fire_limit
    self.lethal_speed = lethal_speed
    
  def set_state(self, str):
    self.state = str
  def set_move_pattern(self, move):
    self.move= move
    
  def update(self, t):
    if self.isHit:
      self.hurt_anim_Counter -= 1
      if self.hurt_anim_Counter == 0:
        oldpos = self.rect.topleft
        self.isHit = False
        AnimatedSprite.__init__(self, configs.images[self.type])
        self.rect.topleft = oldpos
        self.hurt_anim_Counter = 3
    Fighter.update(self,t)
    dx, dy = self.move.update(self)
    self.rect.top += dy
    self.rect.left += dx
    
  def bulletout(self):
    x,y = self.rect.midbottom
    if self.type_num == 1 and self.color == "black":
      return [(x-5, y-5)]
    if self.type_num == 2 and self.color == "black":
      return [(self.rect.right-7, y-5), (self.rect.left+7, y-5)]
    if self.type_num == 1 and self.color == "white":
      return [(x-10, y-5), (x, y-5)]
    if self.type_num == 2 and self.color == "white":
      return [(self.rect.right-10, y-15), (self.rect.left+10, y-15)]

  def onEndAnimate(self):
    if self.dead == True: self.done = True
    
  def onHit(self,b):
    if b.color == self.color: 
      self.health -= 0.5
    else:
      self.health -= 1
    if self.health <= 0:
      self.dead = True
      self.killed_by = b.source
    if not self.dead:
      oldpos = self.rect.topleft
      self.isHit = True
      AnimatedSprite.__init__(self, configs.images[self.type + "_hit"])
      self.rect.topleft = oldpos


    
if __name__ == '__main__':
  unittest.main()
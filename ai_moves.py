#!/usr/bin/env python
# encoding: utf-8
"""
ai_moves.py

Created by Daniel Yang on 2011-03-10.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import random
import math
import pygame
import configs

class MoveStraight():
  def __init__(self, e):
    self.start_pos = e.rect.center
  def update(self, e):
    dy = e.speed
    dx = 0
    if e.rect.top > configs.WINDOW_HEIGHT*0.3:
      e.set_state("atk")
      dy = e.speed/2
    return (dx, dy)


class MoveZag():
  def __init__(self, e):
    self.start_x, self.start_y = e.rect.center
    self.zag_dist = 2*e.rect.width
    self.direction = 1
    e.set_state("atk")
  def update(self, e):
    if abs(e.rect.left-self.start_x) > self.zag_dist:
      self.direction *= -1
    if e.rect.top > configs.WINDOW_HEIGHT*0.3:
      dy = e.speed/2
      dx = self.direction*(e.speed-1)
    else:
      dy = e.speed
      dx = self.direction*e.speed
    return(dx, dy)
    
### Doesn't Work ###    
class MoveCircle():
  def __init__(self, e):
    self.start_x, self.start_y = e.rect.center
    self.radius = e.rect.width
    e.set_state("atk")
    self.degree = 0
  def update(self, e):
    dy = e.speed
    dx = 0
    if e.rect.top > configs.WINDOW_HEIGHT*0.25:
      self.degree += 1
      dx = math.cos(self.degree * 2* math.pi /360 ) * 2#self.radius
      dy = math.sin(self.degree * 2 * math.pi / 360) * 2#self.radius
      if self.degree >= 360: self.degree = 0
    return (dx,dy)
    
class MoveDiamond():
  def __init__(self, e):
    self.diameter = 100
    if e.rect.left > configs.WINDOW_WIDTH*0.5:
      self.center_x = e.rect.left - self.diameter
      self.dir_x = -1
    else:
      self.center_x = e.rect.left + self.diameter
      self.dir_x = 1
    self.center_y = configs.WINDOW_HEIGHT*0.25
    self.dir_y = 1
    self.start = False
  def update(self, e):
    dy = e.speed
    dx = 0
    if e.rect.top > self.center_y:
      self.start = True
      e.set_state("atk")
    if self.start:
      if abs(e.rect.left-self.center_x) > self.diameter:
        self.dir_x *= -1
      if abs(e.rect.top-self.center_y) > self.diameter:
        self.dir_y *= -1
      dy = self.dir_y*(e.speed/2)
      dx = self.dir_x*(e.speed/2)
    return (dx, dy)
    
attack_patterns = [MoveStraight, MoveZag]


  
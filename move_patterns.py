#!/usr/bin/env python
# encoding: utf-8
"""
move_patterns.py

Created by Daniel Yang on 2011-03-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import pygame
import configs
import math

class move_patterns(object):
  def __init__(self):
    self._last_update = 0
    self.delay = 200
    
    self.zag_limit = 0
    self.zag_amt = 0

  def move_straight(self,rect, speed,t):
    return (0, speed)

  def move_wave(self,rect, speed,t):
    if(t-self._last_update > self.delay):
      self._last_update = t
      return (math.sin(t)*speed*10, speed)
    else: return (0,speed)
    
  def move_zag(self, rect, speed, t):
    self.zag_limit = 2*rect.width
    if self.zag_amt <= 0: dlr = speed
    elif self.zag_amt < self.zag_limit: dlr = -speed 
    self.zag_amt += dlr
    return(dlr, speed)
    

def circle(elapsed, level):
  

attack_patterns = 
[
  circle,
  straight,
  vformation,
  moverotate
]
mp = move_patterns()
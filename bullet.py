#!/usr/bin/env python
# encoding: utf-8
"""
bullet.py

Created by Daniel Yang on 2011-03-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import configs
from AnimatedSprite import AnimatedSprite
from fighter import Fighter


class Bullet(AnimatedSprite):
  def __init__(self, type, pos, source, dir = 1, dy=10, dx=0, fps = 10):
    images = configs.images[type]
    AnimatedSprite.__init__(self, images, fps)
    self.dy = dy*dir
    self.dx = dx
    self.rect.topleft = pos
    self.type = type
    self.color = type[0:5]
    self.source = source
    
  def update(self, t):
    self.rect.top += -self.dy
    self.rect.left += self.dx
    
  def onCollide(self):
    pass


if __name__ == '__main__':
  unittest.main()
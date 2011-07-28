#!/usr/bin/env python
# encoding: utf-8
"""
AnimatedSprite.py

Created by Daniel Yang on 2011-03-09.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import pygame


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, images, fps = 10):
        pygame.sprite.Sprite.__init__(self)
        self._images = images

        # Track the time we started, and the time between updates.
        # Then we can figure out when we have to switch the image.
        self._start = pygame.time.get_ticks()
        self._delay = 750 / fps
        self._last_update = 0
        self._frame = 0

        # Call update to set our first image.
        #self.update(pygame.time.get_ticks())
        self.image = self._images[self._frame]
        self.rect = self.image.get_rect()

    def onEndAnimate(self):
      pass
    def update(self, t):
        # Note that this doesn't work if it's been more that self._delay
        # time between calls to update(); we only update the image once
        # then, but it really should be updated twice.

        if t - self._last_update > self._delay:
            self._frame += 1
            if self._frame >= len(self._images):
              self._frame = len(self._images)-1
              self.onEndAnimate()
            self.image = self._images[self._frame]
            self._last_update = t



if __name__ == '__main__':
  print "YOU SHOULDN'T BE RUNNING THIS!"
#!/usr/bin/env python
# encoding: utf-8
"""
menu.py

Created by Daniel Yang on 2011-03-11.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest
import pygame


class menu:
  def __init__(self, stats):
    self.running = True
    self.s1 = stats[0]
    if len(stats) > 1:
      self.s2 = stats[1]
    else:
      self.s2 = None
  def run(self):
    screen = pygame.display.set_mode((400,400))
    pygame.display.set_caption("pyKaruga")
    background_color = pygame.Surface(screen.get_size()).convert()
    background_color.fill((0,0,0))
    
    while self.running:
      screen.fill((0,0,0))
      font2 = pygame.font.Font("destructobeambb_reg.otf", 36)
      gg = font2.render("GAME OVER!", True, (255,255,255))
      screen.blit(gg, (100,100))
      screen.blit(self.s1, (0,200))
      if self.s2:
        screen.blit(self.s2, (200,200))
      pygame.display.set_caption("GAME OVER!!")
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
        if event.type == pygame.KEYDOWN and (event.key == pygame.K_ESCAPE or event.key == pygame.K_q):
          self.running = False
      pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
  #pygame.init()
  #n = menu()
  pass
  #n.run()
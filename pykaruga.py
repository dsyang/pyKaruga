#!/usr/bin/env python
# encoding: utf-8

#### A shmup similar to Ikaruga ####

import pygame, math
import random
import configs
from AnimatedSprite import AnimatedSprite
from fighter import *
from ai_moves import *
from bullet import Bullet
from menu import menu

### create groups of random enemies and have them follow a random path
# Then throw them at the players until all gone, then wait one sec, then repeat
# extra group every 15 seconds, refresh to 1 group every minute
# extra enemy per group every minute
# powerups every 30 seconds
# two player game
# polarity


humans    = configs.humans      
bullets   = configs.bullets    
enemies   = configs.enemies    
lethal    = configs.lethal      
powerups  = configs.powerups  
dead_guys = configs.dead_guys

bconf = configs.bullet_configs
screen = configs.screen
        

##### Stats Variables #####
p1shots = 0
p1hits  = 0
p1kills = 0
p2shots = 0
p2hits  = 0
p2kills = 0


def handle_player_collisions():
  if(configs.NUM_PLAYERS == 1):
    if humans:
      p1 = humans[0]
      if p1.rect.collidelistall(enemies) and not p1.dead: p1.doDie()
  else:
    if len(humans) > 1:
      p1, p2 = humans
      if pygame.sprite.collide_rect(p1, p2) and (not p1.dead or not p2.dead):
        p1.doDie()
        p2.doDie()
      if p1.rect.collidelistall(enemies) and not p1.dead: p1.doDie()
      if p2.rect.collidelistall(enemies) and not p2.dead: p2.doDie()

def handle_enemy_actions(t):
  global p1hits, p2hits, p1kills, p2kills
  # Mark those who have been hit
  for e in enemies:
    for b in bullets:
      if e.rect.colliderect(b.rect): 
        if b in bullets: bullets.remove(b)
        if b.source == "p1": p1hits += 1
        elif b.source == "p2": p2hits += 1
        e.onHit(b)
        if e.dead:
          if e in enemies: enemies.remove(e)
          dead_guys.append(e)
          if e.killed_by == "p1": p1kills += 1
          elif e.killed_by == "p2": p2kills += 1
          e.doDie()
    #fire lethal weapons
    if t-e.last_lethal > e.fire_limit and e.state == "atk":
      for out in e.bulletout():
        lethal.append(Bullet(e.color + "_lethal", out,"e", -1))
        e.last_lethal = t

def handle_lethal_collisions():
  for h in humans:
    for l in lethal:
      if h.rect.colliderect(l.rect):
        if l in lethal: lethal.remove(l)
        h.onHit(l.color)
        if h.dead: 
          if h in humans: humans.remove(h)
          dead_guys.append(h)
          h.doDie()


def D_formation(level, speed, fire_limit, pos, mix, health):
  c1 = random.choice(["black_enemy", "white_enemy"])
  if mix:
    if c1 == "black_enemy": c2 = "white_enemy"
    else: c2 = "black_enemy" 
  else: c2 = c1
  e1 = Enemy(c1+str(level), speed+2, (pos, -10), None, fire_limit, speed, health)
  e1.set_move_pattern(MoveDiamond(e1))
  e2 = Enemy(c2+str(level), speed+2,
              (pos, -10-(e1.rect.height+50)),
               None, fire_limit, speed, health)
  e2.set_move_pattern(MoveDiamond(e2))
  e3 = Enemy(c2+str(level), speed+2,
              (pos, -10-2*(e2.rect.height+50)),
               None, fire_limit, speed, health)
  e3.set_move_pattern(MoveDiamond(e3))
  e4 = Enemy(c1+str(level), speed+2,
              (pos, -10-3*(e3.rect.height+50)),
               None, fire_limit, speed, health)
  e4.set_move_pattern(MoveDiamond(e4))
  enemies.append(e1)
  enemies.append(e2)
  enemies.append(e3)
  enemies.append(e4)

def V_formation(level, speed, fire_limit, pos, mix, health):
  c1 = random.choice(["black_enemy", "white_enemy"])
  if mix:
    if c1 == "black_enemy": c2 = "white_enemy"
    else: c2 = "black_enemy" 
  else: c2 = c1
  e1 = Enemy(c1+str(level), speed+2, (pos, -10), None, fire_limit, speed, health)
  e1.set_move_pattern(MoveStraight(e1))
  e2 = Enemy(c2+str(level), speed+2,
              (pos-(e1.rect.width+5), -10-(e1.rect.height+10)),
               None, fire_limit, speed, health)
  e2.set_move_pattern(MoveStraight(e2))
  e3 = Enemy(c2+str(level), speed+2,
              (pos+(e1.rect.width+5), -10-(e1.rect.height+10)),
               None, fire_limit, speed, health)
  e3.set_move_pattern(MoveStraight(e3))
  e4 = Enemy(c1+str(level), speed+2,
              (pos-2*(e1.rect.width+5), -10-2*(e1.rect.height+10)),
               None, fire_limit, speed, health)
  e4.set_move_pattern(MoveStraight(e4))
  e5 = Enemy(c1+str(level), speed+2,
              (pos+2*(e1.rect.width+5), -10-2*(e1.rect.height+10)),
               None, fire_limit, speed, health)
  e5.set_move_pattern(MoveStraight(e5))
  enemies.append(e1)
  enemies.append(e2)
  enemies.append(e3)
  enemies.append(e4)
  enemies.append(e5)


def setup_enemies(elapsed, level, speed=None):
  if not speed: speed = elapsed/100000
  random.seed(elapsed)
  pos = random.randint(configs.WINDOW_WIDTH*0.4, configs.WINDOW_WIDTH*0.6)
  fire_limit = random.randint(800, 1500)
  color = random.choice(["black_enemy", "white_enemy"])
  e= Enemy(color+str(level), speed+2, (pos, -10), None, fire_limit, speed, 2.0*level+speed)
  e.set_move_pattern(random.choice(attack_patterns)(e))
  enemies.append(e)
  #random.choice(attack_patterns)(elapsed, level)

def setup_multiple_enemies(elapsed, level, speed=None):
  if not speed: speed = elapsed/100000
  random.seed(elapsed)
  pos = random.randint(configs.WINDOW_WIDTH*0.25, configs.WINDOW_WIDTH*0.75)
  fire_limit = random.randint(800, 1500)
  formation = random.choice(["V", "D", "V_mix", "D_mix"])
  health = 3.0+speed
  if formation == "V": V_formation(level, speed, fire_limit, pos, False, health)
  elif formation == "V_mix": V_formation(level, speed, fire_limit, pos, True, health)
  elif formation == "D" : D_formation(level, speed, fire_limit, pos, False, health)
  elif formation == "D_mix":  D_formation(level, speed, fire_limit, pos, True, health)


def main():
  global p1shots, p2shots
  
  player1 = Player("white", (400, 700))
  humans.append(player1)
  if configs.NUM_PLAYERS == 2:
    player2 = Player("black", (200, 700))
    humans.append(player2)
  font = pygame.font.Font("destructobeambb_reg.otf", 14)
  big_font = pygame.font.Font("destructobeambb_reg.otf", 20)
  #### Setup Enemy Spawns ####
  pygame.time.set_timer(configs.EVENT_ENEMY1_M, 5000)
  pygame.time.set_timer(configs.EVENT_ENEMY1, 3000)
  pygame.time.set_timer(configs.EVENT_ENEMY2, 7000)
  #pygame.time.set_timer(configs.EVENT_ENEMY3, 24000)
  #pygame.time.set_timer(configs.EVENT_BOSS, 360000)
  
  
  #### Setup Stats Screen ####
  stats1 = pygame.Surface((200,200))
  if configs.NUM_PLAYERS == 2:
    stats2 = pygame.Surface((200,200))
  
  #### Setup Control Surfaces ####
  controls1 = pygame.Surface((200,200))
  controls1.fill((255,255,255))
  if configs.NUM_PLAYERS == 2:
    controls2 = pygame.Surface((200,200))
    controls2.fill((255,255,255))
  
  #### Setup Paused Surface ####
  paused = pygame.Surface((500,100))
  paused_text = big_font.render("Paused: Hit <enter> to continue", True, (255,255,255))
  paused.blit(paused_text, (0,0))
  #### Key Bindings ####  
  b1 = configs.p1_bindings
  b2 = configs.p2_bindings
  
  start_time = pygame.time.get_ticks()
  while configs.app_running:
    while configs.running:
      dt = configs.clock.tick(60) #delay to keep the game running slower than 60 ticks per second
      t = pygame.time.get_ticks()
      screen.blit(configs.background_color, (0,0))
      configs.app_screen.fill((255,255,255))
      
      #if t % 15 == 3:
      #  print "enemies!"
      #  setup_enemies()
      if not configs.paused:
        keys = pygame.key.get_pressed()
        if configs.NUM_PLAYERS == 2:
          if(keys[b2["up"][0]   ]): player2.move_up()
          if(keys[b2["down"][0] ]): player2.move_down()
          if(keys[b2["left"][0] ]): player2.move_left()
          if(keys[b2["right"][0]]): player2.move_right()
          if(keys[b2["fire"][0] ]):
            if(t-bconf["lastout_p1"]) > bconf["limit_p1"] and not player2.dead:
              bullets.append(Bullet(player2.type + "_bullet", player2.bulletout1(), "p2"))
              bullets.append(Bullet(player2.type + "_bullet", player2.bulletout2(), "p2"))
              bconf["lastout_p1"] = t
              p2shots =  p2shots + 2
        if(keys[b1["up"][0]   ]):   player1.move_up()
        if(keys[b1["down"][0] ]): player1.move_down()
        if(keys[b1["left"][0] ]): player1.move_left()
        if(keys[b1["right"][0]]): player1.move_right()
        if(keys[b1["fire"][0] ]):
          if(t-bconf["lastout_p2"]) > bconf["limit_p2"] and not player1.dead:
            bullets.append(Bullet(player1.type + "_bullet", player1.bulletout1(), "p1"))
            bullets.append(Bullet(player1.type + "_bullet", player1.bulletout2(), "p1"))
            bconf["lastout_p2"] = t
            p1shots = p1shots + 2
            
            
        handle_player_collisions()
        handle_lethal_collisions()
        handle_enemy_actions(t)
      else:pass
  
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          configs.running = False
          configs.app_running = False
          
        if event.type == configs.EVENT_ENEMY1 and not configs.paused:
          setup_enemies(t-start_time, 1)
        if event.type == configs.EVENT_ENEMY1_M and not configs.paused:
          l = random.randint(1,2)
          setup_multiple_enemies(t-start_time, l)
        if event.type == configs.EVENT_ENEMY2 and not configs.paused:
          setup_enemies(t-start_time, 2)
        if event.type == configs.EVENT_ENEMY3 and not configs.paused:
          setup_enemies(t-start_time, 3)
        if event.type == configs.EVENT_BOSS and not configs.paused:
          setup_boss()
        
        if event.type == pygame.KEYDOWN:
          if event.key == b2["switch"][0] and configs.NUM_PLAYERS == 2 and not configs.paused:
            player2.switch_pole()
          if event.key == b1["switch"][0] and not configs.paused:
            player1.switch_pole()
          if event.key == pygame.K_RETURN:
            if configs.paused: configs.paused = False
            else: configs.paused = True
          if event.key == pygame.K_SPACE and configs.DEBUG == True:
            setup_enemies(start_time-t, 1, 1)
          if event.key == pygame.K_t and configs.DEBUG == True:
            setup_multiple_enemies(start_time-t, 1, 1)
          if event.key == pygame.K_p and configs.DEBUG == True:
            if configs.NUM_PLAYERS == 2: player2.doDie() 
            player1.doDie()
      
      
      
      ###############################
      ###   UPDATE Then DRAW    #####
      ###############################
      
      if not configs.paused:
        for h in humans:
          h.update(t)
          screen.blit(h.image, h.rect)
        for b in bullets:
          b.update(t)
          screen.blit(b.image, b.rect)
        
        for p in filter(lambda x: not x.dead, humans):
          if p.shield[p.type] > 0:
            pygame.draw.circle(
            screen, configs.color[p.type], p.rect.center, p.rect.width*0.65, 2+p.shield[p.type])
        
        for e in enemies:
          e.update(t)
          screen.blit(e.image, e.rect)
        for l in lethal:
          l.update(t)
          screen.blit(l.image, l.rect)
        for d in dead_guys:
          d.update(t)
          screen.blit(d.image, d.rect)
        
        for d in dead_guys:
          if d.done:
            dead_guys.remove(d)
        for e in enemies:
          if (e.rect.top > configs.WINDOW_HEIGHT):
              enemies.remove(e)
        for l in lethal:
          if(l.rect.top > configs.WINDOW_HEIGHT or l.rect.top < 0):
            lethal.remove(l)   
        
        for bullet in bullets:
          if(bullet.rect.top > configs.WINDOW_HEIGHT or bullet.rect.top < 0):
            bullets.remove(bullet)
      else:
        screen.blit(paused, (150,400))
        
      
      
      
      
      #####################################
      #####     RIGHT panel code      #####
      #####################################
      
      title1 = font.render("PLAYER 1 STATS:", True, (0,0,0))
      acc1 = font.render("Shots hit/fired: %d/%d" % (p1hits, p1shots), True, (0, 0, 0))
      shieldb1 = font.render("Red Shield Strength: %d" % player1.shield["black"], True, (0,0,0))
      shieldw1 = font.render("Blue Shield Strength: %d" % player1.shield["white"], True, (0,0,0)) 
      kills1 = font.render("Enemies killed: %d" % p1kills, True, (0,0,0))
      
      if configs.NUM_PLAYERS == 2:
        title2 = font.render("PLAYER 2 STATS:", True, (0,0,0))
        acc2 = font.render("Shots hit/fired: %d/%d" % (p2hits, p1shots), True, (0, 0, 0))
        shieldb2 = font.render("Red Shield Strength: %d" % player2.shield["black"], True, (0,0,0))
        shieldw2 = font.render("Blue Shield Strength: %d" % player2.shield["white"], True, (0,0,0))
        kills2 = font.render("Enemies killed %d" % p2kills, True, (0,0,0))
      ### Manage Stats Screen ###
      if humans:
        stats1.fill(configs.color[player1.type+"_banner"])
        stats1.blit(title1, (0,0))
        stats1.blit(player1.image, (50,20))
        stats1.blit(acc1, (0,70))
        stats1.blit(kills1, (0,90))
        stats1.blit(shieldb1, (0,110))
        stats1.blit(shieldw1, (0,130))
        if configs.NUM_PLAYERS == 2:
          stats2.fill(configs.color[player2.type+"_banner"])
          stats2.blit(title2, (0,0))
          stats2.blit(player2.image, (50,20))
          stats2.blit(acc2, (0,70))
          stats2.blit(kills2, (0,90))
          stats2.blit(shieldb2, (0,110))
          stats2.blit(shieldw2, (0,130))
      
      
      ### Draw Controls ###
      controls = font.render("Controls", True, (0, 0, 0))
      up1 = font.render("P1 up = " + b1["up"][1], True, (0, 0, 0))
      down1 = font.render("P1 down = " + b1["down"][1], True, (0, 0, 0))
      left1 = font.render("P1 left = " + b1["left"][1], True, (0, 0, 0))
      right1 = font.render("P1 right = " + b1["right"][1], True, (0, 0, 0))
      switch1 = font.render("P1 switch color = " + b1["switch"][1], True, (0, 0, 0))
      fire1 = font.render("P1 shoot = " + b1["fire"][1], True, (0, 0, 0))
      
      controls1.blit(controls, (0,10))
      controls1.blit(up1, (0,35))
      controls1.blit(down1, (0,55))
      controls1.blit(left1, (0,75))
      controls1.blit(right1, (0,95))
      controls1.blit(switch1, (0,115))
      controls1.blit(fire1, (0,135))
      
      up2 = font.render("P2 up = " + b2["up"][1], True, (0, 0, 0))
      down2 = font.render("P2 down = " + b2["down"][1], True, (0, 0, 0))
      left2 = font.render("P2 left = " + b2["left"][1], True, (0, 0, 0))
      right2 = font.render("P2 right = " + b2["right"][1], True, (0, 0, 0))
      switch2 = font.render("P2 switch color = " + b2["switch"][1], True, (0, 0, 0))
      fire2 = font.render("P2 shoot = " + b2["fire"][1], True, (0, 0, 0))
      
      if configs.NUM_PLAYERS == 2:
        controls2.blit(controls, (0,10))
        controls2.blit(up2, (0,35))
        controls2.blit(down2, (0,55))
        controls2.blit(left2, (0,75))
        controls2.blit(right2, (0,95))
        controls2.blit(switch2, (0,115))
        controls2.blit(fire2, (0,135))
      
      configs.app_screen.blit(stats1, (configs.WINDOW_WIDTH,0))
      configs.app_screen.blit(controls1, (configs.WINDOW_WIDTH, 200))
      if configs.NUM_PLAYERS == 2:
        configs.app_screen.blit(stats2, (configs.WINDOW_WIDTH, 400))
        configs.app_screen.blit(controls2, (configs.WINDOW_WIDTH, 600))
      configs.app_screen.blit(screen, (0,0))
      pygame.display.flip()
      
    ##End game
    if configs.app_running:
      if configs.NUM_PLAYERS == 2: arguments = [stats1, stats2]
      else: arguments = [stats1]
      gg = menu(arguments)
      gg.run()
      configs.app_running = False
  pygame.quit()


if __name__ == '__main__':
  main()

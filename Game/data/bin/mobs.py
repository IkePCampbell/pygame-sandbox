import pygame
import time
from random import randint
clock = pygame.time.Clock()

"""
Welcome to the mob section. Where all your different enemies exist.e
These will always be in development.
"""


class EnMob:
  """
  This should be the class all other mobs inherit from:
  Level  : lvl
  HP     : health
  Attack : a
  Defense: d
  Gold   : g
  Initial X: iX
  Initial Y: iY
  """
  def __init__(self,lvl,health,a,d,g,iX,iY):
    self.level = lvl
    self.hp = health
    self.attack = a
    self.deff   = d
    self.gold   = g
    self.x = iX*32 #tile size is 32
    self.y = iY*32
    self.rect = pygame.Rect(self.x,self.y, 32,32)
    self.limitXp = (iX*32)+32
    self.limitYp = (iY*32)+32
    self.limitXn = (iX*32)-32
    self.limitYn = (iY*32)-32
    self.step = 64
    self.adir = -1
    self.lastmove = 0
    self.moveopt = [0,1,2,3,4]
    self.ismoving = False
    self.countstep = 0

  def draw(self,win):
    """
    Okay so here is the dealerino. In order for me not to worry about increments
    of 32 im going to do what i did in my player move file and just divide things by 32
    """
    if self.ismoving == False:
      self.adir = randint(0,4)
      self.premove()
    self.move()
    self.lastmove = self.moveopt[self.adir]



    pygame.draw.rect(win,(0,0,0),self.rect,2)


  def premove(self):
    """
    The purpose of this is so that way when our bat is up at the top right of the screen,
    he cant chimp out and keep trying to go up and right, purpose is to remove some options
    from the moveopt list. Also so actions cant be repeated.


    NOTE: THIS IS THE ONLY FUNCTION THAT SHOULD OVERRIDE THE NPCS MOVEMENT
    """
    if self.lastmove == self.adir: #if the last move was left and they try again , left  is 2
      tmp = self.moveopt[::] #make a copy [0,1,2,3,4]
      tmp.remove(self.lastmove) #remove 2, [0,1,3,4]
      rand = randint(0,3) # THIS CHOOSES THE NEW VALUE randomly
      self.adir = tmp[rand] #indexes the NEW value for self.adir

##  DBUG
##      print('LASTMOVE WAS:',self.lastmove)
##      print('copy of list new list',tmp)
##      print('newint',rand)
##      print('new dir',self.adir)
##      print('AVOIDED DUPE MOVE')


  def move(self):
    """
    Moves the mob

    This crap can kinda be confusing so here is the rundown, self.adir stands for
    "a direction", so 0 is not moving, 1 is moving left, 2 right, 3 up, 4 down
    for some reason pygame is kinda wack when it comes to its update functions.
    so i have to set a variable called ismoving when a random value is assigned.
    that way the update in the main game will fire, the random variable generation WONT fire
    and this function will fire still with the same movement patterns.

    the if self.countstep == self.step is just a test function, i would like
    to give the people a freedom of up to 2 squares away (64)
    so i believe this is the best way to get solid yet RANDOM movement among ANY AI CRITTERS
    """
    self.ismoving = True

    if self.adir == 0:
      self.countstep +=1
      if self.countstep == self.step:
        self.ismoving = False
        self.countstep = 0

    if self.adir == 1: #left
      self.rect.x -=1
      self.countstep +=1
      if self.countstep == self.step:
        self.ismoving = False
        self.countstep = 0


    if self.adir == 2: #right
      self.rect.x +=1
      self.countstep +=1
      if self.countstep == self.step:
        self.ismoving = False
        self.countstep = 0

    if self.adir == 3: #up
      self.rect.y -=1
      self.countstep +=1
      if self.countstep == self.step:
        self.ismoving = False
        self.countstep = 0

    if self.adir == 4: #down
      self.rect.y +=1
      self.countstep +=1
      if self.countstep == self.step:
        self.ismoving = False
        self.countstep = 0

    if self.rect.x <= self.limitXn:
      self.rect.left = self.limitXn

    if self.rect.x >= self.limitXp:
      self.rect.right = self.limitXp+32

    if self.rect.y <= self.limitYn:
      self.rect.top = self.limitYn

    if self.rect.y >= self.limitYp:
      self.rect.bottom = self.limitYp+32

class Bat(EnMob):
  """inherits all traits from EnMob class"""
  def __init__(self,lvl,health,a,d,g,iX,iY):
    self.id = "001"
    self.name = "Bat"
    #what this is doing is inheriting from the enmob class so its cleaner for me to
    #write instead of wasting 10+ lines for every mob
    super().__init__(lvl,health,a,d,g,iX,iY)

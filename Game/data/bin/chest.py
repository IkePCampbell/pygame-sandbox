import pygame
from .icons import Icons
all_icons = Icons()
###########################################################################################
class Chest:
  #chest, all chests will follow like this
  #- sprite
  def __init__(self,x,y,num):
    self.x = x
    self.y = y
    self.rect = pygame.Rect(self.x, self.y,32,32)
    self.isopen = num
    self.openpos = (self.x/32,(self.y/32)+1) #tc is the (row,height) from draw_tiles

    #DEBUG SHOW COLLISION, COMMENT OUT WHEN DONE
    #(GAME.win,(255,0,0),self.rect,2)

  #code to open
  def update(self,achar,amessage,agame,ainventory):
    keys = pygame.key.get_pressed()
    if self.isopen == 0:
        if achar.current_pos == self.openpos: #if our char is right under the chest
          if achar.rect.top == self.rect.bottom:# and its touching the bottom of chest and chest label is unopened
            if keys[pygame.K_e]: #user hits e
              if self.isopen < 1: #delete this and do self.isopen = ``
                self.isopen +=1
                chest_reward = (self.chest_reward(agame.level1_chest_rewards, agame.item_list, (self.x/32, self.y/32)))
                amessage.show +=1
                amessage.text = ["You got: "+chest_reward[1]+'.']
                ainventory.inventory.append(chest_reward)


    if self.isopen == 1:
      return all_icons.gold_chest_opened
    else:
      return all_icons.gold_chest_closed

  def chest_reward(self,llist,ilist,coord):
    for chest in llist:  #((3,3) , 0)
      if chest[0] == coord:
        for item in ilist: #[0, potion of health]
          if chest[1] == item[0]:
            return item

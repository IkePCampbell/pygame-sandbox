import pygame
class Main_Player(pygame.sprite.Sprite):
  def __init__(self, x, y,adict,enemydict,npcdict,maxhealth,maxmana):
  #maxhp : maxhealth is the maxHP for char
  #hp    : currhealth is the currentHP for char
    self.x = x
    self.y = y                        #width, height
    self.rect = pygame.Rect(self.x, self.y, 32,32)
    self.current_x = (x/32)
    self.current_y = (y/32)
    self.current_pos = (self.current_x,self.current_y)
    self.tmp= ''
    self.collision_dict = adict
    self.enemy_dict = enemydict
    self.npc_dict = npcdict
    self.maxhp = maxhealth
    self.maxmp = maxmana
    self.gold = 0   #you start off broke
    self.incombat = 0
    self.name = 'Isaac'
    self.level = 1
    self.aclass = 'Assassin'
    self.exp = 0
    self.weapon =   [6, "Small Dagger"    ,["Equipment","Weapon"],[1,"Dagger"], [1,0,0,3],  [1,8],  ["A small, yet effective weapon."]]
    self.helmet =   [9,  "Cloth Hat"      ,["Equipment","Helm"], [1, "Cloth"], [0,1,2,3],  [15,8],["Farmhands use these to protect from the sun, and you wanna protect from a sword."]]
    self.armor  =   [12, "Cloth Armor"    ,["Equipment","Chest"],[1, "Cloth"],[0,1,2,2], [15,8], ["Taken from a practice dummy, this hopefully will keep you alive."]]
    self.trinket = [0, "NA"]
  #WHEN YOU ADD TRINKETS UPDATE INVENTORY.PY LINE 217-220
    self.baseattack = 1
    self.basedefence = 1
    self.basespeed = 1
    self.attack = self.baseattack + self.weapon[4][0] #pulls the weapon slot
    self.defence = self.basedefence + self.helmet[4][1] + self.armor[4][1]
    self.maxhp += self.weapon[4][2]+self.helmet[4][2]+self.armor[4][2]
    self.speed = self.basespeed + self.weapon[4][3]
    self.hp = self.maxhp
    self.mp = self.maxmp



  #MOVEMENT etc
  def draw(self,win):
    #COLLISION, COMMENT OUT WHEN DONE
    pygame.draw.rect(win,(255,0,0),self.rect,2)

    #DRAWS OUR CHARACTER
    #win.blit(self.image, (self.x,self.y))
  def move(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      self.pre_move(0,-32)
    elif keys[pygame.K_a]:
      self.pre_move(-32,0)
    elif keys[pygame.K_s]:
      self.pre_move(0,32)
    elif keys[pygame.K_d]:
      self.pre_move(32,0)

  def pre_move(self,newx,newy):
    #update collision boundaries
    self.rect.x += newx
    self.rect.y += newy

    for tile in self.collision_dict:
      obj = self.collision_dict[tile]
      if self.rect.colliderect(obj.rect): #if anything collides in the list
        if newx > 0:
          self.rect.right = obj.rect.left
        if newx < 0 :
          self.rect.left = obj.rect.right
        if newy > 0:
          self.rect.bottom = obj.rect.top
        if newy < 0:
          self.rect.top = obj.rect.bottom

    for npc in self.npc_dict:
        obj = self.npc_dict[npc]
        if self.rect.colliderect(obj.rect): #if anything collides in the list
            if newx > 0:
              self.rect.right = obj.rect.left
            if newx < 0 :
              self.rect.left = obj.rect.right
            if newy > 0:
              self.rect.bottom = obj.rect.top
            if newy < 0:
              self.rect.top = obj.rect.bottom


    self.current_x = self.rect.x /32
    self.current_y = self.rect.y /32
    self.current_pos = (self.current_x,self.current_y)

  def in_combat(self):
    for enemy in self.enemy_dict:
      obj = self.enemy_dict[enemy]
      if self.rect.colliderect(obj.rect):
        self.incombat = 1

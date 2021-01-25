import pygame
from .icons import Icons

all_icons = Icons()
class Inventory():
  def __init__(self,awin,aitemlist,achar,aparty,ainventory):
    self.inventory = ainventory
    self.show_inv = 0
    self.font        = pygame.font.SysFont('Arial',20)
    self.stats_font  = pygame.font.SysFont('Arial',17)
    self.it_font     = pygame.font.SysFont('Arial',18, italic=True )
    self.small_font  = pygame.font.SysFont('Arial',15)
    self.tiny_font   = pygame.font.SysFont('Arial',13)
    self.inv_choice = ['Items','Equipment','Abilities','Status']
    self.nav_menu = 1 # This cycles through the tabs in inventory choice
    self.nav_menu_in = 0 #How deep we are in the inventory 0:no tab, 1: sub tab, 2: interact w/ item, 3: confirming
    self.itemrect = pygame.Rect(135,55,330,380)
    self.submenupos = 0
    self.submenu = []
    self.sub_choice = 0
    self.laste = 0
    self.confirm = 1
    self.yes = 0
    self.no  = 0
    self.win = awin
    self.lasti = 0
    self.item_list = aitemlist
    self.itemcode = 0
    self.char = achar
    self.curr_party_member = 1
    self.party = aparty
    self.equipment_selection = 1
    self.show_equipment_selection = 0
    self.cycle_choice = 1
    self.item_list =[
      [0, "Small Health Potion",["Consumable", "Health"], [1,"Potion"], 10,  [10,5], ["This restores 10 HP to a character."]],
      [1, "Large Health Potion",["Consumable", "Health"], [1,"Potion"], 50,  [25,10],["This restores 50 HP to a character."]],
      [2, "Super Health Potion",["Consumable", "Health"], [1,"Potion"], 100, [50,20],["This restores 100 HP to a character."]],

      [3, "Small Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 10,  [10,5], ["This restores 10 MP to a character."]],
      [4, "Large Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 50,  [25,10], ["This restores 50 MP to a character."]],
      [5, "Super Mana Potion",  ["Consumable", "Mana"], [1,"Potion"], 100, [50,20], ["This restores 100 MP to a character."]],

      [6, "Small Dagger"    ,["Equipment","Weapon"], [1,"Dagger"], [1,0,0,3],  [1,8],  ["A small, yet effective weapon."]],
      [7, "Bronze Sword"    ,["Equipment","Weapon"], [3,"Sword"], [2,1,0,2],  [50,25], ["What squires swing at eachother trying to be knights."]],
      [8, "Iron Sword"      ,["Equipment","Weapon"], [5,"Sword"], [3,1,0,1],  [100,50],["Brave and noble nights wield these."]],

      [9,  "Cloth Hat"      ,["Equipment","Helm"], [1, "Cloth"], [0,1,2,3],  [15,8],["Farmhands use these to protect from the sun, and you wanna protect from a sword."]],
      [10, "Bronze Helm"    ,["Equipment","Helm"], [3, "Plate"], [0,2,3,2],  [50,25],["Made with the finest bronze the local towns have to offer."]],
      [11, "Iron Helm"      ,["Equipment","Helm"], [5, "Plate"],[0,3,5,1],  [75,25], ["Many of these are scattered in deserts."]],


      [12, "Cloth Armor"    ,["Equipment","Chest"],[1, "Cloth"],[0,1,2,2], [15,8], ["Taken from a practice dummy, this hopefully will keep you alive."]],
      [13, "Bronze Armor"   ,["Equipment","Chest"],[3, "Plate"],[0,2,3,1], [50,25],["Guards wear it, and now you!"]],
      [14, "Iron Armor"     ,["Equipment","Chest"],[5, "Plate"],[0,3,5,1], [75,25], ["You can take an arrow to the gut with this and make it away."]]

       ]

  def show_char_stats(self,level_list):
    self.level_list = level_list
    count = 0
    for achar in self.party:
      pygame.draw.rect(self.win, (100,100,100), (self.itemrect.left+2, self.itemrect.top+10+(count*90), 320, 80))
      pygame.draw.rect(self.win, (10,10,10), (self.itemrect.left+5, self.itemrect.top+15+(count*90),70,70))

      party_frame = pygame.Rect(self.itemrect.left+5, self.itemrect.top+10, 320, 80)

      #name
      name = self.stats_font.render(achar.name, False, (255,255,255))
      self.win.blit(name, (party_frame.left+75, party_frame.top+(count*90)+5))

      #class
      charclass = self.it_font.render(achar.aclass, False, (255,255,255))
      self.win.blit(charclass, (party_frame.left+120, party_frame.top+(count*90)+5))

      level = self.small_font.render("lvl   " +str(achar.level), False, (255,255,255))
      self.win.blit(level, (party_frame.right-50, party_frame.top+(count*90)+5))

      #This part is displaying the profile data on our party
      #HP
      currenthp = str(achar.hp)+" / "+str(achar.maxhp) #this basically means 45/50
      hp   = self.small_font.render(currenthp, False,(255,255,255)) #hp
      self.win.blit(hp,             (party_frame.left+100, party_frame.top+(count*90)+27)) #hp text
      self.win.blit(all_icons.hearticon, (party_frame.left+75 , party_frame.top+(count*90)+27)) #hp icon

      #MP
      currentmp = str(achar.mp)+"/"+str(achar.maxmp) #this basically means 45/50
      mp   = self.stats_font.render(currentmp, False,(255,255,255)) #mp
      self.win.blit(mp,            (party_frame.left+100, party_frame.top+(count*90)+52)) #mp text
      self.win.blit(all_icons.manaicon, (party_frame.left+75, party_frame.top+(count*90)+52))

      #EXP
      for level in level_list:
        if level[0]-1 == achar.level: #2-1 = 1,
          xpneeded = level[1] - achar.exp #40-20 = 20 exp needed

      currentxp = "Exp Needed        "+str(xpneeded)#this basically means 45/50
      xp   = self.tiny_font.render(currentxp, False,(255,255,255)) #mp
      self.win.blit(xp,            (party_frame.right-105, party_frame.top+(count*90)+60)) #mp text

      #ATTACK
      currentattack = str(achar.attack)
      attack   = self.stats_font.render(currentattack, False,(255,255,255)) #attack
      self.win.blit(attack,         (party_frame.left+170,party_frame.top+(count*90)+27)) #attack text
      self.win.blit(all_icons.attackicon,(party_frame.left+145 , party_frame.top+(count*90)+27))

      #DEFENCE
      currentdefence = str(achar.defence)
      defence  = self.stats_font.render(currentdefence, False,(255,255,255)) #defence
      self.win.blit(defence,             (party_frame.left+170, party_frame.top+(count*90)+52)) #defence text
      self.win.blit(all_icons.defenceicon,    (party_frame.left+145 , party_frame.top+(count*90)+52))
      count +=1

##    gold = self.stats_font.render("Gila:", False, (255,255,255))
##    currgold = self.stats_font.render(str(achar.gold), False, (255,255,255))
##    self.win.blit(gold, (statsrect.left + 5, statsrect.bottom-25,)) #Gila
##    self.win.blit(currgold, (statsrect.left + 40, statsrect.bottom-25,)) #Gila amount

    #######INVENTORY #################
  def show_inventory(self,canshow):
    if canshow == 1: #establishes dictionary from list
      #DRAW INVENTORY
      pygame.draw.rect(self.win,(100,100,200), (10,10,self.win.get_width()-20,self.win.get_height()-20))#  MAIN INVENTORY SPACE
      #ITEM SPACE
      pygame.draw.rect(self.win, (60,60,60), (122,55,340,370))
      #Show choices:
      self.change_buttons()

  def change_buttons(self):   #THIS IS FOR THE THE TAB BUTTONS
    header = []
    pygame.draw.rect(self.win, (60,60,60),(10,55,110,215))
    for options in range(len(self.inv_choice)):
      if self.nav_menu_in == 0:
        if self.nav_menu == 1: #items
          self.win.blit(all_icons.icon,(15,65))
        if self.nav_menu == 2: #Equipment
          self.win.blit(all_icons.icon,(15,125))
        if self.nav_menu == 3: #misc
          self.win.blit(all_icons.icon,(15,185))
        if self.nav_menu == 4:
          self.win.blit(all_icons.icon,(15,245))
    for aheader in self.inv_choice:
        header.append(self.font.render(aheader,False,(255,255,255)))
    for headers in range(len(header)):
        self.win.blit(header[headers],(31, 60*(headers+1), 130,30))

  def cycle_weapons(self):

    itemDict = {}
    if self.cycle_choice == 1:
        self.win.blit(all_icons.icon, (125,226))
        itemDict = self.update_dict("Equipment","Weapon")
        self.display_equipment(itemDict,"Weapons",self.party[self.curr_party_member])
    if self.cycle_choice == 2:
        self.win.blit(all_icons.icon, (125,256))
        itemDict = self.update_dict("Equipment","Helm")
        self.display_equipment(itemDict,"Helms",self.party[self.curr_party_member])
    if self.cycle_choice == 3:
        self.win.blit(all_icons.icon, (125,286))
        itemDict = self.update_dict("Equipment","Chest")
        self.display_equipment(itemDict,"Armor",self.party[self.curr_party_member])
    if self.cycle_choice == 4:
        self.win.blit(all_icons.icon, (125,316))
        #itemDict = self.update_dict(2,4)
        #display_equipment(itemDict,"Trinkets",self.party[self.curr_party_member])
  def display_equipment(self,adict,aheader,achar):
    textrect = pygame.Rect(290,100,168,320)
    itemList = []
    itemCount = []
    pygame.draw.rect (self.win, (100,100,100), (290,100,168,250))
    iheader = self.font.render(aheader,False,(255,255,255))
    self.win.blit(iheader,(textrect.left+30,textrect.top+2)) #header

    #displays items tab
    equip_count = 0
    acount = 0
    for item in adict:
      #check current pary members gear to see if its equipped
      #print the rest of the inventory
      itemList.append(self.stats_font.render(item,False,(255,255,255)))
      count = ("x "+str(adict[item]))
      itemCount.append(self.stats_font.render(count,False, (255,255,255)))

      if item == achar.weapon[1]:
          equip_count = acount
      acount+=1


    if len(adict) > 0 and self.show_equipment_selection == 1:
        self.win.blit(all_icons.icon,(textrect.left,textrect.top+3+(30*self.equipment_selection)))

    #THIS DISPLAYS THE STUFF IN THE ITEM BOX
    for aItem in range(len(itemList)):
      self.win.blit(itemList [aItem],(textrect.left+30,textrect.top+30+(30*aItem))) #potion of health
      self.win.blit(itemCount[aItem],(textrect.right-25,textrect.top+30+(30*aItem))) # x 1

    self.win.blit(all_icons.equipicon,(textrect.left+14,textrect.top+34+(30*equip_count))) # show equip icon

    if self.nav_menu_in == 4:
        self.compare_weapons(adict,achar)
  
  def compare_weapons(self,adict,achar):
      """
      The purpose of this function is to compare the weapon the user currently
      has to the item its hovered over
      """
      itemList = []
      for item in adict:
          itemList.append(item) #creates tmp list of inventory

      for possibleItems in self.item_list:
        if possibleItems[1] == itemList[self.equipment_selection-1]:  #name of item "small dagger"
          hoveredOver = possibleItems[4]
        else:
          pass

      tmpAttack = achar.baseattack + hoveredOver[0]
      tmpDefence = achar.baseattack + hoveredOver 


     #FROM HERE SHOW THE ARROWS 

  def update_dict(self,acode, atype):
    """
    This just the list of items that are in our inventory. [Potion of health, Potion of health]
    Then transltes to Potion of Health : 2
    Key is the name
    Value is the amount
    acode: EQUIPMENT or CONSUMABLE
    atype: Equipment has Weapon and Armors
    """
    if atype == 1:
        atype = "Weapon"
    elif atype == 2:
        atype = "Helm"
    elif atype == 3:
        atype = "Chest"
    itemDict = {}
    for item in self.inventory: #gets inventory count
      if item[2][0] == acode: #e.g. Equipment
        if item[2][1] == atype: #e.g. Weapon
          if item[1] not in itemDict:
            itemDict[item[1]] = 1
          else:
            itemDict[item[1]] +=1
    return itemDict

  def equipment(self,achar):
    """
    This shows current equipment that they have
    """
    equiprect = pygame.Rect(122,55,340,370)
    description_rect = pygame.Rect(125,354,333,67)
    statsrect = pygame.Rect(10,272,110,153)
    pygame.draw.rect(self.win, (60,60,60), equiprect)
    pygame.draw.rect (self.win, (100,100,100), (125,100,160,250)) #left box
    pygame.draw.rect (self.win, (100,100,100), (290,100,168,250)) #right box
    pygame.draw.rect (self.win, (100,100,100), description_rect) #item description box
    pygame.draw.rect (self.win, (60,60,60), statsrect) #FOR INDIVIDUAL STATS

    char = self.party[self.curr_party_member-1] #we have to index our party member but lists are 0 based
    #Equipment Header
    header = self.font.render("Equipment",False,(255,255,255))
    self.win.blit(header, (equiprect.left+20,equiprect.top+15))
    headername = self.font.render(char.name,False,(255,255,255))
    self.win.blit(headername, (equiprect.left+20, equiprect.top+50))

    #profile picture
    pygame.draw.rect(self.win, (10,10,10), (equiprect.left+20, equiprect.top+80,70,70))

    weapon = self.small_font.render("Weapon: "+char.weapon[1],False,(255,255,255))
    self.win.blit(weapon, (equiprect.left+20,equiprect.top+170))

    helmet= self.small_font.render("Helm : " +char.helmet[1],False,(255,255,255))
    self.win.blit(helmet, (equiprect.left+20,equiprect.top+200))

    armor = self.small_font.render("Armor : " +char.armor[1],False,(255,255,255))
    self.win.blit(armor, (equiprect.left+20,equiprect.top+230))

    trinket = self.small_font.render("Trinket : " +char.trinket[1],False,(255,255,255))
    self.win.blit(trinket, (equiprect.left+20,equiprect.top+260))


    #SHOW CHARACTER STATS

    #attack stat
    self.win.blit(all_icons.attackicon, (statsrect.left+3, statsrect.top+10))
    attackstat = self.small_font.render(str(char.attack), False, (255,255,255))
    self.win.blit(attackstat, (statsrect.left+27,statsrect.top+10))
    #defence stat
    self.win.blit(all_icons.defenceicon, (statsrect.left+3, statsrect.top+32))
    defencestat = self.small_font.render(str(char.defence), False, (255,255,255))
    self.win.blit(defencestat, (statsrect.left+27,statsrect.top+32))
    #speed stat
    self.win.blit(all_icons.speedicon, (statsrect.left+3, statsrect.top+54))
    speedstat = self.small_font.render(str(char.speed), False, (255,255,255))
    self.win.blit(speedstat, (statsrect.left+27,statsrect.top+54))


    #Equipment
    self.cycle_weapons()

  def access_submenu(self,tabchoice):
    """so the submenu relies on constant updates when we use,drop,sell, whatever items. Because of this we need to call
    the dictionary to append to a list so in our menu our current "submenupos" will position in the list with the item.
    for example if we have one item in our inventory, we have [item, value]. If we have 2 potions of health we just want one record in
    our inventory list with a value of 2"""

    #self.submenu = [] #gets current submenu
    #inv = self.update_dict()
    #for item in inv:
      #self.submenu.append([item, inv[item]]) # item, value

    #pygame.draw.rect(self.win, (60,60,60), self.itemrect) #refreshes the background window
    #top  = self.itemrect.top+40
    #left = self.itemrect.left+5
    #self.items()  #redisplay information
    if tabchoice == 2:
      pygame.draw.rect(self.win, (60,60,60), (122,55,340,370))
      self.show_char_stats(self.level_list)
      self.win.blit(all_icons.icon, (self.itemrect.left-13, self.itemrect.top+40 +((self.curr_party_member -1)*90)))

  #def interact_sub_menu(self):
    """Draws submenu text for Use, Drop, and Back on the display screen
    what we are trying to do with #1 is you cant use a sword but you can
    equip it. Same with quest items so we just have to distinguish them
    to change current inventory

    """
    """
    top  = self.itemrect.top+70+(30 * self.submenupos)

    for acode in self.item_list: #[itemcode, itemname, itemusecode]
     if self.submenu[self.submenupos][0] == acode[1]: #if item names are the same
       self.itemcode = acode[2] #then we snag the item

    if self.itemcode == 1: #CONSUMABLE
      action  = self.font.render("Use" ,False,(255,255,255)) #action = use or equip
      self.win.blit(action, (self.itemrect.right-130, top))
    if self.itemcode == 2: #EQUIPMENT
      if self.char.weapon == self.submenu[self.submenupos][0]:
        action  = self.font.render("Unequip" ,False,(255,255,255)) #action = use or equip
      else:
        action  = self.font.render("Equip" ,False,(255,255,255)) #action = use or equip
      self.win.blit(action, (self.itemrect.right-140, top))

    drop    = self.font.render("Drop",False,(255,255,255))
    back    = self.font.render("Back",False ,(255,255,255))

    self.win.blit(drop,(self.itemrect.right-90, top))
    self.win.blit(back,(self.itemrect.right-50, top))

    """

  #def sub_choose(self):
    """
    If the user clicks A or D, scrolls through the avaliable options, paints the text on the new tile when its done
    """
##    top  = self.itemrect.top+70+ (30*self.submenupos)
##    submenurect = pygame.Rect(self.itemrect.right-140,top,130,30)
##    #pygame.draw.rect(self.win,(4,4,4),submenurect) #puts a highlighted box over the current item
##    if self.sub_choice == 0:
##      pygame.draw.rect(self.win, self.select, ((self.itemrect.right-140),top,45,30))
##    if self.sub_choice == 1:
##      pygame.draw.rect(self.win, self.select, ((self.itemrect.right-95) ,top,43,30))
##    if self.sub_choice == 2:
##      pygame.draw.rect(self.win, self.select, ((self.itemrect.right-53) ,top,43,30))
##    self.interact_sub_menu()


  #def reset_drop(self,sc,le,nmi):
    """
    The purpose of this function is to repaint the screen after you drop an item.

    self.subchoice = sc
    self.laste = le
    self.nav_menu_in = nmi
    self.no = 0
    self.yes = 0
    pygame.draw.rect(self.win,(100,100,200), (10,10,self.win.get_width()-20,self.win.get_height()-20))#  MAIN INVENTORY SPACE
    pygame.draw.rect(self.win, (60,60,60), self.itemrect)
    self.access_submenu(self.nav_menu)
    self.items()
    self.change_buttons() #might not need this
    #self.show_char_stats(self.char)
    """

  #def update_inventory(self,akey):
    """
    Subchoice:
    2 is going back, 1 is dropping, 0 is for using
    self.tmp = self.submenu[self.submenupos] #grabs submenu position in the inventory
    if self.sub_choice == 0:  #USE/EQUIP
      if self.itemcode == 1:  #USE
        self.reset_drop(0,0,1)
        if "Health" in self.tmp: #BETA test for health potion
          tmp = self.char.hp + 10
          if tmp > self.char.maxhp:
            self.char.hp = self.char.maxhp
          else:
            self.char.hp += 10
            self.inventory.remove(self.tmp)
      if self.itemcode == 2:
        #self.char.attack += self.itemcode[self.submenupos][3]
        tmp = self.submenu[self.submenupos][0] #Iron sword
        for item in self.item_list:
          if item[1] == tmp:
            self.char.attack += item[4] #add the attack value to our main character
            self.char.weapon = item[1]
            #self.char.attack += item[3] #item 3 is the attack

    if self.sub_choice == 1:
      self.confirm_drop()
      if self.yes == 1:
        for item in self.inventory:
          if item[1] == self.tmp[0]:
            self.inventory.remove(item)
            self.reset_drop(0,0,1)

        if item not in self.inventory:
          self.submenupos = self.submenupos - 1
      if self.no == 1:
        self.reset_drop(1,1,2)

    if self.sub_choice == 2: #BACK
      self.reset_drop(0,0,1)
     """


  #def confirm_drop(self):
    """
    font  = pygame.font.SysFont('Arial',20)
    self.width = (15*32)-20  #THIS NEEDS TO CHANGE IF WE CHANGE RESOLUTION OF GAME
    self.y_pos = 350
    self.x_pos = 10
    self.border = 2
    self.height = 90
    rect = pygame.Rect((self.x_pos+self.border),(self.y_pos+self.border),(self.width-(self.border*2)),(self.height-(self.border *2)))
    message_box = pygame.draw.rect(self.win,(230,230,230), rect)
    dropmessage = ['Are you sure you want to drop: '+ self.tmp[0]+'?']
    newtext = []
    for word in dropmessage:
      newtext.append(self.font.render(word,True,(0,0,0)))
    for line in range(len(newtext)):  #row     #every new row
      self.win.blit(newtext[line],(rect.left+5,rect.top+5+(line*25)))

    yes = self.font.render("Yes",False, (0,0,0))
    no  = self.font.render("No", False, (0,0,0))
    self.win.blit(yes, (rect.right-100, rect.top+40))
    self.win.blit(no , (rect.right-50, rect.top+40))

    if self.confirm == 0:
      self.win.blit(speed, (350,397))
      #circle = pygame.draw.circle(self.win,(255,0,0), (360,405),5,1)
    else:
      #circle = pygame.draw.circle(self.win,(255,0,0), (410,405),5,1)
      self.win.blit(all_icons.icon, (400,397))

 """

  def update(self,akey):
    if self.show_inv == 1: #TAB SECTIONS
        if self.nav_menu_in == 0:
          if akey == 's': #move up an down the sub tabs in inventory
            self.nav_menu = (self.nav_menu % 4) + 1
          if akey == 'w':
            if (self.nav_menu % 4) - 1 == 0:
              self.nav_menu = 4
            else:
              self.nav_menu  = (self.nav_menu) - 1 #    ^^^
          if akey == 'e': #go right into inventory a sub tab
              if self.nav_menu_in == 0 and self.nav_menu == 2: #if we are at EQUIPMENT
                self.nav_menu_in = 1 #then go inside the the subtab

##              else:
##                self.nav_menu_in = 1 #then go inside the the subtab
##                self.submenupos = 0 #initialize current submenu spot to 0 aka the top
##                self.access_submenu(self.nav_menu) #draw menu
        if self.nav_menu_in == 1 and self.laste == 0:   #IF WE ARE IN A SUB TAB like equipment or items
          #EQUIPMENT TAB
          if self.nav_menu == 2:
            if akey == 'q': #backs out
              self.nav_menu_in = 0
            if akey == 'e':
              self.nav_menu_in = 2

        if self.nav_menu_in == 2 and self.laste == 1:
          if self.nav_menu == 2: #equipment again
            if akey == 'q':
              self.nav_menu_in = 0
              self.laste = 0
            if akey == 'e':
              self.nav_menu_in = 3
            if akey == 's':
              self.curr_party_member = self.curr_party_member % (len(self.party))+1
            if akey == 'w':
              if (self.curr_party_member %len(self.party)) - 1 == 0:
                self.curr_party_member = 1
              else:
                self.curr_party_member -=1

        if self.nav_menu_in == 3 and self.laste == 2: #THIS IS FOR EQUIPPING/NOT EQUIPPING
          if self.nav_menu == 2:
              self.equipment(self.curr_party_member) #ACCESS THE EQUIPMENT MENU
              if akey == 'q':
                  self.nav_menu_in = 2
                  self.laste = 1
              if akey == 's':
                  self.cycle_choice = (self.cycle_choice % 4) +1
              if akey == 'w':
                  if (self.cycle_choice % 4) - 1 == 0:
                    self.cycle_choice = 1
                  else:
                    self.cycle_choice -=1
              if akey == 'e':
                  tmp = len(self.update_dict("Equipment",self.cycle_choice)) #you cant access a menu with items you dont have, this checks to make sure you have at lEAST 1
                  if tmp > 0:
                    self.nav_menu_in = 4

        if self.nav_menu_in == 4 and self.laste == 3:
          if self.nav_menu == 2:
              #self.show_equipment_selection = 1
              #self.cycle_weapons()
              #self.show_equipment_selection = 1
              if akey == 'q':
                self.nav_menu_in = 3
                self.laste = 2
                self.show_equipment_selection = 0
                self.equipment_selection = 1
              tmp = len(self.update_dict("Equipment",self.cycle_choice))


              #COMPARE WEAPON JAZZ HERE


              if akey == 's': #cycle down
                #equipment selection starts at 1
                if (self.equipment_selection  + 1) == tmp:
                    self.equipment_selection = tmp
                elif self.equipment_selection < tmp:
                      self.equipment_selection +=1

              if akey == 'w':
                if (self.equipment_selection % tmp) -1  == 0:
                  self.equipment_selection = 1
                elif self.equipment_selection>1 :
                  self.equipment_selection-=1
              if akey == 'e':
                  self.nav_menu_in = 5

              print(self.equipment_selection)
        if self.nav_menu_in == 5 and self.laste == 4:
            pass







##          inv = self._dict()
##          if len(inv) > 0:
##            if akey == 'a': #if we are already in a tab
##              self.nav_menu_in = 0 #then go back to the main menu
##
##            if akey == 's':#if we are already in a subtab and we hit S,
##              if len(inv) == 1:
##                self.submenupos = 0
##              else:
##                self.submenupos = (self.submenupos % (len(inv)-1))+1
##              self.access_submenu(self.nav_menu)
##
##            if akey == 'w':#if we are already in a subtab and we hit S,
##              if len(inv) == 1:
##                self.submenupos = 0
##              if (self.submenupos % len(inv))-1 == -1:
##                self.submenupos = 0
##              else:
##                self.submenupos = (self.submenupos % len(inv))-1
##              self.access_submenu(self.nav_menu)
##
##            if akey == 'e':
##              self.nav_menu_in = 2
##          else:
##            self.nav_menu_in = 0
##
##        if self.nav_menu_in == 2 and self.laste == 1:
##          self.interact_sub_menu()
##          if akey == 'a':
##            if self.sub_choice == 0:
##              pass
##            else:
##              self.sub_choice -=1
##          if akey == 'd':
##            if self.sub_choice == 2:
##              pass
##            else:
##              self.sub_choice +=1
##          self.sub_choose()
##          #this will adjust the menu so they can cycle between "Use,Drop,Back"
##          if akey == 'e':
##            if self.sub_choice == 0 or self.sub_choice == 2:
##              self.update_inventory()
##            elif self.sub_choice == 1: # drop
##              self.nav_menu_in = 3
##
##        #THIS IS FOR CONFIRMING DROPPING
##        if self.nav_menu_in == 3 and self.laste == 2:
##          self.confirm_drop()
##          if akey == 'a':
##            if self.confirm == 0:
##              pass
##            else:
##              self.confirm -=1
##          if akey == 'd':
##            if self.confirm == 1:
##              pass
##            else:
##              self.confirm +=1
##          if akey == 'e' and self.confirm == 1:
##            self.no = 1
##          if akey == 'e' and self.confirm == 0:
##            self.yes = 1
##
##

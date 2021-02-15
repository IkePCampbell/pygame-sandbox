import pygame
from .message import MessageBox
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
    self.nav_menu_in = 0 #How deep we are in the inventory 
    self.itemrect = pygame.Rect(135,55,330,380)
    self.submenupos = 0
    self.submenu = []
    self.sub_choice = 0
    self.laste = 0
    self.lasti = 0
    self.confirm = 0
    self.win = awin
    self.item_list = aitemlist
    self.itemcode = 0
    self.char = achar
    self.curr_party_member = 1
    self.party = aparty
    self.equipment_selection = 1
    self.show_equipment_selection = 0
    self.cycle_choice = 1
    self.invAttr = []
    self.tmpAttr =[]
    self.WHITE_COLOR=(255,255,255)
    self.RED_COLOR=(255,0,0)
    self.GREEN_COLOR=(0,255,0)
    self.inventoryChoice = 0
    self.holding_equip = False
    self.item_selection = 1
    self.itemDict = {}

  def show_char_stats(self,level_list):
    self.level_list = level_list
    count = 0
    for achar in self.party:
      pygame.draw.rect(self.win, (100,100,100), (self.itemrect.left+2, self.itemrect.top+10+(count*90), 320, 80))
      pygame.draw.rect(self.win, (10,10,10), (self.itemrect.left+5, self.itemrect.top+15+(count*90),70,70))

      party_frame = pygame.Rect(self.itemrect.left+5, self.itemrect.top+10, 320, 80)

      #name
      name = self.stats_font.render(achar.name, True, (255,255,255))
      self.win.blit(name, (party_frame.left+75, party_frame.top+(count*90)+5))

      #class
      charclass = self.it_font.render(achar.aclass, True, (255,255,255))
      self.win.blit(charclass, (party_frame.left+120, party_frame.top+(count*90)+5))

      level = self.small_font.render("lvl   " +str(achar.level), True, (255,255,255))
      self.win.blit(level, (party_frame.right-50, party_frame.top+(count*90)+5))

      #This part is displaying the profile data on our party
      #HP
      currenthp = str(achar.hp)+" / "+str(achar.maxhp) #this basically means 45/50
      hp   = self.small_font.render(currenthp, True,(255,255,255)) #hp
      self.win.blit(hp,             (party_frame.left+100, party_frame.top+(count*90)+27)) #hp text
      self.win.blit(all_icons.hearticon, (party_frame.left+75 , party_frame.top+(count*90)+27)) #hp icon

      #MP
      currentmp = str(achar.mp)+"/"+str(achar.maxmp) #this basically means 45/50
      mp   = self.stats_font.render(currentmp, True,(255,255,255)) #mp
      self.win.blit(mp,            (party_frame.left+100, party_frame.top+(count*90)+52)) #mp text
      self.win.blit(all_icons.manaicon, (party_frame.left+75, party_frame.top+(count*90)+52))

      #EXP
      for level in level_list:
        if level[0]-1 == achar.level: #2-1 = 1,
          xpneeded = level[1] - achar.exp #40-20 = 20 exp needed

      currentxp = "Exp Needed      "+str(xpneeded)#this basically means 45/50
      xp   = self.tiny_font.render(currentxp, True,(255,255,255)) #mp
      self.win.blit(xp,            (party_frame.right-115, party_frame.top+(count*90)+60)) #mp text

      #ATTACK
      currentattack = str(achar.attack)
      attack   = self.stats_font.render(currentattack, True,(255,255,255)) #attack
      self.win.blit(attack,         (party_frame.left+170,party_frame.top+(count*90)+27)) #attack text
      self.win.blit(all_icons.attackicon,(party_frame.left+145 , party_frame.top+(count*90)+27))

      #DEFENCE
      currentdefence = str(achar.defence)
      defence  = self.stats_font.render(currentdefence, True,(255,255,255)) #defence
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
          self.win.blit(all_icons.icon,(15,62))
        if self.nav_menu == 2: #Equipment
          self.win.blit(all_icons.icon,(15,122))
        if self.nav_menu == 3: #Abilities
          self.win.blit(all_icons.icon,(15,182))
        if self.nav_menu == 4: #Status
          self.win.blit(all_icons.icon,(15,242))
    for aheader in self.inv_choice:
        header.append(self.stats_font.render(aheader,True,(255,255,255)))
    for headers in range(len(header)):
        self.win.blit(header[headers],(31, 60*(headers+1), 130,30))

  def cycle_weapons(self):
    itemDict = {}
    if self.cycle_choice == 1:
        self.win.blit(all_icons.icon, (125,226))
        itemDict = self.update_dict("Equipment","Weapon")
        self.display_equipment(itemDict,"Weapons",self.party[self.curr_party_member-1])
    if self.cycle_choice == 2:
        self.win.blit(all_icons.icon, (125,256))
        itemDict = self.update_dict("Equipment","Helm")
        self.display_equipment(itemDict,"Helms",self.party[self.curr_party_member-1])
    if self.cycle_choice == 3:
        self.win.blit(all_icons.icon, (125,286))
        itemDict = self.update_dict("Equipment","Chest")
        self.display_equipment(itemDict,"Armor",self.party[self.curr_party_member-1])
    if self.cycle_choice == 4:
        self.win.blit(all_icons.icon, (125,316))
        #itemDict = self.update_dict(2,4)
        #display_equipment(itemDict,"Trinkets",self.party[self.curr_party_member])
  def display_equipment(self,adict,aheader,achar):
    self.holding_equip = False
    textrect = pygame.Rect(290,100,168,320)
    itemList = []
    itemCount = []
    pygame.draw.rect (self.win, (100,100,100), (290,100,168,250))
    iheader = self.font.render(aheader,True,(255,255,255))
    self.win.blit(iheader,(textrect.left+30,textrect.top+2)) #header

    #displays items tab
    equip_count = 0
    wep_c = 0
    hel_c = 0
    arm_c = 0
    for item in adict:
      #check current pary members gear to see if its equipped
      #print the rest of the inventory
      itemList.append(self.stats_font.render(item,True,(255,255,255)))
      count = ("x "+str(adict[item]))
      itemCount.append(self.stats_font.render(count,True, (255,255,255)))

      if item == achar.weapon[1]:
        equip_count = wep_c
      wep_c+=1

      if item == achar.helmet[1]:
        equip_count = hel_c
      hel_c+=1

      if item == achar.armor[1]:
        equip_count = arm_c
      arm_c+=1

    if len(adict) > 0 and self.show_equipment_selection == 1:
        self.win.blit(all_icons.icon,(textrect.left,textrect.top+3+(30*self.equipment_selection)))

    #THIS DISPLAYS THE STUFF IN THE ITEM BOX
    for aItem in range(len(itemList)):
      self.win.blit(itemList [aItem],(textrect.left+30,textrect.top+30+(30*aItem))) #potion of health
      self.win.blit(itemCount[aItem],(textrect.right-25,textrect.top+30+(30*aItem))) # x 1

    if aheader == "Weapons":
      if achar.weapon[1] != "Fists":
        self.win.blit(all_icons.equipicon,(textrect.left+14,textrect.top+34+(30*equip_count))) # show equip icon
    
    if aheader == "Armor":
      if achar.armor[1] != "Nothing":
        self.win.blit(all_icons.equipicon,(textrect.left+14,textrect.top+34+(30*equip_count))) # show equip icon
    
    if aheader == "Helms":
      if achar.helmet[1] != "Nothing":
        self.win.blit(all_icons.equipicon,(textrect.left+14,textrect.top+34+(30*equip_count))) # show equip icon
    if self.nav_menu_in == 4:  
      itemList = []
      self.count = 0
      for item in adict:
          itemList.append(item) #creates tmp list of inventory
      for possibleItems in self.item_list:
        self.count +=1
        if possibleItems[1] == itemList[self.equipment_selection-1]:  #name of item "small dagger"
          hoveredOver = possibleItems[4]
          typeOfEquipment = possibleItems[2][1]
          self.itemDetails = [possibleItems[2][0],possibleItems[1]]
          self.indexItem  = self.count -1
          tmpWep = possibleItems
      
      if typeOfEquipment == "Chest":
        tmpDefence =  achar.basedefence + achar.helmet[4][1] + hoveredOver[1] + achar.weapon[4][1]
        tmpSpeed = achar.basespeed + achar.helmet[4][3]+ hoveredOver[3] + achar.weapon[4][3]
        tmpAttack = achar.baseattack + achar.helmet[4][0] + hoveredOver[0]+ achar.weapon[4][0]
      elif typeOfEquipment == "Helm":
        tmpDefence =  achar.basedefence + achar.armor[4][1] + hoveredOver[1] + achar.weapon[4][1]
        tmpSpeed = achar.basespeed + achar.armor[4][3]+ hoveredOver[3] + achar.weapon[4][3]
        tmpAttack = achar.baseattack + achar.armor[4][0] + hoveredOver[0] + achar.weapon[4][0]
      #Meaning we are attempting to equip a weapon
      else:
        tmpDefence = achar.basedefence + achar.helmet[4][1] + achar.armor[4][1] + hoveredOver[1]
        tmpSpeed =  achar.basespeed + achar.helmet[4][3]+ achar.armor[4][3]+ hoveredOver[3]
        tmpAttack = achar.baseattack + achar.helmet[4][0]+ achar.armor[4][0] + hoveredOver[0]

      description_rect = pygame.Rect(125,354,333,67)
      pygame.draw.rect (self.win, (100,100,100), description_rect) #item description box
      self.show_description(None,tmpWep)
      self.tmpAttr = [tmpAttack,tmpDefence,tmpSpeed]
      self.inventory_side_stats()



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
    pygame.draw.rect(self.win, (60,60,60), equiprect)
    pygame.draw.rect (self.win, (100,100,100), (125,100,160,250)) #left box
    pygame.draw.rect (self.win, (100,100,100), (290,100,168,250)) #right box
    pygame.draw.rect (self.win, (100,100,100), description_rect) #item description box

    char = self.party[self.curr_party_member-1] #we have to index our party member but lists are 0 based
    #Equipment Header
    header = self.font.render("Equipment",True,(255,255,255))
    self.win.blit(header, (equiprect.left+20,equiprect.top+15))
    headername = self.font.render(char.name,True,(255,255,255))
    self.win.blit(headername, (equiprect.left+20, equiprect.top+50))

    #profile picture
    pygame.draw.rect(self.win, (10,10,10), (equiprect.left+20, equiprect.top+80,70,70))

    weapon = self.small_font.render("Weapon: "+char.weapon[1],True,(255,255,255))
    self.win.blit(weapon, (equiprect.left+20,equiprect.top+170))

    helmet= self.small_font.render("Helm : " +char.helmet[1],True,(255,255,255))
    self.win.blit(helmet, (equiprect.left+20,equiprect.top+200))

    armor = self.small_font.render("Armor : " +char.armor[1],True,(255,255,255))
    self.win.blit(armor, (equiprect.left+20,equiprect.top+230))

    trinket = self.small_font.render("Trinket : " +char.trinket[1],True,(255,255,255))
    self.win.blit(trinket, (equiprect.left+20,equiprect.top+260))

    self.inventory_side_stats()

    self.cycle_weapons()
    self.show_description(char,None)

  def inventory_side_stats(self):
    statsrect = pygame.Rect(10,272,110,153)
    pygame.draw.rect (self.win, (60,60,60), statsrect) #FOR INDIVIDUAL STATS
    char = self.party[self.curr_party_member-1] #we have to index our party member but lists are 0 based
    #Reset everytime we attempt to compare

    self.invAttr=[char.attack,char.defence,char.speed]
    #Means we are comparing if the list is greater than 1
    if len(self.tmpAttr) >= 1:
      for i in range(len(self.invAttr)):
        if self.tmpAttr[i] > self.invAttr[i]:
          color = self.GREEN_COLOR
        if self.tmpAttr[i] < self.invAttr[i]:
          color = self.RED_COLOR
        if self.tmpAttr[i] == self.invAttr[i]:
          color = self.WHITE_COLOR
        stat = self.small_font.render(str(self.tmpAttr[i]), True, (color))
        self.win.blit(stat, (statsrect.left+27,statsrect.top+(10+(22*i))))
      self.tmpAttr =[]
    else:
      for i in range(len(self.invAttr)):
        stat = self.small_font.render(str(self.invAttr[i]), True, self.WHITE_COLOR)
        self.win.blit(stat, (statsrect.left+27,statsrect.top+(10+(22*i))))

    self.win.blit(all_icons.attackicon, (statsrect.left+3, statsrect.top+10))
    self.win.blit(all_icons.defenceicon, (statsrect.left+3, statsrect.top+32))
    self.win.blit(all_icons.speedicon, (statsrect.left+3, statsrect.top+54))

  def access_submenu(self,tabchoice):
    """so the submenu relies on constant updates when we use,drop,sell, whatever items. Because of this we need to call
    the dictionary to append to a list so in our menu our current "submenupos" will position in the list with the item.
    for example if we have one item in our inventory, we have [item, value]. If we have 2 potions of health we just want one record in
    our inventory list with a value of 2"""
    if tabchoice == 2:
      pygame.draw.rect(self.win, (60,60,60), (122,55,340,370))
      self.show_char_stats(self.level_list)
      self.win.blit(all_icons.icon, (self.itemrect.left-13, self.itemrect.top+40 +((self.curr_party_member -1)*90)))

  def interact_sub_menu(self,akey):
    """Draws submenu text for Use, Drop, and Back on the display screen
    what we are trying to do with #1 is you cant use a sword but you can
    equip it. Same with quest items so we just have to distinguish them
    to change current inventory
    """

    top  = self.itemrect.top+300
    interactMenu = pygame.Rect(250,350,210,75)
    pygame.draw.rect (self.win, (230,230,230), interactMenu) 
    if self.itemDetails[0] == "Equipment":
      if (self.char.weapon[1] == self.itemDetails[1] or
          self.char.helmet[1] == self.itemDetails[1] or
          self.char.armor[1]  == self.itemDetails[1]): #if it's same weapon
        action ="UnEquip"
      else:
        action = "Equip"
      self.action = action
    words = [action,"Drop","Back"]
    newtext = []
    for word in words:
      if word == "Drop" and action == "UnEquip":
          newtext.append(self.stats_font.render(word,True,(100,100,100)))
          self.holding_equip = True
      elif word == "Drop" and action == "Action":
          self.holding_equip = False
      else:
          newtext.append(self.stats_font.render(word,True,(0,0,0)))

    for line in range(len(newtext)):  #row     #every new row
      self.win.blit(newtext[line],(interactMenu.left+25,interactMenu.top+5+(line*25)))
    #Actual icon tab  
    self.win.blit(all_icons.icon,(253,355+(self.inventoryChoice*25)))

  def sub_choose(self):
    """
    If the user clicks A or D, scrolls through the avaliable options, paints the text on the new tile when its done
    """
    top  = self.itemrect.top+70+ (30*self.submenupos)
    submenurect = pygame.Rect(self.itemrect.right-140,top,130,30)
    pygame.draw.rect(self.win,(4,4,4),submenurect) #puts a highlighted box over the current item
    if self.sub_choice == 0:
      pygame.draw.rect(self.win, self.select, ((self.itemrect.right-140),top,45,30))
    if self.sub_choice == 1:
      pygame.draw.rect(self.win, self.select, ((self.itemrect.right-95) ,top,43,30))
    if self.sub_choice == 2:
      pygame.draw.rect(self.win, self.select, ((self.itemrect.right-53) ,top,43,30))
    self.interact_sub_menu()

  def show_description(self,achar,aweapon):
    equipMenu = pygame.Rect(125,354,333,67)
    txt = ""
    if aweapon != None:
      txt = aweapon[6]

    #Not individual item selection
    if self.nav_menu_in == 3:
      if self.cycle_choice == 1:
        txt = achar.weapon[6]
      elif self.cycle_choice == 2:
        txt = achar.helmet[6]
      elif self.cycle_choice == 3:
        txt = achar.armor[6]
    finishedText = []
    for word in txt:
      finishedText.append(self.small_font.render(word,True,self.WHITE_COLOR))
    for line in range(len(finishedText)):  #row     #every new row
      self.win.blit(finishedText[line],(equipMenu.left+5,equipMenu.top+5+(line*25)))
  
  def drop(self):
    if self.equipment_selection >= 1:
      self.equipment_selection-=1
    self.inventory.remove(self.item_list[self.indexItem])

  def confirm_drop(self):
    dropMenu = pygame.Rect(125,240,333,67)
    message_box = pygame.draw.rect(self.win,(230,230,230), dropMenu)
    dropmessage = ['Drop: '+ self.item_list[self.indexItem][1] +'?']
    newtext = []
    for word in dropmessage:
      newtext.append(self.small_font.render(word,True,(0,0,0)))
    for line in range(len(newtext)):  #row     #every new row
      self.win.blit(newtext[line],(dropMenu.left+5,dropMenu.top+5+(line*25)))

    yes = self.small_font.render("Yes",True, (0,0,0))
    no  = self.small_font.render("No", True, (0,0,0))
    self.win.blit(yes, (dropMenu.right-150, dropMenu.top+40))
    self.win.blit(no , (dropMenu.right-50, dropMenu.top+40))

    if self.confirm == 1:
      self.win.blit(all_icons.icon, (dropMenu.right-170,dropMenu.top+40))  
    else:
      self.win.blit(all_icons.icon, (dropMenu.right-70,dropMenu.top+40))

  def display_items(self):
    self.itemDict = {}
    for item in self.inventory: #gets inventory count
      if item[2][0] == "Item": #e.g. Equipment
        if item[1] not in self.itemDict:
          self.itemDict[item[1]] = 1
        else:
          self.itemDict[item[1]] +=1
    
    equiprect = pygame.Rect(122,55,340,370)
    description_rect = pygame.Rect(125,354,333,67)
    pygame.draw.rect(self.win, (60,60,60), equiprect)
    header = self.font.render("Items",True,(255,255,255))
    self.win.blit(header, (equiprect.left+20,equiprect.top+15))
    pygame.draw.rect (self.win, (100,100,100), (125,100,335,250)) #left box
    pygame.draw.rect (self.win, (100,100,100), description_rect) #item description box
    #Actually display items
    itemList = []
    itemCount = []
    for item in self.itemDict:
      itemList.append(self.stats_font.render(item,True,(255,255,255)))
      count = ("x "+str(self.itemDict[item]))
      itemCount.append(self.stats_font.render(count,True, (255,255,255)))
    
    if len(self.itemDict) > 0 and self.item_selection >= 1:
      self.win.blit(all_icons.icon,(equiprect.left,equiprect.top+33+(30*self.item_selection)))
    for aItem in range(len(itemList)):
      self.win.blit(itemList [aItem],(equiprect.left+30,equiprect.top+60+(30*aItem))) #potion of health
      self.win.blit(itemCount[aItem],(equiprect.right-40,equiprect.top+60+(30*aItem))) # x 1

  def update(self,akey):
    if self.show_inv == 1: #TAB SECTIONS
      if self.nav_menu_in == 0:
        if akey == 's': #move up an down the sub tabs in inventory
          self.nav_menu = (self.nav_menu % 4) + 1
        if akey == 'w':
          self.nav_menu = 4 if (self.nav_menu % 4) - 1 == 0 else (self.nav_menu) - 1
        if akey == 'e': #go right into inventory a sub tab
          if self.nav_menu_in == 0 and self.nav_menu in [1,2,3,4]:
            self.nav_menu_in = 1 
        if akey == 'q':
          self.show_inv = 0

      if self.nav_menu_in == 1 and self.laste == 0:   #IF WE ARE IN A SUB TAB like equipment or items
        if akey == 'q':
          self.nav_menu_in = 0
        if akey == 'e':
          self.nav_menu_in = 2

      if self.nav_menu_in == 2 and self.laste == 1:
        if akey == 'q':
          self.nav_menu_in = 0
          self.laste = 0

        if self.nav_menu == 1:
          #Now need to cycle through every item
          if akey == 's':
            self.item_selection = self.item_selection % (len(self.itemDict))+1
          if akey == 'w':
            if (self.item_selection %len(self.itemDict)) - 1 >=1:
              self.item_selection -=1

        if self.nav_menu == 2: #equipment again
          self.curr_party_member = 1
          if akey == 'e':
            self.nav_menu_in = 3
          if akey == 's':
            self.curr_party_member = self.curr_party_member % (len(self.party))+1
          if akey == 'w':
            if (self.curr_party_member %len(self.party)) - 1 >=1:
              self.curr_party_member -=1

      if self.nav_menu_in == 3 and self.laste == 2: 
          if self.nav_menu == 2:
              self.equipment(self.curr_party_member) #ACCESS THE EQUIPMENT MENU
              if akey == 'q':
                  self.nav_menu_in = 2
                  self.laste=1
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
            if akey == 'q':
              self.nav_menu_in = 3
              self.laste = 2
              self.show_equipment_selection = 0
              self.equipment_selection = 1
            tmp = len(self.update_dict("Equipment",self.cycle_choice))

            if akey == 's': #cycle down
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
              self.laste = 4
      #Selecting an item to equip
      if self.nav_menu_in == 5 and self.laste == 4:
        if akey == 'q':
          self.nav_menu_in = 4
          self.laste = 3
        if akey =='e':
          self.nav_menu_in = 6
          self.laste = 5

      #Equip, drop, use item
      if self.nav_menu_in == 6 and self.laste in [5,6]:
        if self.nav_menu == 2:
          if akey == 'q':
            self.nav_menu_in = 4
            self.laste = 3
            self.inventoryChoice = 0
          if akey == 's': #cycle down
            self.inventoryChoice = (self.inventoryChoice  + 1) % 3
          if akey == 'w':
            self.inventoryChoice = (self.inventoryChoice  - 1) % 3
          if akey == 'e' and self.laste == 5:
            self.laste = 6
          elif akey == 'e' and self.laste == 6 and self.inventoryChoice == 0:
            #Un/Equip Weapon
            self.party[self.curr_party_member-1].equipGear(self.item_list[self.indexItem],self.action)
            self.laste = 3
            self.nav_menu_in = 4
            self.inventoryChoice = 0
          elif akey == 'e' and self.laste == 6 and self.inventoryChoice == 1 and self.holding_equip == False:
            self.laste = 7
            self.nav_menu_in = 7
          elif akey == 'e' and self.laste == 6 and self.inventoryChoice == 2:
            self.nav_menu_in = 4
            self.laste = 3
            self.inventoryChoice = 0

      if self.nav_menu_in == 7 and self.laste in [7,8]:
        self.confirm_drop()
        if akey == 'q':
          self.nav_menu_in = 6
          self.laste = 6
          self.confirm = 0
        if akey == 'a':
          self.confirm = 1
        if akey == 'd':
          self.confirm = 0
        if akey == 'e' and self.laste == 7:
          self.laste = 8
        elif akey == 'e' and self.laste == 8 and self.confirm == 0:
          self.nav_menu_in = 6
          self.laste = 6
        elif akey == 'e' and self.laste == 8 and self.confirm == 1:
          self.drop()
          #Check to see if we've emptied inv
          if self.equipment_selection == 0:
            self.nav_menu_in = 3
            self.laste=2
            self.equipment_selection = 1
          else:
            self.nav_menu_in = 4
            self.laste = 3
            self.confirm = 0
      
      #Will need to confirm the drops

#Inventory update helper functions          
  def inventory_menu_helper(self,menu_in,laste):
    self.nav_menu_in = menu_in
    self.laste = laste
          

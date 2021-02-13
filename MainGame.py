import pygame
import sys #access system
import time
import os
#import from bin
from data.bin.tile import Tile
from data.bin.message import MessageBox
from data.bin.inventory import Inventory
from data.bin.mobs import *
from data.bin.combat import Combat
from data.bin.mainchar import Main_Player
from data.bin.chest import Chest
from data.bin.npc import Merchant
from data.bin.icons import Icons
from data.bin.item_list import AllItems
from data.bin.floor_plans import Floors
os.environ['SDL_VIDEO_CENTERED'] = '1' #this sets the window
pygame.init() #initializes pygame, always need to have this

main_path = os.path.dirname('MainGame')
image_path = os.path.join(main_path, 'data\sprites\obj')

#establishes fps
clock = pygame.time.Clock()
run = True
all_icons = Icons()
#Tile Dimensions
class GAMEFRAME:
  def __init__(self, MAP_X,MAP_Y,TILESIZE):
    self.MAP_X = MAP_X
    self.MAP_Y = MAP_Y
    self.SIZE = TILESIZE
    self.win = pygame.display.set_mode((MAP_X*self.SIZE,MAP_Y*self.SIZE)) #window sizes
    pygame.display.set_caption("Game_Name") #window name

    #ALL IMAGE STUFF HAPPENS HERE

    self.collision_dict = {}
    self.party = []
    self.enemy_dict = {}
    self.npc_dict = {}
    self.chest_dict = {}
    self.item_list = AllItems().item_list
    self.levels = [Floors().level1,Floors().level2]
    self.currentLevelMap = self.levels[0][0]
    self.currentLevel = self.levels[0][1]
    self.zone_change = Floors().areaSwitchArea
    self.npcList = []

    self.level_list = [
      [2,40], #level, amount to next level
      [3,120]
      ]

    self.chest_rewards = [
      [(3,3), 6,1,False],
      [(11,3),7,1,False],
      [(6,3) ,8,1,False],
      [(3,3),8,2,False]
    ]
    self.zoneChangeSpots = []
  def getZoneChangePlaces(self):
      for row in range(len(self.currentLevelMap)):
        for height in range(len(self.currentLevelMap[row])):
            if self.currentLevelMap[row][height] == 5:
                self.zoneChangeSpots.append((height,row))
      #if intentional, set self.calcZoneChange to false

  def areaSwitch(self,char):
    for i in range(len(self.zone_change)):
      if char.current_pos == self.zone_change[i][0] and self.currentLevel == self.zone_change[i][1][1]:
        self.currentLevelMap = self.zone_change[i][3][0]
        self.currentLevel = self.zone_change[i][3][1]
        char.current_pos = self.zone_change[i][2]
        char.current_x = self.zone_change[i][2][1]
        char.current_y = self.zone_change[i][2][0]
        char.x = self.zone_change[i][2][1] * 32
        char.y = self.zone_change[i][2][0] * 32
        char.rect = pygame.Rect(char.x, char.y, 32,32)
        self.zoneChangeSpots = []

  def update_npc_coll(self,npcList,char):
    self.enemy_dict = {}
    self.npc_dict = {}
    for i in range(len(npcList)):
      if npcList[i].map == self.currentLevel:
        if npcList[i].name != "NPC":
          self.enemy_dict["mob"+str(i)] = npcList[i]
        else:
          self.npc_dict["NPC"+str(i)] =npcList[i]
    char.enemy_dict = self.enemy_dict
    char.npc_dict = self.npc_dict



  def draw_tiles(win,levelList,collide_dict):
    #loops through every row and column in our level list
    for row in range(GAME.MAP_Y):
      for height in range(GAME.MAP_X):
        if levelList[row][height] == 0: #WALL
          image = all_icons.wall
        if levelList[row][height] in [1,5]: #FLOOR
          image = all_icons.floor
        
        #GET COLLISION BOUNDARIES
        image_rect = image.get_rect()
        image_rect.topleft = (height * image_rect.width,
                              row    * image_rect.height)
        #position of tile
        new_x = height*GAME.SIZE
        new_y = row   *GAME.SIZE

        GAME.win.blit(image,(new_x,new_y,GAME.SIZE,GAME.SIZE)) #draw basic chest

        #DICT FOR TILES COLLISION ETC KEEP OR INFINITE LOOP AND NO MEMORY
        tc = (row, height)
        if levelList[row][height] == 0:
          if tc not in collide_dict:
            newTile = Tile(new_x,new_y)
            collide_dict[tc,'WALL'] = newTile
          GAME.win.blit(image,(new_x,new_y,GAME.SIZE,GAME.SIZE)) #draw walls

        if levelList[row][height] == 3: #CHEST
          if tc not in collide_dict:
            newChest = Chest(new_x,new_y,0,GAME.currentLevel)
            collide_dict[tc]   = newChest

          if tc not in GAME.chest_dict:
            for chest_reward in GAME.chest_rewards:
              if chest_reward[0] == tc and chest_reward[2] == GAME.currentLevel and chest_reward[3] == False:
                newChest = Chest(new_x,new_y,0,GAME.currentLevel)
              elif chest_reward[0] == tc and chest_reward[2] == GAME.currentLevel and chest_reward[3] == True:
                newChest = Chest(new_x,new_y,1,GAME.currentLevel) 
              GAME.chest_dict[tc]= [newChest,newChest.openpos]
              GAME.win.blit(image,(new_x,new_y,GAME.SIZE,GAME.SIZE)) #draw basic chest

          if tc in GAME.chest_dict:
            for chest in GAME.chest_dict:
              image = GAME.chest_dict[chest][0].update(main_char,message,GAME,inventory)
              GAME.win.blit(image,(GAME.chest_dict[chest][0].x, \
                                   GAME.chest_dict[chest][0].y, \
                                   GAME.SIZE,\
                                   GAME.SIZE)) #draw basic chest




########################## INSTANCES #########
#INITIALIZE GAME
GAME = GAMEFRAME(15,14,32)
#Starting Inventory
start_inventory = [
  GAME.item_list[0],
  GAME.item_list[3],
  GAME.item_list[6],
  GAME.item_list[8],
  GAME.item_list[9],
  GAME.item_list[10],     
  GAME.item_list[12],      ]

tier1_consumables = [
  GAME.item_list[0],
  GAME.item_list[3],
                     ]
tier1_gear = [
  GAME.item_list[9],
  GAME.item_list[12]
      ]

tier1_weapons = [
  GAME.item_list[6],
 ]

akey = ''


#max length per line, 50 chars   USE THIS ['',''] FORMAT
message = MessageBox('',0,GAME.win, GAME.MAP_X, GAME.SIZE)
#instance              #x,   y
main_char = Main_Player(64,64,GAME.collision_dict,GAME.enemy_dict,GAME.npc_dict,25,10)
inventory = Inventory(GAME.win,GAME.item_list,main_char,GAME.party,start_inventory)
bat1 = Bat(1,10,1,1,10,6,6,1)
bat2 = Bat(1,10,1,1,10,9,9,1)
bat3 = Bat(1,10,1,1,10,11,11,2)
merchant1 = Merchant(5,3,tier1_consumables,2,1,"NPC","Harold")
combat = Combat()
###############################################
enemies = [bat1,bat2,bat3]
npcs = [merchant1]
GAME.npcList = enemies + npcs
GAME.update_npc_coll(GAME.npcList,main_char)
GAME.party.append(main_char)

#always want drawing to be done in one area, anytime i redraw it needs to be here
def update_screen():
  keys = pygame.key.get_pressed()
  if message.show == 0 and \
    inventory.show_inv == 0 and \
    inventory.nav_menu_in == 0 and \
    main_char.incombat == 0:

    GAME.win.fill((0,0,0)) #ALWAYS KEEP THIS
    #
    if len(GAME.zoneChangeSpots) == 0:
      GAME.getZoneChangePlaces()  
    if main_char.current_pos in GAME.zoneChangeSpots:
      GAME.areaSwitch(main_char)
      GAME.collision_dict = {}
      GAME.chest_dict = {}
      main_char.collision_dict = {}
      main_char.enemy_dict = {}
      GAME.update_npc_coll(GAME.npcList,main_char)

    GAME.draw_tiles(GAME.currentLevelMap,GAME.collision_dict)
    main_char.collision_dict = GAME.collision_dict
    main_char.move(GAME.zoneChangeSpots)
    #Move Zones here, update new pos based off of coordinates I came in
    main_char.in_combat() #checks for combat
    main_char.draw(GAME.win)

    merchant1.update(main_char,message)

    for enemy in enemies:
      enemy.draw(GAME.win,GAME.currentLevel)

    for npc in npcs:
        npc.draw(GAME.win,GAME.currentLevel)

  if message.show == 1:
    message.update_text()

  #CHAR SHOULD BE LAST BECAUSE HE SHOULD BE THE LAST THING ON TOP OF EVERYTHING
  pygame.display.update() #updates our screen

########## MAIN LOOP FOR GAME ###
#Main loop for game
while run:
  #GET ALL INPUTS
  keys = pygame.key.get_pressed()
  for event in pygame.event.get(): #list of all events in pygame
    if event.type == pygame.QUIT:  #If we quit it
      run = False
    if event.type == pygame.KEYDOWN: #means we can access inventory
      #MESSAGE THINGS
      if message.show == 1 and message.laste == 1:
        if event.key == pygame.K_e:
          message.show = 0
          message.laste = 0
      #inventory stuff
      if message.show == 0:
        ############################################
        #THESE EVENTS ARE PURELY FOR INVENTORY ONLY#
        ############################################
        if event.key == pygame.K_i and inventory.lasti == 0:
          inventory.show_inv = 1
        if event.key == pygame.K_i and inventory.lasti == 1 and inventory.nav_menu_in == 0:
          inventory.show_inv = 0
          inventory.nav_menu = 1

        if event.key == pygame.K_s:
          akey = 's'
        if event.key == pygame.K_a:
          akey = 'a'
        if event.key == pygame.K_d:
          akey = 'd'
        if event.key == pygame.K_w:
          akey = 'w'
        if event.key == pygame.K_e:
          akey = 'e'
        if event.key == pygame.K_q:
          akey = 'q'

        inventory.update(akey)
        akey = ''
########################
#These automatically update the screen rather than updating on a keydown action
########################
    if inventory.show_inv == 1 and inventory.nav_menu_in == 0 and message.show == 0:
      inventory.show_inventory(inventory.show_inv)
      inventory.show_char_stats(GAME.level_list)
    #INTERACTS WITH SUB MENU
    if inventory.nav_menu_in == 1:
      inventory.access_submenu(inventory.nav_menu)

    if inventory.nav_menu_in == 2:
      if inventory.nav_menu == 2: #on equipment
        inventory.show_inventory(inventory.show_inv)
        inventory.access_submenu(inventory.nav_menu)
        #inventory.show_char_stats(GAME.level_list)

    if inventory.nav_menu_in == 3:
      if inventory.nav_menu == 2:
        inventory.show_description(inventory.party[inventory.curr_party_member-1],None)
        inventory.equipment(inventory.curr_party_member)

    if inventory.nav_menu_in == 4:
      if inventory.nav_menu == 2:
        inventory.show_equipment_selection = 1
        inventory.equipment(inventory.curr_party_member)
        inventory.cycle_weapons()
       
    if inventory.nav_menu_in == 6:
      if inventory.nav_menu == 2:
        inventory.equipment(inventory.curr_party_member)
        inventory.cycle_weapons()
        inventory.interact_sub_menu(akey)

    if inventory.nav_menu_in == 7:
      if inventory.nav_menu == 2:
        inventory.confirm_drop()
      #inventory.update_inventory()

##    if inventory.nav_menu_in == 1:  KEEP FOR ITEMS
##      inv = inventory.update_dict()
##      inventory.change_buttons()
##      if len(inv) < 1:
##        inventory.nav_menu_in = 0
##      inventory.access_submenu(inventory.nav_menu)


###################### END OF INVENTORY #########
    if event.type == pygame.KEYUP: #reset variables
      #reset for inventory
      if event.key == pygame.K_e:

        if inventory.nav_menu_in == 2:
          inventory.laste = 1
        if inventory.nav_menu_in == 3:
          inventory.laste = 2
        if inventory.nav_menu_in == 4:
          inventory.laste = 3
        if inventory.nav_menu_in == 5:
          inventory.laste = 4

        if message.show == 1:
          message.laste = 1
      if event.key == pygame.K_i:
        if inventory.show_inv == 1:
          inventory.lasti = 1
        if inventory.show_inv == 0:
          inventory.lasti = 0

  update_screen() #updates our screen

  clock.tick(20)
  pygame.event.pump()
pygame.quit()


#TEXT ON SCREEN
